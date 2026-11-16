"""10. Plan de arborización: zonas estratégicas, coordenadas, número de árboles y costos.

Insumos (todos en el repositorio):
  datos/limites_municipios.geojson, datos/veredas_igac_2026.geojson, datos/agua_igac.geojson,
  datos/bosque_igac.geojson, datos/geografia.js (cerros), datos/predios_2026.geojson,
  insumos/osm_arborizacion_2026-11-16.txt (vías, parques y colegios de OpenStreetMap).
Produce:
  planarborizacion/datos/zonas.geojson   zonas de siembra con atributos
  planarborizacion/datos/zonas.csv       la misma tabla, con coordenadas
  planarborizacion/datos/prioridad.geojson  rejilla urbana de prioridad de sombra (200 m)
  planarborizacion/datos/resumen.json    totales por tipo y por etapa
Uso: python procesamiento/10_arborizacion.py
Todas las cantidades son potenciales técnicos para planeación. Cada punto exige visita de campo,
verificación de redes, propiedad del suelo y concepto de la autoridad ambiental antes de sembrar.
"""
import json, csv, math, sys
sys.path.insert(0, 'procesamiento')
from recetas_arborizacion import R as RECETA, MESES, LIMITES
from collections import defaultdict
from shapely.geometry import shape, mapping, LineString, Point, box
from shapely.ops import transform, unary_union
from pyproj import Transformer

A = Transformer.from_crs('EPSG:4326', 'EPSG:9377', always_xy=True).transform   # MAGNA-SIRGAS origen nacional, metros
G = Transformer.from_crs('EPSG:9377', 'EPSG:4326', always_xy=True).transform
m = lambda g: transform(A, g)
w = lambda g: transform(G, g)

def load(p): return json.load(open(p, encoding='utf-8'))
def js(p, var):
    t = open(p, encoding='utf-8').read(); i = t.index('window.' + var + '=') + len('window.' + var + '=')
    return json.JSONDecoder().raw_decode(t[i:])[0]

lim = [shape(f['geometry']) for f in load('datos/limites_municipios.geojson')['features'] if f['properties']['c'] == 25175][0].buffer(0)
CH = m(lim)
NOMV = {'YERBABUENA': 'Yerbabuena', 'CERCA DE PIEDRA': 'Cerca de Piedra', 'FUSCA': 'Fusca', 'BOJACA': 'Bojacá', 'FONQUETA': 'Fonquetá', 'TIQUIZA': 'Tíquiza', 'SN': 'La Balsa', 'FAGUA': 'Fagua', 'CHIA': 'Cabecera urbana', 'MERCEDES DE CALAHORRA': 'Mercedes de Calahorra'}
VER = [(NOMV[f['properties']['n']], m(shape(f['geometry']).buffer(0))) for f in load('datos/veredas_igac_2026.geojson')['features']]
def vereda(g):
    c = g.representative_point() if g.geom_type != 'Point' else g
    best = [n for n, p in VER if p.contains(c)]
    if best: return best[0]
    return min(VER, key=lambda v: v[1].distance(c))[0]
AG = load('datos/agua_igac.geojson')['features']
BOS = unary_union([m(shape(f['geometry']).buffer(0)) for f in load('datos/bosque_igac.geojson')['features']])
PRE = load('datos/predios_2026.geojson')['features']

# ---------- insumo OSM curado ----------
sec, cur = defaultdict(list), None
for l in open('insumos/osm_arborizacion_2026-11-16.txt', encoding='utf-8'):
    l = l.rstrip('\n')
    if not l or l.startswith('#'): continue
    if l.startswith('@'): cur = l[1:]; continue
    sec[cur].append(l.split('|'))

