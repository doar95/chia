# Método y límites

Este documento reúne las decisiones que cambian lo que el portal muestra. Si una cifra le parece extraña, la explicación debería estar aquí.

## Regla general de fuentes

Se incluyen hechos que constan en actos administrativos, providencias judiciales, estadísticas oficiales o estudios de entidades públicas. Cuando un hecho oficial reciente solo se pudo verificar en prensa, se marca como Prensa y el hito lleva la advertencia de provisional. A noviembre de 2026 están en esa situación la sentencia del 17 de octubre de 2025 sobre el Acuerdo 100 de 2016, la Resolución 003736 de 2025 de la ANLA, la aclaración del Tribunal sobre la Troncal de los Andes y la fecha de cierre de la actualización catastral.

OpenStreetMap y Global Forest Change no son fuentes oficiales colombianas. Se usan como complemento en el capítulo de Geografía y así se rotulan.

## Límites municipales

No son la línea oficial. Se construyen uniendo las veredas de la capa de referencia del DANE de 2024. Esa capa no incluye las cabeceras, así que cada vacío se asigna al municipio con el que comparte más borde. Para Chía el área resultante es 80,5 kilómetros cuadrados frente a 80,44 que reporta la Alcaldía. Los de Mosquera y Madrid quedan recortados porque sus cabeceras no se cierran con esta regla. Sirven de contexto, no para medir.

## Población

Hay dos series que no se deben mezclar. Los censos de 1951 a 2018 vienen de una tabla de la Alcaldía con fuente DANE. La serie anual de 1985 a 2025 viene de las proyecciones y retroproyecciones del DANE basadas en el Censo de 2018, que recalculan los años anteriores. Para 2005 el censo da 97.444 habitantes y la serie anual 75.239.

La pirámide compara 2005 y 2017 porque es el archivo municipal por edad simple disponible en los insumos.

## Hacienda

El recaudo por impuesto está en pesos constantes de 2025. El gasto total, el funcionamiento y la inversión están en pesos corrientes de cada año, por lo que solo se usan como proporción dentro del mismo año. Los datos de 1984 a 1999 son ejecuciones presupuestales y los de 2000 a 2025 son Operaciones Efectivas de Caja, dos metodologías del DNP que no son idénticas. El dato de 2025 puede ser preliminar.

Las explicaciones de cada impuesto son generales y no reproducen el estatuto tributario municipal.

El aumento del predial en 2025 coincide con la entrada de nuevos avalúos catastrales según la prensa local. El portal no demuestra que esa sea la causa.

## Catastro de 2018

Los registros 1 y 2 del IGAC para Chía tienen corte del 28 de mayo de 2018 y contienen datos personales. No se publican. Se leen 43.581 predios, tomando una sola línea por predio.

- El **avalúo por metro cuadrado** es el avalúo total del predio, terreno más construcción, dividido por el área de terreno. Sobrestima el valor del suelo donde hay mucha construcción.
- Se excluyen de ese cálculo la propiedad horizontal y las mejoras, porque no tienen terreno propio comparable.
- El avalúo catastral no es precio comercial.
- Los nombres de vereda se asignaron por el código predial. La capa de veredas del catastro del IGAC de 2026 confirma la asignación. El código 007 aparece allí sin nombre y corresponde a La Balsa.
- Solo se publican grupos de cinco o más predios.

## Predios de 2026 y rejilla de avalúo

Los polígonos vienen de la Base Catastral Pública del IGAC de septiembre de 2026. Se cruzan con los registros de 2018 por el número predial anterior. De 32.322 predios cruzan 22.338. Cuando un predio no cruza directo pero su terreno sí, caso de la propiedad horizontal, se le asigna el destino más frecuente de sus unidades. El resto queda sin dato.

El mapa de avalúo usa celdas de unos 150 metros y muestra la mediana de las que reúnen cinco o más predios. Son valores de 2018 dibujados sobre el territorio de 2026.

## Geografía

La altitud y las curvas de nivel se calculan en el navegador con las teselas de elevación Terrarium, de unos 30 metros de resolución. No son curvas oficiales.

El agua, el bosque y los cerros vienen de la cartografía básica del IGAC a escala 1:25.000, recortada a Chía y un borde de contexto. La cifra de 1.086 hectáreas de bosque se mide contra el contorno simplificado de `insumos/chia_limite_aproximado.json`.

## Traducciones

Las hizo un modelo de inteligencia artificial y no tienen revisión de hablantes nativos. Los nombres de documentos se dejan en español.

## Lo que falta

Zonificación y usos del suelo de cada POT, cerro del Majuy y nacimientos, lluvia y calidad del agua y del aire, capacidad de servicios públicos, colegios, saldo de la deuda, patrimonio y turismo, topónimos muiscas, valor comercial del suelo, avalúos posteriores a la actualización catastral y trazados oficiales de vías.
