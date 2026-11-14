# Chía, memoria y porvenir

Portal interactivo sobre la historia y los planes del municipio de Chía, Cundinamarca, construido con documentos oficiales. Sitio publicado en https://doar95.github.io/chia/

## Qué contiene

Un solo mapa con un control de tiempo que va de la época muisca a 2026 y siete capítulos.

1. **Historia.** Dieciséis hitos, desde el cacicazgo de Chía hasta las decisiones judiciales de 2026.
2. **Gente.** Población anual del DANE de 1985 a 2025, censos de 1951 a 2018, estructura por edad y sexo y comparación con Sabana Centro y Sabana Occidente.
3. **Hacienda.** Recaudo por impuesto de 1984 a 2025 en pesos constantes, gasto e inversión.
4. **Suelo.** Predios por tamaño de 2010 a 2019, estructura predial por vereda y densidad predial, según el diagnóstico del POT de 2020.
5. **Agua.** Río Frío, PTAR Chía I y II, Sentencia del río Bogotá y Chucua de Fagua.
7. **Geografía.** Altitud, curvas de nivel, cuerpos de agua y bosque, predios del catastro de 2026 por destino económico y avalúo catastral de 2018 en celdas de 150 metros.
6. **Planes y obras.** POT de 2000 y de 2016 y su trámite judicial, Troncal de los Andes, Autopista Norte, conexiones por el occidente y territorio del resguardo muisca.

Incluye un recorrido automático de 30 segundos con pausa y repetición, y versiones en español, inglés, portugués, francés, chino mandarín y árabe. La versión validada es la española. Las demás son traducciones de apoyo pendientes de revisión por hablantes nativos.

## Criterio de fuentes

Cada dato lleva su fuente y una etiqueta de tipo.

| Etiqueta | Qué es |
| --- | --- |
| Oficial | Actos administrativos, estadísticas y publicaciones de entidades públicas |
| Judicial | Providencias de juzgados, tribunales y altas cortes |
| Académica | Estudios de universidades públicas |
| Prensa | Solo para hechos oficiales recientes cuyo documento original aún no se ubicó |

No se incluyen datos de Bogotá. Los demás municipios de Sabana Centro y Sabana Occidente aparecen como contexto regional.

## Datos

| Archivo | Contenido | Fuente |
| --- | --- | --- |
| `datos/datos.js` | Límites, veredas, población, pirámide y hacienda que usa el mapa | DANE y DNP |
| `datos/poblacion.csv` | Población total y de cabecera, 19 municipios, 1985 a 2025 | DANE, proyecciones y retroproyecciones |
| `datos/catastro_zona_2018.csv` | Avalúo catastral por vereda y zona urbana, 2018 | IGAC, registros 1 y 2 |
| `datos/catastro_manzana_2018.csv` | Avalúo catastral por manzana o sector con cinco o más predios, 2018 | IGAC, registros 1 y 2 |
| `datos/predios_2026.geojson` | 32.322 polígonos prediales con destino económico agrupado, sin códigos ni propietarios | IGAC, Base Catastral Pública, septiembre de 2026, cruzada con registros de 2018 |
| `datos/avaluo_rejilla_2018.geojson` | Mediana del avalúo catastral por metro cuadrado en celdas de unos 150 metros con cinco o más predios | IGAC, registros 1 y 2 de 2018 |
| `datos/geografia_osm.js` | Cultivos, invernaderos, quebradas menores y canales, como complemento no oficial | OpenStreetMap, licencia ODbL |
| `datos/geografia.js` | Cuerpos de agua, drenajes y bosque | IGAC, cartografía básica 1:25.000 |
| `datos/hacienda.csv` | Ingresos y gastos de Chía, 1984 a 2025 | DNP, ejecuciones presupuestales y Operaciones Efectivas de Caja |

Los límites municipales se construyen uniendo las veredas de la capa de referencia DANE 2024 y asignando a cada municipio su cabecera. El área resultante para Chía es de 80,5 kilómetros cuadrados, frente a 80,44 que reporta la Alcaldía. Los límites de los demás municipios son aproximados y sirven solo como contexto.

La serie fiscal proviene del panel del repositorio [carga-tributaria-ciudades](https://github.com/doar95/carga-tributaria-ciudades).

Los archivos de catastro son agregados. No se publican nombres, documentos, direcciones ni registros de predios individuales.

## Pendientes

- Zonificación y usos del suelo predio a predio de los Acuerdos 17 de 2000 y 100 de 2016
- Cerro del Majuy y cerros orientales, figuras de protección y nacimientos
- Lluvia, calidad del agua y del aire con series del IDEAM y la CAR
- Cobertura y capacidad de acueducto, alcantarillado y aseo
- Colegios oficiales, matrícula y nuevas sedes
- Saldo de deuda pública e indicadores de la Ley 358
- Patrimonio inmueble, turismo y topónimos muiscas con el corpus de cubun.org
- Valor del suelo por metro cuadrado según catastro
- Trazado oficial de vías y proyectos viales
- Coberturas de la tierra oficiales del IDEAM

## Tecnología

Sitio estático sin proceso de compilación. MapLibre GL JS y maplibre-contour incluidos en `vendor/`. El relieve proviene de AWS Terrain Tiles y se carga desde internet. Si no está disponible, el mapa funciona igual con los límites del DANE.

## Licencia

Código bajo licencia MIT. Los datos conservan las condiciones de uso de sus fuentes oficiales.