# ---------- costos unitarios (pesos colombianos de 2027, IVA incluido) ----------
# Ver documento, sección 7. Restauración: precios del contrato SAMC-012-2025 de Chía indexados 12 %.
COSTO = {
    'urbano':      480_000,   # árbol ≥2,0 m, bolsa ≥20 L, sustrato, tutor triple, protector, riego y mantenimiento 36 meses, reposición 15 %
    'vial':        520_000,   # igual que urbano más manejo de tráfico y protección contra impacto vehicular
    'ronda':        62_000,   # restauración 0,9–1,2 m a 3 x 3 m, preparación, 6 mantenimientos en 3 años, reposición 20 %
    'cerro':        58_000,   # enriquecimiento en claros de ladera, mismo paquete que ronda con menor plateo
    'cerca':        28_000,   # cerca viva con arbolito o arbusto nativo de 0,6–0,9 m cada 3 m, 2 años de mantenimiento comunitario
    'escolar':     450_000,   # árbol de sombra en colegio público, mantenimiento compartido con la comunidad educativa
    'parque':      460_000,   # árbol en parque, incluye diseño de grupo y acolchado
}

zonas = []
def add(zid, nombre, tipo, etapa, geom_m, arboles, especies, gestor='', nota='', financia='Público'):
    g4 = w(geom_m)
    c = geom_m.representative_point() if geom_m.geom_type != 'Point' else geom_m
    c4 = w(c)
    b = g4.bounds
    long_m = round(geom_m.length) if geom_m.geom_type in ('LineString', 'MultiLineString') else None
    area_ha = round(geom_m.area / 1e4, 2) if geom_m.geom_type in ('Polygon', 'MultiPolygon') else None
    zonas.append({'id': zid, 'nombre': nombre, 'tipo': tipo, 'etapa': etapa, 'vereda': vereda(c), 'gestor': gestor,
                  'lat': round(c4.y, 5), 'lon': round(c4.x, 5),
                  'bbox': [round(b[1], 5), round(b[0], 5), round(b[3], 5), round(b[2], 5)],
                  'longitud_m': long_m, 'area_ha': area_ha, 'arboles': int(arboles), 'paleta': especies,
                  'costo_cop': int(arboles * COSTO[tipo]), 'financia': financia, 'nota': nota, '_g': g4})

# ---------- 1. Rondas hídricas: franja de 30 m a cada lado, fracción sembrable ----------
rios = defaultdict(list)
for f in AG:
    if f['properties']['t'] == 'q':
        rios[f['properties']['n']].append(m(shape(f['geometry'])))
osm_q = {'Quebrada Tiquiza': [(-74.0789, 4.8757), (-74.0774, 4.8750), (-74.0752, 4.8750), (-74.0742, 4.8738), (-74.0719, 4.8733), (-74.0710, 4.8727), (-74.0672, 4.8693), (-74.0661, 4.8688)]}
for n, pts in osm_q.items(): rios[n].append(m(LineString(pts)))
urb = m(unary_union([shape(f['geometry']).buffer(0) for f in load('datos/veredas_igac_2026.geojson')['features'] if f['properties']['n'] in ('CHIA', 'MERCEDES DE CALAHORRA')]))
k = 0
for n, ls in sorted(rios.items()):
    line = unary_union(ls).intersection(CH)
    if line.is_empty: continue
    strip = line.buffer(30, cap_style=2).intersection(CH).difference(BOS)
    if n.startswith('Río'):
        # se divide cada río en tramo urbano y tramo rural porque cambian el gestor, la etapa y la paleta
        fr_rural = 0.30 if 'Bogotá' in n else 0.45
        for parte, geo, etapa, frac in (('urbano', strip.intersection(urb.buffer(150)), 1, 0.35), ('rural', strip.difference(urb.buffer(150)), 2, fr_rural)):
            if geo.area < 5000: continue
            k += 1
            add(f'R{k:02d}', f'{n}, ronda {parte}', 'ronda', etapa, geo, geo.area / 1e4 * frac * 1111, 'P1 ribereña',
                'Municipio, CAR y propietarios', f'Franja de 30 m por margen; se asume sembrable el {int(frac*100)} % (el resto es vía, construcción, pastos de uso o ya arbolado).', 'Mixto' if parte == 'rural' else 'Público')
    else:
        k += 1
        add(f'R{k:02d}', f'{n}, ronda', 'ronda', 2, strip, strip.area / 1e4 * 0.45 * 1111, 'P1 ribereña',
            'Municipio, CAR y propietarios', 'Franja de 30 m por margen; se asume sembrable el 45 %.', 'Mixto')
