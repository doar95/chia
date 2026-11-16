"""Recetas de siembra por tipo de zona: qué especies, en qué proporción, cómo y cuándo.
Las especies salen de la paleta del documento (sección 8, 41 nativas de la Sabana y del bosque altoandino).
Criterios de distancia y tamaño: propuesta de diseño para el manual municipal de silvicultura urbana (etapa 0);
deben validarse con la Secretaría de Medio Ambiente, la CAR y las empresas de servicios antes de contratar.
Uso: lo importa 10_arborizacion.py y escribe planarborizacion/datos/recetas.json."""

MESES = {'es': 'Siembra en las dos temporadas de lluvia: abril–mayo y mediados de octubre–noviembre. No sembrar entre diciembre y febrero (seca y heladas) ni en julio–agosto sin riego.',
         'en': 'Plant in the two rainy seasons: April–May and mid-October–November. Do not plant December–February (dry season and frost) or July–August without irrigation.'}

R = {
 'urbano': {
  'es': {
   'principal': 'Arrayán (Myrcianthes leucoxyla), Cerezo de monte (Prunus buxifolia), Cajeto (Citharexylum subflavescens) solo en andén de 2 m o más',
   'intermedio': 'Chicalá (Tecoma stans), Siete cueros (Andesanthus lepidotus), Tíbar (Escallonia pendula), Sangregado (Croton bogotanus), Mano de oso (Oreopanax floribundus)',
   'acomp': 'Bajo redes eléctricas: solo especies de menos de 8 m (chicalá, siete cueros, tíbar, sangregado).',
   'corto': 'Arrayán, cerezo de monte, chicalá, siete cueros, tíbar, sangregado, mano de oso',
   'como': 'Árbol de 2 m o más en bolsa de 20 L; alcorque de 1 × 1 m; un árbol cada 8 m, alternando 3 o 4 especies por cuadra. Dejar 1,2 m de andén libre, 5 m a esquinas y semáforos y 2 m a postes, cajas y acometidas. Tutor triple y protector. Andén de menos de 1,2 m: no se siembra en el andén; se ofrece el antejardín al propietario.',
   'mezcla': 'Ninguna especie más del 30 % de un sector.'},
  'en': {
   'principal': 'Arrayán (Myrcianthes leucoxyla), mountain cherry (Prunus buxifolia), cajeto (Citharexylum subflavescens) only on pavements 2 m or wider',
   'intermedio': 'Chicalá (Tecoma stans), siete cueros (Andesanthus lepidotus), tíbar (Escallonia pendula), sangregado (Croton bogotanus), mano de oso (Oreopanax floribundus)',
   'acomp': 'Under power lines: only species under 8 m (chicalá, siete cueros, tíbar, sangregado).',
   'corto': 'Arrayán, mountain cherry, chicalá, siete cueros, tíbar, sangregado, mano de oso',
   'como': 'Tree 2 m or taller in a 20 L bag; 1 × 1 m tree pit; one tree every 8 m, alternating 3 or 4 species per block. Keep 1.2 m of clear pavement, 5 m from corners and traffic lights and 2 m from poles, utility boxes and connections. Triple stake and guard. Pavement under 1.2 m: no tree on the pavement; the front garden is offered to the owner.',
   'mezcla': 'No species above 30% of a sector.'}},
 'vial': {
  'es': {
   'principal': 'Nogal (Juglans neotropica) y Roble andino (Quercus humboldtii) en separadores de 4 m o más; Cedro de montaña (Cedrela montana) con nodriza',
   'intermedio': 'Cajeto (Citharexylum subflavescens), Arrayán (Myrcianthes leucoxyla), Mano de oso (Oreopanax floribundus), Cerezo de monte (Prunus buxifolia)',
   'acomp': 'Andenes angostos o con redes: chicalá (Tecoma stans) y siete cueros (Andesanthus lepidotus).',
   'corto': 'Nogal, roble andino, cedro de montaña, cajeto, arrayán, mano de oso, chicalá',
   'como': 'Árbol de 2,5 m en bolsa de 30 L; un árbol cada 10 m por costado; en separador, hilera central a 1,5 m o más del sardinel. Sin árboles a menos de 30 m de un cruce semaforizado ni en curvas donde tapen la visibilidad. Protector contra impacto vehicular. En vías nacionales y departamentales, solo con permiso del titular.',
   'mezcla': 'Tramos de 100 a 200 m con una especie de dosel dominante y otra intercalada, para que el corredor se lea como una alameda.'},
  'en': {
   'principal': 'Walnut (Juglans neotropica) and Andean oak (Quercus humboldtii) on medians 4 m or wider; mountain cedar (Cedrela montana) with a nurse shrub',
   'intermedio': 'Cajeto (Citharexylum subflavescens), arrayán (Myrcianthes leucoxyla), mano de oso (Oreopanax floribundus), mountain cherry (Prunus buxifolia)',
   'acomp': 'Narrow pavements or under lines: chicalá (Tecoma stans) and siete cueros (Andesanthus lepidotus).',
   'corto': 'Walnut, Andean oak, mountain cedar, cajeto, arrayán, mano de oso, chicalá',
   'como': 'Tree 2.5 m tall in a 30 L bag; one every 10 m per side; on medians, a central row 1.5 m or more from the kerb. No trees within 30 m of a signalised junction or on bends where they block sight lines. Vehicle-impact guard. National and departmental roads only with the owner’s permit.',
   'mezcla': 'Stretches of 100–200 m with one dominant canopy species and one interplanted, so the corridor reads as an avenue.'}},
 'parque': {
  'es': {
   'principal': 'Roble andino (Quercus humboldtii), Nogal (Juglans neotropica), Cedro de montaña (Cedrela montana), Aliso (Alnus acuminata) en zonas húmedas',
   'intermedio': 'Arrayán, Cajeto, Gaque (Clusia multiflora), Cerezo de monte, Cedrillo (Phyllanthus salviifolius), Tuno esmeraldo (Miconia squamulosa)',
   'acomp': 'Bordes de arbustos para aves y polinizadores: garrocho (Viburnum triphyllum), mortiño (Hesperomeles goudotiana), chilco (Baccharis latifolia).',
   'corto': 'Roble andino, nogal, cedro de montaña, aliso, arrayán, cajeto, gaque, cerezo de monte',
   'como': 'Bosquetes de 5 a 15 árboles a 5–6 m entre sí, no hileras sueltas; dejar libres las canchas, juegos infantiles y senderos. Árbol de 2 m en bolsa de 20 L, acolchado de 10 cm y riego en seca durante dos años.',
   'mezcla': 'Al menos 6 especies por parque.'},
  'en': {
   'principal': 'Andean oak (Quercus humboldtii), walnut (Juglans neotropica), mountain cedar (Cedrela montana), alder (Alnus acuminata) in moist spots',
   'intermedio': 'Arrayán, cajeto, gaque (Clusia multiflora), mountain cherry, cedrillo (Phyllanthus salviifolius), tuno esmeraldo (Miconia squamulosa)',
   'acomp': 'Shrub edges for birds and pollinators: garrocho (Viburnum triphyllum), mortiño (Hesperomeles goudotiana), chilco (Baccharis latifolia).',
   'corto': 'Andean oak, walnut, mountain cedar, alder, arrayán, cajeto, gaque, mountain cherry',
   'como': 'Groves of 5–15 trees 5–6 m apart rather than scattered rows; keep sports courts, playgrounds and paths clear. Tree 2 m tall in a 20 L bag, 10 cm mulch and dry-season watering for two years.',
   'mezcla': 'At least 6 species per park.'}},
 'escolar': {
  'es': {
   'principal': 'Arrayán (Myrcianthes leucoxyla), Cajeto (Citharexylum subflavescens), Mano de oso (Oreopanax floribundus)',
   'intermedio': 'Cerezo de monte (Prunus buxifolia), Chicalá (Tecoma stans), Gaque (Clusia multiflora), Cedrillo (Phyllanthus salviifolius)',
   'acomp': 'No sembrar especies espinosas ni de frutos tóxicos (tinto, corono, espino) en patios escolares.',
   'corto': 'Arrayán, cajeto, mano de oso, cerezo de monte, chicalá, gaque, cedrillo',
   'como': 'Árboles de sombra en el borde sur y occidental de patios y canchas, a 3 m de muros y a 5 m de aulas. Árbol de 2 m en bolsa de 20 L con protector. Cada curso adopta árboles dentro del proyecto ambiental escolar (PRAE).',
   'mezcla': 'Al menos 4 especies por sede.'},
  'en': {
   'principal': 'Arrayán (Myrcianthes leucoxyla), cajeto (Citharexylum subflavescens), mano de oso (Oreopanax floribundus)',
   'intermedio': 'Mountain cherry (Prunus buxifolia), chicalá (Tecoma stans), gaque (Clusia multiflora), cedrillo (Phyllanthus salviifolius)',
   'acomp': 'No thorny species or species with toxic fruit (tinto, corono, espino) in school yards.',
   'corto': 'Arrayán, cajeto, mano de oso, mountain cherry, chicalá, gaque, cedrillo',
   'como': 'Shade trees along the south and west edges of yards and courts, 3 m from walls and 5 m from classrooms. Tree 2 m tall in a 20 L bag with a guard. Each class adopts trees through the school environmental project (PRAE).',
   'mezcla': 'At least 4 species per school.'}},
 'ronda': {
  'es': {
   'principal': 'Orilla (0–5 m del cauce): Aliso (Alnus acuminata), Sauce criollo (Salix humboldtiana), Chilco (Baccharis latifolia), Duraznillo (Abatia parviflora)',
   'intermedio': 'Franja media (5–30 m): Tobo (Escallonia paniculata), Tíbar (Escallonia pendula), Cucharo (Myrsine coriacea), Laurel de cera (Morella pubescens), Raque (Vallea stipularis), Arrayán',
   'acomp': 'Arbustos: garrocho (Viburnum triphyllum) y chilco como nodrizas. En suelos encharcables del río Bogotá: aliso, sauce, chilco y laurel de cera.',
   'corto': 'Aliso, sauce criollo, chilco, duraznillo, tobo, tíbar, cucharo, laurel de cera, raque',
   'como': 'Planta de 0,9–1,2 m a 3 × 3 m (1.111 por hectárea) en tresbolillo; 40 % pioneras (aliso, chilco, laurel de cera) y 60 % de las demás. Plateo de 1 m, hidrorretenedor y abono; aislar con cerca si hay ganado. No sembrar dentro del cauce ni sobre jarillones sin concepto de la CAR.',
   'mezcla': 'Al menos 8 especies por tramo.'},
  'en': {
   'principal': 'Bank (0–5 m from the channel): alder (Alnus acuminata), Andean willow (Salix humboldtiana), chilco (Baccharis latifolia), duraznillo (Abatia parviflora)',
   'intermedio': 'Middle strip (5–30 m): tobo (Escallonia paniculata), tíbar (Escallonia pendula), cucharo (Myrsine coriacea), wax myrtle (Morella pubescens), raque (Vallea stipularis), arrayán',
   'acomp': 'Shrubs: garrocho (Viburnum triphyllum) and chilco as nurses. On waterlogged Bogotá River soils: alder, willow, chilco and wax myrtle.',
   'corto': 'Alder, Andean willow, chilco, duraznillo, tobo, tíbar, cucharo, wax myrtle, raque',
   'como': 'Stock 0.9–1.2 m at 3 × 3 m (1,111 per hectare) in a staggered grid; 40% pioneers (alder, chilco, wax myrtle), 60% the rest. 1 m weeded circle, hydrogel and compost; fence off cattle. No planting in the channel or on levees without a CAR opinion.',
   'mezcla': 'At least 8 species per reach.'}},
 'cerro': {
  'es': {
   'principal': 'Años 1–2, pioneras: Chilco, Arboloco (Smallanthus pyramidalis), Tabaquillo (Verbesina crassiramea), Laurel de cera, Cucharo, Raque, Mortiño',
   'intermedio': 'Años 3–5, bajo la sombra de las pioneras: Encenillo (Weinmannia tomentosa), Gaque, Mano de oso, Aguacatillo (Persea mutisii), Amarillo (Ocotea calophylla), Ají de páramo (Drimys granadensis) en la parte alta y húmeda',
   'acomp': 'Arbustos de flor para colibríes: pegamosco (Bejaria resinosa) y uvo de monte (Cavendishia bracteata).',
   'corto': 'Chilco, arboloco, tabaquillo, laurel de cera, cucharo, raque, mortiño; después encenillo, gaque, aguacatillo',
   'como': 'Núcleos de 20 × 20 m (unas 25 plantas a 4 × 4 m) pegados al borde del bosque, no plantación continua: el resto se deja regenerar con semillas de las aves. Planta de 0,6–1 m; cerca contra ganado; no sembrar en vegetación nativa existente ni en suelos de páramo.',
   'mezcla': 'Al menos 10 especies por núcleo.'},
  'en': {
   'principal': 'Years 1–2, pioneers: chilco, arboloco (Smallanthus pyramidalis), tabaquillo (Verbesina crassiramea), wax myrtle, cucharo, raque, mortiño',
   'intermedio': 'Years 3–5, under the pioneers’ shade: encenillo (Weinmannia tomentosa), gaque, mano de oso, aguacatillo (Persea mutisii), amarillo (Ocotea calophylla), ají de páramo (Drimys granadensis) on upper, moist slopes',
   'acomp': 'Hummingbird shrubs: pegamosco (Bejaria resinosa) and uvo de monte (Cavendishia bracteata).',
   'corto': 'Chilco, arboloco, tabaquillo, wax myrtle, cucharo, raque, mortiño; later encenillo, gaque, aguacatillo',
   'como': 'Nuclei of 20 × 20 m (about 25 plants at 4 × 4 m) right at the forest edge, not continuous planting: the rest is left to regenerate from bird-dispersed seed. Stock 0.6–1 m; fence off cattle; no planting over existing native vegetation or páramo soils.',
   'mezcla': 'At least 10 species per nucleus.'}},
 'cerca': {
  'es': {
   'principal': 'Arbustos espinosos o densos: Corono (Xylosma spiculifera), Espino (Duranta mutisii), Hayuelo (Dodonaea viscosa), Mortiño (Hesperomeles goudotiana)',
   'intermedio': 'Arbolitos intercalados cada 9 m: Tíbar, Arrayán, Laurel de cera, Sauco andino (Sambucus peruviana), Raque',
   'acomp': 'En linderos húmedos: chilco y aliso. Sauco andino, no el sauco europeo.',
   'corto': 'Corono, espino, hayuelo, mortiño, tíbar, arrayán, laurel de cera, sauco andino',
   'como': 'Una planta cada 3 m sobre el lindero, de 0,6–0,9 m; un arbolito cada tercera planta. Se siembra junto a la cerca de alambre existente y la reemplaza en 4 a 6 años. El propietario aporta el cuidado; el municipio, las plantas y la asistencia técnica.',
   'mezcla': 'Al menos 4 especies por lindero.'},
  'en': {
   'principal': 'Thorny or dense shrubs: corono (Xylosma spiculifera), espino (Duranta mutisii), hopbush (Dodonaea viscosa), mortiño (Hesperomeles goudotiana)',
   'intermedio': 'Small trees every 9 m: tíbar, arrayán, wax myrtle, Andean elder (Sambucus peruviana), raque',
   'acomp': 'On moist boundaries: chilco and alder. Andean elder, not the European elder.',
   'corto': 'Corono, espino, hopbush, mortiño, tíbar, arrayán, wax myrtle, Andean elder',
   'como': 'One plant every 3 m along the boundary, 0.6–0.9 m tall; a small tree every third plant. Planted along the existing wire fence, which it replaces in 4–6 years. The owner provides care; the municipality provides plants and technical support.',
   'mezcla': 'At least 4 species per boundary.'}},
}
LIMITES = {
 'es': 'Límites: las recetas son por tipo de zona, no por sitio. La especie final de cada punto depende del ancho real del andén o separador, las redes aéreas y subterráneas, el drenaje del suelo y la disponibilidad en vivero, y se ajusta en la visita técnica. Las distancias son una propuesta de diseño para el manual municipal de silvicultura urbana y deben validarse con la Secretaría de Medio Ambiente, la CAR y las empresas de servicios. Las recetas se prepararon con apoyo de Claude, un asistente de inteligencia artificial de Anthropic, a partir de la paleta de especies del documento; requieren revisión de un ingeniero forestal o biólogo con experiencia en la Sabana.',
 'en': 'Limitations: recipes are per zone type, not per site. The final species at each point depends on actual pavement or median width, overhead and underground utilities, soil drainage and nursery stock, and is adjusted at the site visit. Distances are a design proposal for the municipal urban forestry manual and must be validated with the Environment Department, the CAR and utility companies. The recipes were prepared with the help of Claude, an AI assistant by Anthropic, from the paper’s species palette; they need review by a forester or biologist with Savanna experience.'}
