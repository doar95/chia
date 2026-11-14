"""01. Límites, veredas, población, pirámide y hacienda.

Insumos públicos, tomados de dos repositorios del mismo autor:
  --incendios  carpeta del repositorio doar95/incendios-colombia (veredas DANE 2024 en datos/d_25.json y d_11.json)
  --carga      carpeta del repositorio doar95/carga-tributaria-ciudades (población DANE y panel fiscal DNP)
Uso, desde la raíz de este repositorio:
  python procesamiento/01_base.py --incendios ../incendios-colombia --carga ../carga-tributaria-ciudades
Produce datos/_base.json y los archivos abiertos CSV y GeoJSON.
"""
import json, csv, math, argparse
from shapely.geometry import shape, mapping, box, Polygon
from shapely.ops import unary_union
ap = argparse.ArgumentParser(); ap.add_argument('--incendios', required=True); ap.add_argument('--carga', required=True); a = ap.parse_args()
SC = {25126:'Cajicá',25175:'Chía',25200:'Cogua',25214:'Cota',25295:'Gachancipá',25486:'Nemocón',25758:'Sopó',25785:'Tabio',25799:'Tenjo',25817:'Tocancipá',25899:'Zipaquirá'}
SO = {25099:'Bojacá',25260:'El Rosal',25269:'Facatativá',25286:'Funza',25430:'Madrid',25473:'Mosquera',25769:'Subachoque',25898:'Zipacón'}
ALL = {**SC, **SO}

# --- Límites municipales: unión de veredas más las cabeceras que la capa veredal deja vacías
d25 = json.load(open(a.incendios + '/datos/d_25.json'))['features']
fs = d25 + json.load(open(a.incendios + '/datos/d_11.json'))['features']
R = box(-74.65, 4.5, -73.7, 5.35)
by = {}
for f in fs:
    g = shape(f['geometry']).buffer(0)
    if g.intersects(R): by.setdefault(f['properties']['mc'], []).append(g)
un = {mc: unary_union(gs).buffer(0.0004).buffer(-0.0004) for mc, gs in by.items()}
tot = unary_union(list(un.values()))
gaps = R.difference(tot.buffer(0.0002))
gaps = [g for g in (gaps.geoms if gaps.geom_type != 'Polygon' else [gaps]) if 2e-6 < g.area < 0.02]
extra = {}
for g in gaps:                      # cada vacío se asigna al municipio con el que comparte más borde
    gb = g.buffer(0.0012); best = None; bl = 0
    for mc, u in un.items():
        if u.intersects(gb):
            l = u.boundary.intersection(gb).length
            if l > bl: bl = l; best = mc
    if best in ALL: extra.setdefault(best, []).append(g.buffer(0.0006))
def rnd(geom):
    r = lambda c: [[round(x, 4), round(y, 4)] for x, y in c]
    m = mapping(geom)
    if m['type'] == 'Polygon': return {'type': 'Polygon', 'coordinates': [r(x) for x in m['coordinates']]}
    return {'type': 'MultiPolygon', 'coordinates': [[r(x) for x in p] for p in m['coordinates']]}
k = 111.32 * 110.57 * math.cos(math.radians(4.86))
mun = []
for mc in ALL:
    u = unary_union([un[mc]] + extra.get(mc, [])).buffer(0.0005).buffer(-0.0005)
    ps = [u] if u.geom_type == 'Polygon' else list(u.geoms)
    u = unary_union([Polygon(p.exterior) for p in ps if p.area > 2e-6]).simplify(0.0005)
    print(ALL[mc], round(u.area * k, 1), 'km2')
    mun.append({'type': 'Feature', 'properties': {'c': mc, 'n': ALL[mc], 'p': 'centro' if mc in SC else 'occidente'}, 'geometry': rnd(u)})
ver = [{'type': 'Feature', 'properties': {'n': f['properties']['n'], 'a': f['properties']['a']}, 'geometry': f['geometry']} for f in d25 if f['properties']['mc'] == 25175]