k += 1
cg = m(LineString([tuple(map(float, p.split(','))) for p in [r for r in sec['via'] if r[0] == 'V14'][0][3].split(' ')]))
add(f'R{k:02d}', 'Canal Guaymaral, franja de amortiguación', 'ronda', 2, cg.buffer(15, cap_style=2).intersection(CH), cg.length / 3 * 0.6, 'P1 ribereña',
    'Municipio y CAR', 'Una hilera por margen a 6 m; 60 % de la longitud disponible.')

# ---------- 2. Corredores viales ----------
for r in sec['via']:
    zid, nombre, gestor, coords = r
    if zid == 'V14': continue
    ln = m(LineString([tuple(map(float, p.split(','))) for p in coords.split(' ')])).intersection(CH)
    if ln.is_empty or ln.length < 300: continue
    enurb = ln.intersection(urb.buffer(100)).length / ln.length
    etapa = 1 if zid in ('V01', 'V05', 'V06', 'V07') else (3 if gestor.startswith('Nación') or 'Troncal' in gestor else 2)
    frac = 0.45 if enurb > 0.5 else 0.6
    arb = ln.length / 10 * 2 * frac
    add(zid, nombre, 'vial', etapa, ln, arb, 'P3 vial' if enurb > 0.5 else 'P2 sabana',
        gestor, f'Un árbol cada 10 m por costado donde haya andén, separador o franja ≥1,5 m; se asume factible el {int(frac*100)} % de la longitud.', 'Público' if gestor.startswith('Municipio') else 'Gestión con el titular de la vía')

# ---------- 3. Parques, colegios e instituciones (de OSM) ----------
k = 0
for t, n, x, y, a in sec['pol']:
    p = m(Point(float(x), float(y)))
    if not CH.contains(p): continue
    a = float(a)
    if t in ('park', 'recr') and a >= 2000:
        priv = n in ('Club Campestre Guaymaral', 'Parque Hipódromo de los Andes', 'Área social Encenillos de Sindamanoy', 'Buenavista Colsubsidio', 'Parque Centro Comercial Centro Chía', 'Faunáticos Granja Pedagógica')
        arb = min(a / 120, 400)
        k += 1
        add(f'P{k:02d}', n or f'Zona verde sin nombre ({float(y):.4f}, {float(x):.4f})', 'parque', 3 if priv else (1 if a < 30000 else 2), p.buffer(math.sqrt(a / math.pi)), arb,
            'P4 parque', 'Privado (convenio voluntario)' if priv else 'Municipio', 'Un árbol por cada 120 m² de zona verde hasta 400 por sitio; ajustar con el censo de lo ya plantado.', 'Privado' if priv else 'Público')
    elif t in ('scho', 'coll', 'univ', 'hosp', 'town') and a >= 2500:
        publico = any(s in n for s in ('IED', 'Institución Educativa', 'Fagua', 'Diosa', 'Conaldi', 'Departamental', 'Yerbabuena', 'Fonquetá', 'IE Fusca', 'Universidad de Cundinamarca', 'SENA', 'Hospital San Antonio', 'Centro Administrativo'))
        arb = min(a / 250, 120)
        k += 1
        add(f'E{k:02d}', n or 'Institución sin nombre', 'escolar', 1 if publico else 3, p.buffer(math.sqrt(a / math.pi)), arb,
            'P4 parque', 'Municipio / Secretaría de Educación' if publico else 'Privado (convenio voluntario)', 'Patio de sombra: un árbol por cada 250 m² de predio hasta 120.', 'Público' if publico else 'Privado')

