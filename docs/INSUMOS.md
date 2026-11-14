# Insumos

Fecha de consulta de todos los servicios en línea: 14 de noviembre de 2026, salvo que se indique otra.

## Repositorios públicos del mismo autor

| Insumo | Dónde está | Origen |
| --- | --- | --- |
| Veredas de Cundinamarca y Bogotá | `doar95/incendios-colombia`, archivos `datos/d_25.json` y `datos/d_11.json` | DANE, capa de referencia de veredas de 2024 |
| Población municipal 1985 a 2025 | `doar95/carga-tributaria-ciudades`, `data/intermedios/poblacionMunicipal1985a2025.csv` | DANE, proyecciones y retroproyecciones |
| Población por sexo y edad 2005 a 2017 | `doar95/carga-tributaria-ciudades`, `insumos/pob_2005_2017_sexoedad.xlsx` | DANE |
| Panel fiscal 1984 a 2025 | `doar95/carga-tributaria-ciudades`, `data/panelCargaTributaria1984a2025.csv` | DNP, ejecuciones presupuestales y Operaciones Efectivas de Caja |

## Base Catastral Pública del IGAC

- Archivo: `insumos/catastro_igac_2026_chia.txt`
- Servicio: `https://services2.arcgis.com/RVvWzU3lgJISqdke/arcgis/rest/services/CATASTRO_PUBLICO_31092026/FeatureServer`
- Capas: 7 terreno urbano, 14 terreno rural, 5 manzana, 15 vereda, 8 sector urbano, 2 perímetro urbano
- Filtro: `codigo_municipio='25175'`
- Parámetros: `outSR=4326`, `geometryPrecision=5`, `maxAllowableOffset` entre 0,00002 y 0,00005 grados, páginas de 2.000 registros ordenadas por `OBJECTID`
- Formato del archivo: secciones que empiezan por `@@`. Cada línea trae los campos separados por `|` y al final la geometría. Las coordenadas son enteros de cien milésimas de grado. El primer punto de cada anillo es relativo al origen longitud -75, latitud 0, y los siguientes son diferencias con el punto anterior. Los anillos se separan con `;`.
- El IGAC publica una versión nueva cada mes. Para repetir con otro corte hay que cambiar el nombre del servicio.

## Cartografía básica del IGAC, escala 1:25.000

- Archivo: `insumos/cartografia_igac_25000_chia.txt`
- Servicio: cartografía vectorial 1:25.000 del IGAC, publicada en `mapas.igac.gov.co` y `mapas2.igac.gov.co`, carpeta `carto`, servicio `carto25000colombia2017`
- Recorte: rectángulo alrededor de Chía
- Secciones usadas por el programa 04: 7 orografía, 22 drenaje sencillo, 32 drenaje doble, 34 y 42 lagunas y otros cuerpos de agua, 43 bosque
- Mismo formato de coordenadas que el archivo catastral
- **Advertencia:** el fragmento exacto de la consulta con que se armó este archivo no se conservó. El archivo sí está completo en el repositorio, así que el paso 04 se puede repetir, pero para regenerar el archivo desde el servicio hay que verificar los números de capa, que cambian entre servidores.

## OpenStreetMap

- Archivo: `insumos/osm_chia_2026-11-14.txt`
- Servicio: Overpass API, `https://overpass-api.de/api/interpreter`
- Consulta, sobre el rectángulo sur 4,785, oeste -74,115, norte 4,935, este -73,975:

```
[out:json][timeout:25];
(way["waterway"](4.785,-74.115,4.935,-73.975);
 way["landuse"~"forest|farmland|orchard|greenhouse_horticulture|meadow"](4.785,-74.115,4.935,-73.975););
out geom;
```

- Se conservan cultivos (`farmland`, `orchard`), invernaderos (`greenhouse_horticulture`) y cursos de agua.
- OpenStreetMap cambia a diario. El archivo es la foto de ese día.

## Listados prediales del IGAC de 2018

No están en el repositorio porque contienen datos personales. Son los listados "Registro 1 y 2" del municipio 25175, con fecha de corte 28 de mayo de 2018, que el IGAC entrega por solicitud. Quien quiera repetir el paso 02 debe pedirlos al IGAC o al gestor catastral y ponerlos en la carpeta `privado/` con los nombres que indica el programa.

## Teselas que el portal carga en línea

| Capa | Dirección | Nota |
| --- | --- | --- |
| Relieve y altitud | `https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png` | Terrain Tiles en AWS Open Data |
| Pérdida de bosque | `https://storage.googleapis.com/earthenginepartners-hansen/tiles/gfc_v1.11/loss_alpha/{z}/{x}/{y}.png` | Global Forest Change 1.11 |

## Documentos

Las direcciones de todos los documentos citados están en el botón Fuentes y método del portal y en el objeto `F` de `app.js`.
