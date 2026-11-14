"""03. Predios del IGAC de 2026 con destino económico y rejilla de avalúo de 2018.

Insumos:
  insumos/catastro_igac_2026_chia.txt   público, extracto de la Base Catastral Pública del IGAC (ver docs/INSUMOS.md)
  privado/pred_2018.json                 no publicable, lo produce el paso 02
Uso: python procesamiento/03_predios_y_rejilla.py
Produce datos/predios_2026.geojson, datos/avaluo_rejilla_2018.geojson y datos/veredas_igac_2026.geojson.
El cruce es por número predial anterior. Cuando el predio de 2026 no cruza directo pero sí su terreno,
caso típico de la propiedad horizontal, se toma el destino más frecuente de sus unidades.
Cada predio publicado lleva solo el destino agrupado. El avalúo sale únicamente en celdas con cinco o más predios.
"""
import json,sys
def dec(s):
    rings=[]
    for r in s.split(';'):
        if not r: continue
        x=y=0;pts=[]
        for p in r.split(' '):
            a,b=p.split(',');x+=int(a);y+=int(b);pts.append([round(x/1e5-75,5),round(y/1e5,5)])
        rings.append(pts)
    return rings
def load(fn):
    sec={};cur=None
    for l in open(fn,encoding='utf-8').read().split('\n'):
        if l.startswith('@@'): cur=l[2:];sec[cur]=[];continue
        if l and cur: 
            p=l.split('|'); sec[cur].append((p[:-1],dec(p[-1])))
    return sec

import collections,statistics as st,math
from shapely.geometry import Polygon
S=load('insumos/catastro_igac_2026_chia.txt')
A=json.load(open('privado/pred_2018.json'))
pref=collections.defaultdict(list)
for k,v in A.items(): pref[k[:12]].append(v)
DN={'A':'h','D':'a','C':'c','Q':'l','R':'l','S':'l'}
KX=111320*math.cos(math.radians(4.87)); KY=110570
feats=[];stat=collections.Counter();pts=[]
for sec in('ut','rt'):
    for a,g in S[sec]:
        if not g or len(g[0])<4: stat['nogeom']+=1;continue
        ring=g[0]
        try:
            P=Polygon([(x*KX,y*KY) for x,y in ring]);area=abs(P.area);c=P.representative_point()
        except Exception: stat['bad']+=1;continue
        k=a[0][5:] if len(a[0])==20 else None
        d='n';m2=None
        if k and k in A:
            v=A[k];d=DN.get(v['dest'],'o');stat['directo']+=1
            t=v['terr'] if v['terr']>0 else area
            if t>0 and k[12:]=='000': m2=v['av']/t
        elif k and k[:12] in pref:
            vs=pref[k[:12]];stat['ph']+=1
            d=DN.get(collections.Counter(v['dest'] for v in vs).most_common(1)[0][0],'o')
            if area>20: m2=sum(v['av'] for v in vs)/area
        else: stat['sin']+=1
        feats.append({'type':'Feature','properties':{'d':d,'u':1 if sec=='ut' else 0},'geometry':{'type':'Polygon','coordinates':[[[round(x,5),round(y,5)] for x,y in r] for r in g]}})
        if m2 and 500<m2<2e7: pts.append((c.x/KX,c.y/KY,m2))
print(stat,len(feats),len(pts))
print('dest',collections.Counter(f['properties']['d'] for f in feats))
# rejilla ~150 m
STEP=0.0014
cells=collections.defaultdict(list)
for x,y,m in pts: cells[(math.floor(x/STEP),math.floor(y/STEP))].append(m)
grid=[]
for (i,j),ms in cells.items():
    if len(ms)>=5:
        x0=round(i*STEP,5);y0=round(j*STEP,5);x1=round(x0+STEP,5);y1=round(y0+STEP,5)
        grid.append({'type':'Feature','properties':{'v':int(round(st.median(ms),-3)),'n':len(ms)},'geometry':{'type':'Polygon','coordinates':[[[x0,y0],[x1,y0],[x1,y1],[x0,y1],[x0,y0]]]}})
vals=sorted(f['properties']['v'] for f in grid)
print('celdas',len(grid),'de',len(cells),'cuantiles',[vals[int(len(vals)*q)] for q in(.05,.25,.5,.75,.95)])
cov=sum(len(ms) for ms in cells.values() if len(ms)>=5);print('predios en celdas publicadas',cov,len(pts))
json.dump({'type':'FeatureCollection','features':feats},open('datos/predios_2026.geojson','w'),separators=(',',':'))
json.dump({'type':'FeatureCollection','features':grid},open('datos/avaluo_rejilla_2018.geojson','w'),separators=(',',':'))
ver=[{'type':'Feature','properties':{'cod':a[0],'n':a[1]},'geometry':{'type':'Polygon','coordinates':g}} for a,g in S['vereda']]
per=[{'type':'Feature','properties':{'n':a[0]},'geometry':{'type':'Polygon','coordinates':g}} for a,g in S['perim']]
json.dump({'type':'FeatureCollection','features':ver+per},open('datos/veredas_igac_2026.geojson','w'))
import os;print(os.path.getsize('datos/predios_2026.geojson'),os.path.getsize('datos/avaluo_rejilla_2018.geojson'))