# ---------- 4. Cerros: franja de 300 m alrededor del bosque IGAC, fuera de lo urbano ----------
# Sin modelo de elevación en este paso, la ladera se aproxima por la vecindad del bosque remanente:
# restaurar junto a los parches existentes aumenta la conectividad y la llegada de semillas por aves.
borde = BOS.buffer(300).difference(BOS).difference(urb.buffer(100)).intersection(CH)
oeste = borde.intersection(box(*CH.bounds[:2], A(-74.062, 0)[0], CH.bounds[3]))
este = borde.difference(oeste)
for i, (nombre, g) in enumerate((('Cerro del Majuy y La Valvanera (occidente)', oeste), ('Cerros orientales: Yerbabuena, Fusca y La Caro', este))):
    meta_ha = 30 if i == 0 else 50          # 80 ha de núcleos en total, coherente con la meta 49 del Plan de Desarrollo (157,5 ha por recuperar)
    add(f'M{i+1:02d}', f'{nombre}: núcleos de restauración junto al bosque', 'cerro', 2, g, meta_ha * 625, 'P5 ladera',
        'Municipio (predios públicos), CAR y propietarios', f'Franja de 300 m alrededor del bosque IGAC ({g.area/1e4:,.0f} ha) como área de búsqueda; meta de {meta_ha} ha de núcleos a 4 x 4 m, primero en predios municipales y nacimientos.', 'Mixto')

# ---------- 5. Cercas vivas rurales en predios agropecuarios ----------
agro = defaultdict(float)
for f in PRE:
    if f['properties']['d'] == 'a':
        g = m(shape(f['geometry']).buffer(0))
        agro[vereda(g)] += g.length
for n, per in sorted(agro.items()):
    if per < 2000: continue
    geo = unary_union([m(shape(f['geometry']).buffer(0)) for f in PRE if f['properties']['d'] == 'a' and vereda(m(shape(f['geometry']).buffer(0))) == n]).buffer(0)
    add('C-' + ''.join(ch for ch in n.upper() if ch.isalpha())[:3].replace('Í','I').replace('Á','A'), f'Cercas vivas, vereda {n}', 'cerca', 3, geo, per * 0.5 * 0.10 / 3, 'P6 cerca viva',
        'Propietarios rurales, Secretaría para el Desarrollo Económico y CAR', 'Perímetro de predios agropecuarios / 2 (linderos compartidos); meta del 10 % con una planta cada 3 m.', 'Mixto')

# ---------- 6. Calles de barrio en el casco urbano ----------
# Lógica: donde vive la gente es donde la sombra rinde más (salud, calor, caminata). La regla 3-30-300 pide
# que cada vivienda vea al menos tres árboles; en una cabecera de manzanas compactas eso solo se logra con
# árboles de calle. Por eso la cantidad se calcula con los metros de calle local de OpenStreetMap y no con
# el número de predios: un árbol cada 8 m por andén, en el 40 % de la longitud (el resto son garajes,
# esquinas, redes, andenes de menos de 1,2 m o fachadas sin retroceso). Las vías arterias quedan en los corredores V.
# La rejilla es de 0,002° (unos 222 x 221 m). Los cuadros se agrupan en sectores por el barrio de OpenStreetMap más cercano.
cs = defaultdict(list)
for l in open('insumos/osm_calles_urbanas_2026-11-16.txt', encoding='utf-8'):
    l = l.strip()
    if not l or l.startswith('#'): continue
    if l.startswith('@'): seccion = l[1:]; continue
    cs[seccion].append(l)
calle = {}
for reg in ' '.join(cs['calle']).split():
    i, j, v = map(int, reg.split(',')); calle[(i, j)] = v
barrios = [(n, float(x), float(y)) for n, x, y in (r.split('|') for r in cs['barrio'])]
urb_w = w(urb)
mercedes = [shape(f['geometry']).buffer(0) for f in load('datos/veredas_igac_2026.geojson')['features'] if f['properties']['n'] == 'MERCEDES DE CALAHORRA'][0]
pred = defaultdict(int)
for f in PRE:
    if f['properties']['u'] == 1 and f['properties']['d'] in ('h', 'c'):
        c = shape(f['geometry']).representative_point()
        pred[(math.floor(c.x * 500), math.floor(c.y * 500))] += 1
