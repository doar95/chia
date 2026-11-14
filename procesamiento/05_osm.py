"""05. Cultivos, invernaderos, quebradas menores y canales de OpenStreetMap. Complemento no oficial.

Insumo público: insumos/osm_chia_2026-11-14.txt, extracto de OpenStreetMap del 14 de noviembre de 2026
obtenido con la consulta Overpass que está en docs/INSUMOS.md. Datos bajo licencia ODbL, © colaboradores de OpenStreetMap.
Formato: secciones @cul cultivos, @inv invernaderos y @oww cursos de agua. Cada línea es nombre|tipo|geometría,
con coordenadas en enteros de cien milésimas de grado, la primera relativa al origen (-74,2 ; 4,7) y las demás como diferencias.
Uso: python procesamiento/05_osm.py     Requiere haber corrido 01, que produce datos/_base.json.
Produce datos/geografia_osm.js y datos/cultivos_osm.geojson.
"""
import json
from shapely.geometry import Polygon, LineString, shape, mapping
sec = {}; cur = None
for l in open('insumos/osm_chia_2026-11-14.txt', encoding='utf-8').read().split('\n'):
    if l.startswith('@'): cur = l[1:]; sec[cur] = []; continue
    if l: sec[cur].append(l)
def dec(r):
    out = []; x = y = 0
    for p in r.split(' '):
        a, b = p.split(','); x += int(a); y += int(b); out.append((round(x / 1e5 - 74.2, 5), round(y / 1e5 + 4.7, 5)))
    return out
D = json.load(open('datos/_base.json', encoding='utf-8'))
chia = shape([m for m in D['mun']['features'] if m['properties']['c'] == 25175][0]['geometry']).buffer(0)
area = chia.buffer(0.012)          # Chía más un borde de contexto de 1,3 km aproximadamente
def feat(g, props):
    m = mapping(g)
    def rr(c): return [round(c[0], 5), round(c[1], 5)] if isinstance(c[0], (float, int)) else [rr(x) for x in c]
    return {'type': 'Feature', 'properties': props, 'geometry': {'type': m['type'], 'coordinates': rr(m['coordinates'])}}
def polys(lines, t):
    out = []
    for l in lines:
        n, a, g = l.split('|', 2)
        for r in g.split(';'):
            pts = dec(r)
            if len(pts) >= 4:
                p = Polygon(pts).buffer(0)
                if not p.is_empty and p.intersects(area): out.append(feat(p.intersection(area), {'t': t}))
    return out
cul = polys(sec['cul'], 'c') + polys(sec['inv'], 'i')
q = []
for l in sec['oww']:
    n, a, g = l.split('|', 2)
    for r in g.split(';'):
        pts = dec(r)
        if len(pts) >= 2:
            ls = LineString(pts)
            if ls.intersects(area):
                c = ls.intersection(area)
                if not c.is_empty: q.append(feat(c, {'n': n.strip(), 't': a}))
open('datos/geografia_osm.js', 'w', encoding='utf-8').write('window.CHIA_GEO_CULT=' + json.dumps({'type': 'FeatureCollection', 'features': cul}, ensure_ascii=False, separators=(',', ':')) + ';window.CHIA_GEO_QOSM=' + json.dumps({'type': 'FeatureCollection', 'features': q}, ensure_ascii=False, separators=(',', ':')) + ';')
json.dump({'type': 'FeatureCollection', 'features': cul}, open('datos/cultivos_osm.geojson', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
k = 111.32 * 110.57 * 0.9964 * 100
print('cultivos ha', round(sum(shape(f['geometry']).intersection(chia).area for f in cul if f['properties']['t'] == 'c') * k), 'invernaderos ha', round(sum(shape(f['geometry']).intersection(chia).area for f in cul if f['properties']['t'] == 'i') * k), 'tramos', len(q))
