"""11. Figuras estáticas del plan de arborización (español e inglés), para el documento y su PDF.
Uso: python procesamiento/11_figuras_arborizacion.py   (después del paso 10)
Produce planarborizacion/fig/*.png
"""
import json, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from shapely.geometry import shape

os.makedirs('planarborizacion/fig', exist_ok=True)
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9, 'axes.edgecolor': '#8a8f8b', 'axes.labelcolor': '#1b2420',
                     'xtick.color': '#56615b', 'ytick.color': '#56615b', 'axes.spines.top': False, 'axes.spines.right': False})
COL = {'ronda': '#2a78d6', 'vial': '#eb6834', 'parque': '#1baf7a', 'cerca': '#eda100', 'urbano': '#e87ba4', 'cerro': '#008300', 'escolar': '#6250d6'}
NOM = {'es': {'ronda': 'Rondas de ríos y quebradas', 'cerro': 'Núcleos de restauración en ladera', 'vial': 'Corredores viales', 'parque': 'Parques y zonas verdes',
              'escolar': 'Colegios e instituciones', 'urbano': 'Calles de sombra', 'cerca': 'Cercas vivas rurales'},
       'en': {'ronda': 'River and stream buffers', 'cerro': 'Hillside restoration nuclei', 'vial': 'Road corridors', 'parque': 'Parks and green areas',
              'escolar': 'Schools and institutions', 'urbano': 'Shade streets', 'cerca': 'Rural living fences'}}
Z = json.load(open('planarborizacion/datos/zonas.geojson', encoding='utf-8'))['features']
R = json.load(open('planarborizacion/datos/resumen.json', encoding='utf-8'))
lim = [shape(f['geometry']) for f in json.load(open('datos/limites_municipios.geojson'))['features'] if f['properties']['c'] == 25175][0]
bos = [shape(f['geometry']) for f in json.load(open('datos/bosque_igac.geojson'))['features']]
agua = [f for f in json.load(open('datos/agua_igac.geojson'))['features'] if f['properties']['t'] == 'q']
ver = json.load(open('datos/veredas_igac_2026.geojson'))['features']

def poly(ax, g, **kw):
    for p in (g.geoms if g.geom_type == 'MultiPolygon' else [g]):
        x, y = p.exterior.xy; ax.fill(x, y, **kw)