# Verde de referencia: parques de 0,5 ha o más y bosque. Los colegios y las plazas no cuentan porque en su mayoría
# están pavimentados; además, los parques mismos son zonas de siembra del plan.
verdes = m(unary_union([z['_g'] for z in zonas if z['tipo'] == 'parque' and z['_g'].area > 0] + [w(BOS)]))
celdas = []
for (i, j), metros in calle.items():
    cell4 = box(i / 500, j / 500, (i + 1) / 500, (j + 1) / 500)
    if cell4.intersection(urb_w.buffer(0.0005)).area < 0.25 * cell4.area: continue
    cm = m(cell4)
    vfrac = cm.intersection(verdes).area / cm.area
    dist = verdes.distance(cm.centroid)
    n = pred.get((i, j), 0)
    pr = 0.7 * min(n / 120, 1) + 0.3 * min(dist / 400, 1)
    c = cell4.centroid
    if mercedes.contains(c): sector = 'Mercedes de Calahorra'
    else:
        d, sector = min((math.hypot((c.x - x) * 110.9, (c.y - y) * 110.6), nb) for nb, x, y in barrios)
        if d > 0.7: sector = 'Cabecera ' + ('norte' if c.y > 4.872 else 'sur' if c.y < 4.852 else 'oriente' if c.x > -74.05 else 'occidente')
    celdas.append({'g': cell4, 'sector': sector, 'calle_m': metros, 'predios': n, 'verde': round(vfrac, 3), 'dist_verde_m': round(dist),
                   'prioridad': round(pr, 3), 'arboles': round(metros * 2 / 8 * 0.40)})
sect = defaultdict(list)
for c in celdas: sect[c['sector']].append(c)
info = []
for nb, cc in sect.items():
    arb = sum(c['arboles'] for c in cc)
    pr = sum(c['prioridad'] * c['arboles'] for c in cc) / max(arb, 1)
    info.append((pr, nb, cc, arb))
info.sort(key=lambda t: -t[0])
tot_u = sum(t[3] for t in info); acum = 0
for k, (pr, nb, cc, arb) in enumerate(info):
    etapa = 1 if pr >= 0.55 else 2          # prioridad alta: mucha gente y lejos del verde
    acum += arb
    for c in cc: c['etapa'] = etapa; c['codigo'] = f'U{k+1:02d}'
    geo = m(unary_union([c['g'] for c in cc]))
    add(f'U{k+1:02d}', f'Calles de barrio: {nb}', 'urbano', etapa, geo, arb, 'P3 vial', 'Municipio y juntas de acción comunal',
        f'{sum(c["calle_m"] for c in cc)/1000:.1f} km de calle local; un árbol cada 8 m por andén en el 40 % de la longitud. Prioridad {pr:.2f} de 1 '
        f'(70 % densidad de predios residenciales y comerciales, 30 % distancia al parque de 0,5 ha o más o al bosque).')

# ---------- salidas ----------
def r5(o):
    if isinstance(o, float): return round(o, 5)
    if isinstance(o, (list, tuple)): return [r5(x) for x in o]
    return o
feats = []
for z in zonas:
    g = mapping(z['_g'].simplify(0.00003))
    feats.append({'type': 'Feature', 'properties': {k2: v for k2, v in z.items() if k2 != '_g'}, 'geometry': {'type': g['type'], 'coordinates': r5(g['coordinates'])}})
