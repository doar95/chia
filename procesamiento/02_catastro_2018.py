"""02. Catastro 2018: del listado predial del IGAC a tablas agregadas.

Insumo NO publicable: los listados "Registro 1 y 2" del IGAC para Chía, corte del 28 de mayo de 2018,
en dos libros de Excel de una sola columna de texto con ancho fijo. Contienen nombres, documentos y
direcciones de propietarios. Deben ponerse en la carpeta privado/ con estos nombres:
  privado/num-25-175 RURAL original.xlsx
  privado/num-25-175 URBANO original.xlsx
Se piden al IGAC o al gestor catastral. La carpeta privado/ está excluida del repositorio.
Uso: python procesamiento/02_catastro_2018.py
Produce privado/pred_2018.json, que no se publica, y los agregados públicos
datos/_catastro.json, datos/catastro_zona_2018.csv y datos/catastro_manzana_2018.csv.
Solo salen grupos de cinco o más predios.
"""
# --- Paso A: pasar los libros de Excel a texto
import openpyxl
base='privado/'
for f in ['num-25-175 RURAL original.xlsx','num-25-175 URBANO original.xlsx']:
    ws=openpyxl.load_workbook(base+f,read_only=True).worksheets[0]
    L=[r[0] for r in ws.iter_rows(values_only=True)]
    open('privado/'+f.split()[1]+'.txt','w',encoding='utf-8').write('\n'.join('' if x is None else str(x) for x in L))
    print(f,len(L))

# --- Paso B: leer cada predio. Se toma solo la primera línea de propietario y no se guarda ningún dato personal
import re,collections,json,statistics as st
def parse(fn):
    L=open(fn,encoding='utf-8').read().split('\n'); out={}
    r1=re.compile(r'^ (\d{15}) (\d{3}) (\d{3}) .*([A-Z])\s+(\d+) (\d{4})\s+(\d+) \$\s+([\d.]+)\s*$')
    r2=re.compile(r'^ (\d{3}) (\d{2}) (.{18}) (\d{2}) (\d{2}) (\d{10})')
    cur=None;bad=0
    for l in L:
        m=r1.match(l)
        if m:
            k=m.group(1)
            if m.group(2)=='001' and k not in out:
                out[k]=dict(dest=m.group(4),terr=int(m.group(5))*10000+int(m.group(6)),cons=int(m.group(7)),av=int(m.group(8).replace('.','')),nprop=int(m.group(3)))
                cur=k
            else: cur=None
            continue
        m=r2.match(l)
        if m and cur and 'ze' not in out[cur] and m.group(1)=='001': out[cur]['zf']=m.group(4);out[cur]['ze']=m.group(5)
        elif re.match(r'^ \d{15} ',l): bad+=1
    return out,bad
R,b1=parse('privado/RURAL.txt');U,b2=parse('privado/URBANO.txt')
print(len(R),b1,len(U),b2, len(set(R)&set(U)))
A=dict(U);A.update(R)
print('total',len(A))
c=collections.Counter(k[:2] for k in A);print('tipo',c)
c=collections.Counter(k[:4] for k in A);print('tipo+sector',sorted(c.items()))
c=collections.Counter(k[:8] for k in A if k[:2]=='00');print('rural vereda',sorted(c.items()))
print('dest',collections.Counter(v['dest'] for v in A.values()).most_common())
print('avaluo total',sum(v['av'] for v in A.values())/1e12)
print('mejoras',sum(1 for k in A if k[12:]!='000'))
json.dump(A,open('privado/pred_2018.json','w'))

# --- Paso C: agregados por zona, destino, zona geoeconómica y manzana
import json,statistics as st,collections,math,csv
A=json.load(open('privado/pred_2018.json'))
VER={'0002':'Fonquetá','0003':'Fagua','0004':'Bojacá','0005':'Yerbabuena','0006':'Fusca','0007':'La Balsa','0008':'Cerca de Piedra','0009':'Tíquiza'}
def zona(k):
    if k[:2]=='00': return VER.get(k[4:8])
    return 'Urbano' if k[:2]=='01' else 'Urbano Calahorra'