# --- Población anual DANE
pop = {}
for r in csv.DictReader(open(a.carga + '/data/intermedios/poblacionMunicipal1985a2025.csv')):
    c = int(r['codigo'])
    if c in ALL: pop.setdefault(c, {})[int(r['anio'])] = [round(float(r['pob'])), round(float(r['pobCabecera'])) if r['pobCabecera'] else None]

# --- Pirámide 2005 y 2017, retroproyección DANE por edad simple agrupada en quinquenios
import openpyxl
ws = openpyxl.load_workbook(a.carga + '/insumos/pob_2005_2017_sexoedad.xlsx', read_only=True)['NuevaMpal']
hdr = None; rows = []
for r in ws.iter_rows(values_only=True):
    if hdr is None:
        if r and any(str(x).strip().upper() in ('AÑO', 'ANO') for x in r if x): hdr = [str(x) for x in r]
        continue
    if '25175' in [str(x) for x in r[:5]]: rows.append(r)
def pir(year):
    r = [x for x in rows if x[4] == year and x[5] == 'Total'][0]
    H = [0] * 18; M = [0] * 18
    for i, name in enumerate(hdr):
        for S, arr in (('Hombres_', H), ('Mujeres_', M)):
            if name.startswith(S):
                e = name[len(S):]; e = 85 if e.startswith('85') else int(e)
                arr[min(e // 5, 17)] += int(r[i])
    return {'h': H, 'm': M}
P = {str(y): pir(y) for y in (2005, 2017)}

# --- Hacienda, panel DNP
fis = []
for r in csv.DictReader(open(a.carga + '/data/panelCargaTributaria1984a2025.csv', encoding='utf-8')):
    if r['codigo'] == '25175':
        f = lambda kk: round(float(r[kk]), 1) if r[kk] not in ('', None) else None
        fis.append({'a': int(r['anio']), 'cat': r['categoria'], 'pred': f('predialConst2025'), 'ica': f('icaConst2025'), 'otros': f('otrosTributariosConst2025'), 'trib': f('tributariosConst2025'), 'tot': f('ingresosTotalesConst2025'), 'pc': f('pcTributarios2025'), 'aut': f('autonomiaTributaria'), 'inv': f('inversion'), 'fun': f('funcionamiento'), 'gas': f('gastosTotales'), 'ing': f('ingresosTotales'), 'rep': r['reporta'], 'al': r['alertaCalidad']})

json.dump({'mun': {'type': 'FeatureCollection', 'features': mun}, 'ver': {'type': 'FeatureCollection', 'features': ver}, 'pop': pop, 'pir': P, 'fis': fis}, open('datos/_base.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
json.dump({'type': 'FeatureCollection', 'features': mun}, open('datos/limites_municipios.geojson', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
json.dump({'type': 'FeatureCollection', 'features': ver}, open('datos/veredas_dane_2024.geojson', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
w = csv.writer(open('datos/poblacion.csv', 'w', newline='', encoding='utf-8')); w.writerow(['codigo', 'municipio', 'provincia', 'anio', 'poblacion', 'cabecera'])
for c in pop:
    for y in sorted(pop[c]): w.writerow([c, ALL[c], 'Sabana Centro' if c in SC else 'Sabana Occidente', y] + pop[c][y])
w = csv.writer(open('datos/piramide_2005_2017.csv', 'w', newline='', encoding='utf-8')); w.writerow(['anio', 'edad_desde', 'hombres', 'mujeres'])
for y in P:
    for i in range(18): w.writerow([y, i * 5, P[y]['h'][i], P[y]['m'][i]])
w = csv.writer(open('datos/hacienda.csv', 'w', newline='', encoding='utf-8')); kk = list(fis[0].keys()); w.writerow(kk)
for x in fis: w.writerow([x[i] for i in kk])
print('listo')