for L in ('es', 'en'):
    # Figura 1: mapa de zonas
    fig, ax = plt.subplots(figsize=(7.2, 7.6), dpi=200)
    poly(ax, lim, facecolor='#f4f2ea', edgecolor='#56615b', linewidth=0.8)
    for f in ver:
        g = shape(f['geometry'])
        for p in (g.geoms if g.geom_type == 'MultiPolygon' else [g]):
            x, y = p.exterior.xy; ax.plot(x, y, color='#c9c4b5', lw=0.4)
    for b in bos: poly(ax, b, facecolor='#cfe0c8', edgecolor='none')
    for f in agua:
        g = shape(f['geometry'])
        for l in (g.geoms if g.geom_type == 'MultiLineString' else [g]):
            x, y = l.xy; ax.plot(x, y, color='#7fa7c9', lw=0.7)
    orden = ['cerca', 'cerro', 'ronda', 'parque', 'escolar', 'urbano', 'vial']
    for t in orden:
        for f in Z:
            if f['properties']['tipo'] != t: continue
            g = shape(f['geometry'])
            if g.geom_type in ('LineString', 'MultiLineString'):
                for l in (g.geoms if g.geom_type == 'MultiLineString' else [g]):
                    x, y = l.xy; ax.plot(x, y, color=COL[t], lw=2.0, solid_capstyle='round')
            else:
                poly(ax, g, facecolor=COL[t], edgecolor='white', linewidth=0.3, alpha=0.30 if t in ('cerca', 'cerro') else 0.85)
    for f in Z:
        p = f['properties']
        if p['tipo'] in ('vial',) or p['id'] in ('R04', 'R05', 'R06', 'R02', 'R01'):
            ax.annotate(p['id'], (p['lon'], p['lat']), fontsize=6.5, color='#1b2420', ha='center', va='center',
                        bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.8))
    hs = [plt.Line2D([0], [0], color=COL[t], lw=6 if t != 'vial' else 2.5, alpha=0.9) for t in orden[::-1]]
    ax.legend(hs, [NOM[L][t] for t in orden[::-1]], loc='upper center', bbox_to_anchor=(0.5, -0.08), ncol=3, fontsize=7, frameon=False)
    ax.set_xlim(-74.1, -73.978); ax.set_ylim(4.815, 4.922)
    ax.set_aspect(1 / 0.9965); ax.set_xlabel('Longitud (°)' if L == 'es' else 'Longitude (°)'); ax.set_ylabel('Latitud (°)' if L == 'es' else 'Latitude (°)')
    ax.tick_params(labelsize=7)
    ax.set_title('Zonas estratégicas de siembra, Chía' if L == 'es' else 'Strategic planting zones, Chía', fontsize=10, loc='left')
    fig.tight_layout(); fig.savefig(f'planarborizacion/fig/mapa_zonas_{L}.png'); plt.close(fig)

    # Figura 2: clima, dos paneles con su propio eje (no doble eje)
    mes = ['E', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'] if L == 'es' else ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
    tavg = [13.4, 13.8, 14.2, 14.3, 14.4, 13.8, 13.5, 13.3, 13.4, 13.7, 14.0, 13.8]
    tmin = [0.8, 0.8, 5.1, 3.9, 5.5, 5.6, 4.9, 3.2, 3.6, 4.7, 3.3, 2.9]
    tmax = [25.6, 26.0, 25.4, 24.1, 22.2, 22.3, 21.6, 22.5, 23.6, 24.4, 23.8, 24.0]
    pp = {2020: [17.4, 104, 71, 66.2, 36.6, 45.4, 55, 26.2, 43.2, 31.6, 157.2, 15], 2021: [1.2, 25.4, 70.6, 53.8, 43.6, 66, 37.2, 71, 28.6, 98.4, 26.2, 15.4]}
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 2.8), dpi=200)
    x = range(12)
    a1.fill_between(x, tmin, tmax, color='#2a78d6', alpha=0.13, lw=0)
    a1.plot(x, tavg, color='#2a78d6', lw=2); a1.plot(x, tmin, color='#2a78d6', lw=1, ls='--')
    a1.axhline(0, color='#b5541c', lw=0.8); a1.set_xticks(list(x)); a1.set_xticklabels(mes)
    a1.set_ylabel('°C'); a1.set_ylim(-1, 27)
    a1.set_title('Temperatura del aire por mes' if L == 'es' else 'Monthly air temperature', fontsize=9, loc='left')
    a1.text(0.2, 1.6, 'mín. 0,8' if L == 'es' else 'min. 0.8', fontsize=7, color='#b5541c')
    a1.text(5.5, 15.2, 'media' if L == 'es' else 'mean', fontsize=7, color='#2a78d6')
    w = 0.38
    a2.bar([i - w / 2 for i in x], pp[2020], width=w, color='#2a78d6', label='2020')
    a2.bar([i + w / 2 for i in x], pp[2021], width=w, color='#eb6834', label='2021')
    a2.set_xticks(list(x)); a2.set_xticklabels(mes); a2.set_ylabel('mm')
    a2.set_title('Lluvia mensual' if L == 'es' else 'Monthly rainfall', fontsize=9, loc='left'); a2.legend(fontsize=7, frameon=False)
    fig.tight_layout(); fig.savefig(f'planarborizacion/fig/clima_{L}.png'); plt.close(fig)

    # Figura 3: costo por etapa y fuente
    fu = ['Público', 'Mixto', 'Gestión con el titular de la vía', 'Privado']
    fn = {'es': ['Municipio', 'Mixto (municipio, CAR, empresas, propietarios)', 'Titular de la vía nacional o departamental', 'Privado voluntario'],
          'en': ['Municipality', 'Mixed (municipality, CAR, companies, owners)', 'Road authority (national or departmental)', 'Voluntary private']}
    fc = ['#2a78d6', '#1baf7a', '#eb6834', '#e87ba4']
    fig, ax = plt.subplots(figsize=(7.2, 2.6), dpi=200)
    et = ['1', '2', '3']
    left = [0, 0, 0]
    for k, f in enumerate(fu):
        vals = [R['presupuesto']['etapas'][e]['por_financia'].get(f, 0) / 1e9 for e in et]
        ax.barh(et, vals, left=left, color=fc[k], label=fn[L][k], edgecolor='white', linewidth=1.5, height=0.55)
        left = [l + v for l, v in zip(left, vals)]
    for i, v in enumerate(left): ax.text(v + 0.08, i, f'{v:,.1f}'.replace('.', ',') if L == 'es' else f'{v:,.1f}', va='center', fontsize=7.5)
    ax.set_yticks(range(3)); ax.set_yticklabels(['Etapa 1', 'Etapa 2', 'Etapa 3'] if L == 'es' else ['Stage 1', 'Stage 2', 'Stage 3'])
    ax.invert_yaxis(); ax.set_xlabel('Miles de millones de pesos de 2027' if L == 'es' else 'Billions of 2027 Colombian pesos (thousand millions)')
    ax.legend(fontsize=6.5, frameon=False, loc='lower right'); ax.grid(axis='x', color='#e6e3d9', lw=0.6); ax.set_axisbelow(True)
    fig.tight_layout(); fig.savefig(f'planarborizacion/fig/costo_etapas_{L}.png'); plt.close(fig)
print('ok')