def q(v,p): v=sorted(v); return v[min(int(p*len(v)),len(v)-1)]
rows=[]
for k,v in A.items():
    z=zona(k)
    if not z: continue
    v['z']=z; v['k']=k
    v['m2']= v['av']/v['terr'] if (v['terr']>0 and k[12:]=='000') else None
    rows.append(v)
print(len(rows))
out={'n':len(rows),'tot':sum(v['av'] for v in rows)}
Z=[]
for z in list(VER.values())+['Urbano','Urbano Calahorra']:
    r=[v for v in rows if v['z']==z]; m=[v['m2'] for v in r if v['m2']]
    Z.append({'z':z,'n':len(r),'av':round(sum(v['av'] for v in r)/1e9,1),'med':round(st.median(v['av'] for v in r)/1e6,1),'nm2':len(m),'p25':round(q(m,.25)),'p50':round(q(m,.5)),'p75':round(q(m,.75))})
    print(Z[-1])
out['zonas']=Z
DN={'A':'hab','D':'agro','C':'com','Q':'lote','R':'lote','S':'lote'}
D=collections.defaultdict(list)
for v in rows: D[DN.get(v['dest'],'otros')].append(v)
out['dest']=[{'d':d,'n':len(r),'av':round(sum(v['av'] for v in r)/1e9,1),'p50':round(q([v['m2'] for v in r if v['m2']],.5))} for d,r in D.items()]
print(out['dest'])
# histograma avaluo por predio, log10 bins de 0.25 entre 1e6 y 1e10
def hist(vals,lo,hi,step):
    n=int(round((hi-lo)/step)); h=[0]*n
    for x in vals:
        if x>0:
            i=int((math.log10(x)-lo)/step); h[max(0,min(n-1,i))]+=1
    return h
out['hAv']={'lo':6,'step':0.25,'u':hist([v['av'] for v in rows if v['z'].startswith('Urb')],6,10,.25),'r':hist([v['av'] for v in rows if not v['z'].startswith('Urb')],6,10,.25)}
out['hM2']={'lo':3,'step':0.25,'u':hist([v['m2'] for v in rows if v['m2'] and v['z'].startswith('Urb')],3,6.5,.25),'r':hist([v['m2'] for v in rows if v['m2'] and not v['z'].startswith('Urb')],3,6.5,.25)}
print(out['hAv'],out['hM2'])
# zonas economicas urbanas
ZE=collections.defaultdict(list)
for v in rows:
    if v['z']=='Urbano' and v.get('ze') and v['m2']: ZE[v['ze']].append(v['m2'])
out['ze']=sorted([{'ze':k,'n':len(m),'p50':round(q(m,.5))} for k,m in ZE.items() if len(m)>=20],key=lambda x:x['p50'])
print(out['ze'])
# CSV por manzana/sector (n>=5)
M=collections.defaultdict(list)
for v in rows: M[(v['z'],v['k'][:8])].append(v)
w=csv.writer(open('datos/catastro_manzana_2018.csv','w',newline='',encoding='utf-8'))
w.writerow(['zona','codigo_sector_manzana','predios','avaluo_total_millones','mediana_avaluo_millones','mediana_avaluo_por_m2_terreno','predios_con_valor_m2'])
nm=0
for (z,c),r in sorted(M.items()):
    if len(r)>=5:
        m=[v['m2'] for v in r if v['m2']]; nm+=1
        w.writerow([z,c,len(r),round(sum(v['av'] for v in r)/1e6,1),round(st.median(v['av'] for v in r)/1e6,1),round(q(m,.5)) if len(m)>=5 else '',len(m)])
print('manzanas',nm,len(M))
w=csv.writer(open('datos/catastro_zona_2018.csv','w',newline='',encoding='utf-8'));w.writerow(['zona','predios','avaluo_total_miles_de_millones','mediana_avaluo_millones','predios_con_valor_m2','p25_m2','mediana_m2','p75_m2'])
for z in Z: w.writerow([z['z'],z['n'],z['av'],z['med'],z['nm2'],z['p25'],z['p50'],z['p75']])
json.dump(out,open('datos/_catastro.json','w',encoding='utf-8'),ensure_ascii=False)
print(out['n'],out['tot']/1e12)
