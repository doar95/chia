# Diccionario de variables

## poblacion.csv
| Variable | Significado |
| --- | --- |
| codigo | Código DANE del municipio |
| municipio, provincia | Nombre y provincia de Cundinamarca |
| anio | Año |
| poblacion | Habitantes estimados |
| cabecera | Habitantes estimados en el casco urbano |

## piramide_2005_2017.csv
| Variable | Significado |
| --- | --- |
| anio | 2005 o 2017 |
| edad_desde | Edad inicial del grupo de cinco años. 85 reúne 85 y más |
| hombres, mujeres | Personas |

## hacienda.csv
| Variable | Significado | Unidad |
| --- | --- | --- |
| a | Año | |
| cat | Categoría municipal de ley | |
| pred, ica, otros | Predial, industria y comercio, otros tributos | Millones de pesos de 2025 |
| trib | Suma de los tres anteriores | Millones de pesos de 2025 |
| tot | Ingresos totales | Millones de pesos de 2025 |
| pc | Recaudo tributario por habitante | Pesos de 2025 |
| aut | Recaudo tributario sobre ingresos totales | Proporción de 0 a 1 |
| inv, fun, gas, ing | Inversión, funcionamiento, gasto total, ingreso total | Millones de pesos corrientes |
| rep, al | Marca de reporte y alerta de calidad del panel de origen | |

## catastro_zona_2018.csv y catastro_manzana_2018.csv
| Variable | Significado |
| --- | --- |
| zona | Vereda, Urbano o Urbano Calahorra |
| codigo_sector_manzana | Ocho primeros dígitos del número predial: tipo, sector y manzana o vereda |
| predios | Número de predios del grupo |
| avaluo_total_miles_de_millones, avaluo_total_millones | Suma de avalúos, pesos de 2018 |
| mediana_avaluo_millones | Mediana del avalúo por predio, pesos de 2018 |
| p25_m2, mediana_m2, p75_m2, mediana_avaluo_por_m2_terreno | Cuartiles del avalúo total sobre área de terreno, pesos de 2018 por metro cuadrado |
| predios_con_valor_m2 | Predios que entran en ese cálculo |

## predios_2026.geojson
| Propiedad | Significado |
| --- | --- |
| d | Destino económico agrupado: h habitacional, c comercial, a agropecuario, l lotes, o otros, n sin dato |
| u | 1 urbano, 0 rural |

## avaluo_rejilla_2018.geojson
| Propiedad | Significado |
| --- | --- |
| v | Mediana del avalúo por metro cuadrado, redondeada a miles de pesos de 2018 |
| n | Predios en la celda |

## limites_municipios.geojson
| Propiedad | Significado |
| --- | --- |
| c | Código DANE |
| n | Nombre |
| p | Provincia: centro u occidente |

## veredas_dane_2024.geojson
`n` nombre de la vereda, `a` área en hectáreas según la capa de origen.

## veredas_igac_2026.geojson
`cod` código catastral, `n` nombre. SN es la vereda sin nombre en la base, que corresponde a La Balsa. CHIA y MERCEDES DE CALAHORRA son los dos perímetros urbanos.

## agua_igac.geojson
`t` tipo: l laguna u otro cuerpo de agua, d río de doble margen, q drenaje sencillo. `n` nombre geográfico cuando existe.

## cultivos_osm.geojson
`t` tipo: c cultivo, i invernadero.
