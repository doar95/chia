"""04. Cuerpos de agua, drenajes, bosque y cerros de la cartografía básica del IGAC a escala 1:25.000.

Insumos públicos:
  insumos/cartografia_igac_25000_chia.txt   extracto del servicio de cartografía del IGAC (ver docs/INSUMOS.md)
  insumos/chia_limite_aproximado.json       contorno simplificado de Chía usado solo para recortar
Uso: python procesamiento/04_agua_bosque_cerros.py
Produce datos/geografia.js.
"""
import json,sys,collections,math
txt=open('insumos/cartografia_igac_25000_chia.txt',encoding='utf-8').read()
sec={};cur=None
for l in txt.split('\n'):
    if l.startswith('@@'): cur=l[2:].strip();sec[cur]=[];continue
    if l.strip() and cur: sec[cur].append(l)
print({k:len(v) for k,v in sec.items()})
def dec(s):
    out=[]
    for r in s.split(';'):
        if not r: continue
        x=y=0;pts=[]
        for p in r.split(' '):
            a,b=p.split(',');x+=int(a);y+=int(b);pts.append([round(x/1e5-75,5),round(y/1e5,5)])
        out.append(pts)
    return out
from shapely.geometry import shape,Polygon,LineString,mapping
core=shape(json.load(open('insumos/chia_limite_aproximado.json'))).buffer(0)
chia=core.buffer(0.004)
def attrs(a): return dict(x.split('=',1) for x in a.split(';') if '=' in x)
def nom(at): return next((v for kk,v in at.items() if 'NOMBRE' in kk.upper() and v and v!='null'),'')
agua=[];bos=[];names=collections.Counter()
for k,t in (('34','l'),('42','l'),('32','d')):
    for l in sec.get(k,[]):
        a,g=l.rsplit('|',1);at=attrs(a);rings=dec(g)
        if not rings or len(rings[0])<4: continue
        try: P=Polygon(rings[0],[r for r in rings[1:] if len(r)>=4]).buffer(0)
        except Exception as e: continue
        if not P.intersects(chia): continue
        if k=='32': P=P.intersection(chia.buffer(0.012))
        names[(k,nom(at))]+=1
        if P.is_empty: continue
        agua.append({'type':'Feature','properties':{'t':t,'n':nom(at)},'geometry':mapping(P)})
for l in sec.get('22',[]):
    a,g=l.rsplit('|',1);at=attrs(a)
    for p in dec(g):
        if len(p)<2: continue
        L=LineString(p)
        if L.intersects(chia):
            names[('22',nom(at))]+=1
            G=L.intersection(chia.buffer(0.012))
            if not G.is_empty: agua.append({'type':'Feature','properties':{'t':'q','n':nom(at)},'geometry':mapping(G)})
for l in sec.get('43',[]):
    a,g=l.rsplit('|',1);rings=dec(g)
    if not rings or len(rings[0])<4: continue
    try: P=Polygon(rings[0],[r for r in rings[1:] if len(r)>=4]).buffer(0)
    except Exception: continue
    if P.intersects(chia):
        P=P.intersection(chia)
        if not P.is_empty and P.area>1e-8: bos.append({'type':'Feature','properties':{},'geometry':mapping(P)})
print('agua',len(agua),'bosque',len(bos)); print(names.most_common(30))
print('orografia',[(attrs(l.rsplit('|',1)[0]),l.rsplit('|',1)[1][:24]) for l in sec.get('7',[])])
k=111.32*110.57*math.cos(math.radians(4.87))
print('bosque ha en Chia',round(sum(shape(f['geometry']).intersection(core).area for f in bos)*k*100,1),'lagunas en Chia',sum(1 for f in agua if f['properties']['t']=='l' and shape(f['geometry']).intersects(core)))
def rd(o):
    if isinstance(o,(list,tuple)): return [rd(x) for x in o]
    if isinstance(o,float): return round(o,5)
    return o
for f in agua+bos: f['geometry']={'type':f['geometry']['type'],'coordinates':rd(f['geometry']['coordinates'])}
s='window.CHIA_GEO_AGUA='+json.dumps({'type':'FeatureCollection','features':agua},ensure_ascii=False,separators=(',',':'))+';window.CHIA_GEO_BOSQUE='+json.dumps({'type':'FeatureCollection','features':bos},separators=(',',':'))+';'
# cerros con nombre: un punto por nombre, el primero que aparece
cerros=[];vistos=set()
for l in sec.get('7',[]):
    a_,g=l.rsplit('|',1);n=nom(attrs(a_));x,y=g.split(',')
    if n and n not in vistos: vistos.add(n);cerros.append([n,round(int(x)/1e5-75,5),round(int(y)/1e5,5)])
s+='window.CHIA_GEO_CERROS='+json.dumps(cerros,ensure_ascii=False)+';'
open('datos/geografia.js','w',encoding='utf-8').write(s);print(len(s))
json.dump({'type':'FeatureCollection','features':agua},open('datos/agua_igac.geojson','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
json.dump({'type':'FeatureCollection','features':bos},open('datos/bosque_igac.geojson','w',encoding='utf-8'),separators=(',',':'))
