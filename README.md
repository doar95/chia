# Chía, memoria y porvenir

Portal interactivo sobre la historia, la gente, las finanzas, el suelo, el agua, los planes y la geografía del municipio de Chía, Cundinamarca, conocido como la Ciudad de la Luna. Está construido con documentos y datos oficiales.

**Sitio:** https://doar95.github.io/chia/

## Para quien llega por primera vez

El portal es un solo mapa con siete capítulos y una barra de tiempo que va de la época muisca a 2026. Cada capítulo empieza con una explicación corta de qué muestra, y hay un glosario para los términos técnicos. Está en español, inglés, portugués, francés, chino mandarín y árabe. La versión validada es la española.

Cada dato lleva su fuente con una etiqueta: Oficial, Judicial, Académica o Prensa. La prensa solo se usa para hechos oficiales recientes cuyo documento original aún no se ubicó, y esos hitos se marcan como provisionales.

## Cómo reproducirlo

Todo lo que se ve en el portal sale de los programas de la carpeta `procesamiento/`, que se corren en orden desde la raíz del repositorio.

```
pip install -r procesamiento/requisitos.txt
python procesamiento/01_base.py --incendios ../incendios-colombia --carga ../carga-tributaria-ciudades
python procesamiento/02_catastro_2018.py        # requiere insumos privados, ver abajo
python procesamiento/03_predios_y_rejilla.py    # requiere el resultado privado del paso 02
python procesamiento/04_agua_bosque_cerros.py
python procesamiento/05_osm.py
python procesamiento/09_empaqueta.py
```

El 14 de noviembre de 2026 se corrió esta cadena completa en una copia limpia y produjo archivos idénticos a los publicados.

| Paso | Qué hace | Insumos | Se puede repetir sin permisos |
| --- | --- | --- | --- |
| 01 | Límites, veredas, población, pirámide, hacienda | Repositorios públicos `incendios-colombia` y `carga-tributaria-ciudades` | Sí |
| 02 | Agregados del catastro de 2018 | Listados prediales del IGAC con datos personales | No. Hay que pedir los listados al IGAC |
| 03 | Predios de 2026 con destino y rejilla de avalúo | `insumos/catastro_igac_2026_chia.txt` y el resultado privado del paso 02 | Parcial |
| 04 | Agua, bosque y cerros | `insumos/cartografia_igac_25000_chia.txt` | Sí |
| 05 | Cultivos, invernaderos y quebradas menores | `insumos/osm_chia_2026-11-14.txt` | Sí |
| 09 | Empaqueta `datos/datos.js` | Resultados de 01 y 02 | Sí |

## Documentación

| Documento | Contenido |
| --- | --- |
| [docs/METODO.md](docs/METODO.md) | Decisiones de método y sus límites |
| [docs/INDICADORES.md](docs/INDICADORES.md) | Ficha de cada indicador: qué mide, fórmula, fuente y qué no se debe concluir |
| [docs/INSUMOS.md](docs/INSUMOS.md) | De dónde salió cada insumo, con dirección, fecha y consulta |
| [docs/DICCIONARIO.md](docs/DICCIONARIO.md) | Variables de cada archivo de datos |
| [docs/CAMBIOS.md](docs/CAMBIOS.md) | Registro de cambios y correcciones |
| [docs/LICENCIAS.md](docs/LICENCIAS.md) | Condiciones de uso del código y de cada fuente |

## Datos abiertos

Están en `datos/`. Los CSV usan coma como separador y UTF-8. Los mapas están en GeoJSON con coordenadas geográficas WGS84.

| Archivo | Contenido |
| --- | --- |
| `poblacion.csv` | Población total y de cabecera de 19 municipios, 1985 a 2025 |
| `piramide_2005_2017.csv` | Población de Chía por sexo y grupos de cinco años |
| `hacienda.csv` | Ingresos y gastos de Chía, 1984 a 2025 |
| `catastro_zona_2018.csv` | Avalúo catastral por vereda y zona urbana |
| `catastro_manzana_2018.csv` | Avalúo catastral por manzana o sector con cinco o más predios |
| `limites_municipios.geojson` | Límites aproximados de 19 municipios |
| `veredas_dane_2024.geojson` | Veredas de Chía según el DANE |
| `veredas_igac_2026.geojson` | Veredas y perímetros urbanos de Chía según el catastro del IGAC |
| `predios_2026.geojson` | 32.322 predios con destino económico agrupado, sin códigos ni propietarios |
| `avaluo_rejilla_2018.geojson` | Mediana de avalúo por metro cuadrado en celdas de unos 150 metros |
| `agua_igac.geojson`, `bosque_igac.geojson` | Cuerpos de agua, drenajes y bosque del IGAC |
| `cultivos_osm.geojson` | Cultivos e invernaderos de OpenStreetMap, no oficial |

No se publican nombres, documentos, direcciones ni valores de predios individuales.

## Autoría

Elaborado por el titular de este repositorio con asistencia de inteligencia artificial, Claude de Anthropic, que redactó textos, programas y traducciones bajo su dirección. Las traducciones no tienen revisión de hablantes nativos. Los errores se pueden reportar en la pestaña Issues de este repositorio.

## Tecnología

Sitio estático sin compilación. MapLibre GL JS y maplibre-contour están en `vendor/`. El relieve se carga de AWS Terrain Tiles y la pérdida de bosque de los servidores de Global Forest Change. Si no están disponibles, el resto del mapa funciona igual.