json.dump({'type': 'FeatureCollection', 'features': feats}, open('planarborizacion/datos/zonas.geojson', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
json.dump({'type': 'FeatureCollection', 'features': [{'type': 'Feature', 'properties': {k2: v for k2, v in c.items() if k2 != 'g'}, 'geometry': {'type': 'Polygon', 'coordinates': r5(mapping(c['g'])['coordinates'])}} for c in celdas]},
          open('planarborizacion/datos/prioridad.geojson', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
# Tabla para personas: encabezados en español, sin envolvente, con enlace al mapa y diccionario de códigos.
# CSV en UTF-8 con BOM para que Excel reconozca las tildes; además un .xlsx, que no depende de la configuración regional.
TIPO_ES = {'ronda': 'Ronda de río o quebrada', 'vial': 'Corredor vial', 'parque': 'Parque o zona verde', 'escolar': 'Colegio o institución',
           'urbano': 'Calles de barrio', 'cerro': 'Núcleo de restauración en montaña', 'cerca': 'Cerca viva rural'}
PERIODO = {1: '2027–2028', 2: '2029–2031', 3: '2032–2035'}
CODIGOS = [('R', 'Ronda de río o quebrada: franja de 30 m por margen'), ('V', 'Corredor vial: árboles en andén o separador'),
           ('U', 'Calles de barrio del casco urbano'), ('P', 'Parque o zona verde'), ('E', 'Colegio, universidad u otra institución'),
           ('M', 'Montaña: núcleos de restauración junto al bosque de los cerros'), ('C-', 'Cerca viva en predios rurales de una vereda (C-FUS = Fusca)')]
CAB = ['Código', 'Nombre', 'Tipo', 'Etapa', 'Periodo de siembra', 'Vereda o sector', 'Latitud', 'Longitud', 'Ver en Google Maps',
       'Longitud (m)', 'Área (ha)', 'Árboles y arbustos', 'Especies principales', 'Especies intermedias', 'Restricciones y acompañantes', 'Cómo sembrar', 'Mezcla', 'Meses de siembra', 'Paleta', 'Costo estimado (COP 2027)', 'Financiación', 'Responsable', 'Supuesto']
def fila(z):
    return [z['id'], z['nombre'], TIPO_ES[z['tipo']], z['etapa'], PERIODO[z['etapa']], z['vereda'], z['lat'], z['lon'],
            f"https://www.google.com/maps/search/?api=1&query={z['lat']},{z['lon']}", z['longitud_m'] or '', z['area_ha'] or '',
            z['arboles'], RECETA[z['tipo']]['es']['principal'], RECETA[z['tipo']]['es']['intermedio'], RECETA[z['tipo']]['es']['acomp'], RECETA[z['tipo']]['es']['como'], RECETA[z['tipo']]['es']['mezcla'], MESES['es'], z['paleta'], z['costo_cop'], z['financia'], z['gestor'], z['nota']]
with open('planarborizacion/datos/zonas.csv', 'w', encoding='utf-8-sig', newline='') as fh:
    wr = csv.writer(fh); wr.writerow(CAB)
    for z in zonas: wr.writerow(fila(z))
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
wb = Workbook(); ws = wb.active; ws.title = 'Zonas'
ws.append(CAB)
for z in zonas:
    ws.append(fila(z)); r = ws.max_row
    ws.cell(r, 9).hyperlink = ws.cell(r, 9).value; ws.cell(r, 9).value = 'Abrir mapa'; ws.cell(r, 9).font = Font(color='1F5FAD', underline='single')
    ws.cell(r, 20).number_format = '#,##0'; ws.cell(r, 12).number_format = '#,##0'
for c in ws[1]: c.font = Font(bold=True, color='FFFFFF'); c.fill = PatternFill('solid', fgColor='2E5E3E'); c.alignment = Alignment(wrap_text=True, vertical='top')
for col, wd in zip('ABCDEFGHIJKLMNOPQRSTUVW', (8, 46, 26, 7, 12, 22, 10, 10, 12, 11, 9, 11, 45, 45, 40, 60, 28, 40, 14, 16, 16, 30, 60)): ws.column_dimensions[col].width = wd
for row in ws.iter_rows(min_row=2):
    for c in row: c.alignment = Alignment(wrap_text=True, vertical='top')
ws.freeze_panes = 'C2'; ws.auto_filter.ref = ws.dimensions
wc = wb.create_sheet('Códigos')
wc.append(['Prefijo', 'Significado']); [setattr(c, 'font', Font(bold=True)) for c in wc[1]]
for k in CODIGOS: wc.append(list(k))
wc.append([]); wc.append(['Etapa', 'Periodo'])
for e, p_ in PERIODO.items(): wc.append([e, p_])
wc.append([]); wc.append(['Límites', LIMITES['es']])
wc.append([]); wc.append(['Nota', 'Cantidades potenciales de planeación. Cada sitio requiere visita técnica, verificación de redes y propiedad, y concepto de la CAR antes de sembrar.'])
wc.column_dimensions['A'].width = 10; wc.column_dimensions['B'].width = 90
wb.save('planarborizacion/datos/zonas_arborizacion_chia.xlsx')
json.dump({'recetas': RECETA, 'meses': MESES, 'limites': LIMITES}, open('planarborizacion/datos/recetas.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
res = {'por_tipo': defaultdict(lambda: [0, 0, 0]), 'por_etapa': defaultdict(lambda: [0, 0, 0]), 'por_financia': defaultdict(lambda: [0, 0, 0])}
for z in zonas:
    for key, kk in (('por_tipo', z['tipo']), ('por_etapa', z['etapa']), ('por_financia', z['financia'])):
        res[key][kk][0] += 1; res[key][kk][1] += z['arboles']; res[key][kk][2] += z['costo_cop']
res = {k2: dict(v) for k2, v in res.items()}
res['total'] = [len(zonas), sum(z['arboles'] for z in zonas), sum(z['costo_cop'] for z in zonas)]
res['area_chia_km2'] = round(CH.area / 1e6, 2)
res['bosque_igac_ha'] = round(BOS.intersection(CH).area / 1e4)
res['celdas'] = [len(celdas), len(info)]
json.dump(res, open('planarborizacion/datos/resumen.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False, indent=1))
for z in zonas: print(z['id'], z['tipo'], z['etapa'], z['vereda'], z['lat'], z['lon'], z['longitud_m'], z['area_ha'], z['arboles'], f"{z['costo_cop']:,}", z['nombre'][:60])

# ---------- presupuesto del programa ----------
# Todos los valores en pesos de 2027 con IVA. Supuestos explícitos en el documento (sección 7).
obra = defaultdict(lambda: defaultdict(int))
for z in zonas: obra[z['etapa']][z['financia']] += z['costo_cop']
cuota = {'Público': 1.0, 'Mixto': 0.5, 'Gestión con el titular de la vía': 0.0, 'Privado': 0.0}
P = {'etapa0': {'Censo georreferenciado del arbolado urbano público (unos 25.000 individuos a $7.500, referencia JBB 2026)': 187_500_000,
                'Línea base satelital: temperatura de superficie (Landsat), altura de dosel (CHMv2), modelo de superficie (GEM-15) y mapa de sitios sembrables': 120_000_000,
                'Manual municipal de silvicultura urbana y paleta de especies, con revisión de la CAR': 150_000_000,
                'Delimitación y convocatoria de Áreas de Vida (Ley 2173 de 2021, Resolución 1491 de 2025)': 60_000_000,
                'Estudios de diseño paisajístico de los corredores y sectores de barrio de la etapa 1': 180_000_000,
                'Socialización, mesas veredales y diálogo con el Resguardo Indígena de Fonquetá y Cerca de Piedra': 60_000_000},
     'transversal_anual': {'Monitoreo de supervivencia, plataforma de datos abiertos y reporte anual': 80_000_000,
                           'Programa comunitario «Guardianes del árbol», PRAE escolares y adopción de árboles': 100_000_000},
     'vivero_fortalecimiento': 350_000_000, 'anios': 9, 'interventoria': 0.08, 'contingencia': 0.05}
etapas = {}
for e in (1, 2, 3):
    tot = sum(obra[e].values()); mun = sum(v * cuota[f] for f, v in obra[e].items())
    etapas[e] = {'obra_total': tot, 'obra_municipio': round(mun), 'por_financia': dict(obra[e])}
mun_obra = sum(v['obra_municipio'] for v in etapas.values())
e0 = sum(P['etapa0'].values()); trans = sum(P['transversal_anual'].values()) * P['anios']
inter = mun_obra * P['interventoria']; base = mun_obra + e0 + trans + P['vivero_fortalecimiento'] + inter
cont = base * P['contingencia']
res['presupuesto'] = {'supuestos': P, 'etapas': etapas, 'etapa0': e0, 'transversal_total': trans, 'interventoria': round(inter),
                      'contingencia': round(cont), 'municipio_total': round(base + cont), 'programa_total_todas_las_fuentes': round(sum(z['costo_cop'] for z in zonas) + e0 + trans + P['vivero_fortalecimiento'] + inter + cont),
                      'municipio_anual_promedio': round((base + cont) / P['anios'])}
json.dump(res, open('planarborizacion/datos/resumen.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(res['presupuesto'], ensure_ascii=False, indent=1))
