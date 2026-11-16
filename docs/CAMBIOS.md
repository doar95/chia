# Registro de cambios

Las fechas son de 2026.

## 16 de noviembre, plan de arborización, versión 1.1
- El documento abre con un resumen de dos páginas: qué se propone, dónde, qué va primero, cuánto cuesta, cómo se cuida la plata y qué se pide. El documento técnico viene después.
- **Corrección.** El casco urbano estaba subestimado: tenía 1.098 árboles calculados por número de predios en 20 cuadros. Ahora se calcula con los metros de calle local de OpenStreetMap (un árbol cada 8 m por andén en el 40 % de la longitud) y suma 9.241 árboles en 27 sectores con nombre de barrio, 14 de ellos en la etapa 1.
- **Corrección.** El índice de prioridad contaba colegios y plazas como verde. Ahora solo cuentan los parques de 0,5 ha o más y el bosque; pondera 70 % densidad de predios y 30 % distancia al verde.
- Códigos legibles: U calles de barrio, V vías, P parques, E colegios, R rondas, M montaña, C- cercas vivas.
- El mapa abre con una explicación, muestra el código de cada zona con su nombre al pasar el puntero y permite colorear por tipo o por etapa. La rejilla técnica sale de la vista y queda como dato descargable.
- **Corrección.** La tabla CSV se veía con caracteres rotos en Excel. Ahora va en UTF-8 con BOM, con encabezados en español y sin la columna de envolvente, y se agrega una versión .xlsx con hoja de códigos. Nueva página de datos.
- Nueva figura del casco urbano. El total pasa a 117 zonas y 138.577 plantas; el costo municipal, a $15.435 millones en nueve años.

## 15 de noviembre
- La fuente fiscal se cita como Operaciones Efectivas de Caja, OEC, del DNP.

## 14 de noviembre
- Nuevo diseño de pantalla: los capítulos pasan a una barra grande sobre el mapa, con Geografía en segundo lugar. Las capas del mapa salen del panel a un recuadro propio y se pueden prender en cualquier capítulo. El panel es más ancho y se puede ampliar.
- Tema claro por defecto y tema oscuro como opción.
- Guía al inicio de cada capítulo, glosario y marca de dato provisional en los hitos verificados solo en prensa.
- Se publican los programas de procesamiento, los insumos públicos, las fichas de indicadores, el diccionario y este registro. La cadena completa se corrió en limpio y reprodujo los archivos publicados.
- **Corrección.** La frase del resumen "la población se multiplicó por dieciocho" mezclaba un censo con una estimación. Ahora dice de dónde sale cada cifra.
- **Corrección.** Se aclara que la coincidencia entre el aumento del predial de 2025 y la actualización catastral no prueba la causa, y que las explicaciones de los impuestos son generales.
- **Corrección.** La fuente de los registros catastrales de 2018 se cita como IGAC, que es su origen.
- Versión en inglés, botón de descargas, capítulo de Hacienda ampliado y texto más grande. El resumen de 30 segundos ya no arranca solo.
- Se añade que Chía significa luna en lengua chibcha, con la guía de turismo de la Alcaldía como fuente.
- Capítulo de Geografía con altitud, curvas de nivel, agua, bosque, cultivos, pérdida de bosque, predios del IGAC de 2026 y rejilla de avalúo de 2018.

## 10 de noviembre
- **Corrección.** El texto sobre el resguardo de Fonquetá y Cerca de Piedra decía "reconocido en 2013". Se cambió para reflejar que la comunidad poseía la tierra desde antes y que el Acuerdo 315 de 2013 tituló el predio.
- **Corrección.** Se quitó un mapa de fondo que mostraba una marca de agua y se corrigió el límite de Chía, que no incluía la cabecera.
- Catastro de 2018 agregado por zona y manzana. Capítulo Suelo con la estructura predial del diagnóstico del POT de 2020.
- Primera versión: historia, gente, hacienda, agua, planes y obras, en cinco idiomas.

## 16 de noviembre de 2026: plan de arborización

- Nueva sección `planarborizacion/`: documento técnico en español e inglés (con PDF), mapa interactivo de 110 zonas con coordenadas y datos abiertos (`zonas.geojson`, `zonas.csv`, `prioridad.geojson`, `resumen.json`).
- Nuevos programas `procesamiento/10_arborizacion.py` (zonas, cantidades, costos) y `11_figuras_arborizacion.py` (figuras).
- Nuevo insumo `insumos/osm_arborizacion_2026-11-16.txt` con vías, parques y colegios de OpenStreetMap.
- Botón de acceso al plan en la cabecera del portal.
