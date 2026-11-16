/* Datos compartidos y armado del documento. Los textos están en texto_es.js y texto_en.js. */
const ESPECIES = [
// común, científico, familia, porte (m), H, S, E, paletas, nota es, nota en
['Aliso', 'Alnus acuminata', 'Betulaceae', '15–25', 3, 1, 3, 'P1 P4 P5 P6', 'Fija nitrógeno; pionero ribereño', 'Nitrogen-fixing riparian pioneer'],
['Roble andino', 'Quercus humboldtii', 'Fagaceae', '20–30', 3, 2, 1, 'P2 P4', 'Vulnerable; bellotas para fauna; lento', 'Vulnerable; acorns for wildlife; slow'],
['Nogal', 'Juglans neotropica', 'Juglandaceae', '15–25', 2, 2, 1, 'P2 P4', 'En peligro; separadores anchos', 'Endangered; wide medians'],
['Cedro de montaña', 'Cedrela montana', 'Meliaceae', '15–25', 2, 2, 1, 'P2 P4', 'Joven sensible a helada: sembrar con nodriza', 'Frost-sensitive when young: plant with nurse shrubs'],
['Arrayán', 'Myrcianthes leucoxyla', 'Myrtaceae', '8–15', 3, 2, 2, 'P1 P2 P3 P4 P6', 'Flor blanca; frutos para aves', 'White flowers; fruit for birds'],
['Chicalá', 'Tecoma stans', 'Bignoniaceae', '5–8', 2, 3, 1, 'P2 P3 P4 P6', 'Flor amarilla; colibríes; tolera sequía', 'Yellow flowers; hummingbirds; drought-tolerant'],
['Cajeto, garagay', 'Citharexylum subflavescens', 'Verbenaceae', '8–12', 2, 2, 2, 'P2 P3 P4', 'Frutos para aves', 'Fruit for birds'],
['Sangregado', 'Croton bogotanus', 'Euphorbiaceae', '6–10', 2, 3, 1, 'P2 P3 P6', 'Crecimiento rápido', 'Fast-growing'],
['Tíbar', 'Escallonia pendula', 'Escalloniaceae', '6–10', 3, 2, 2, 'P1 P3 P5 P6', 'Flores para polinizadores', 'Flowers for pollinators'],
['Tobo', 'Escallonia paniculata', 'Escalloniaceae', '8–12', 3, 2, 2, 'P1 P5', 'Bordes de bosque y quebrada', 'Forest and stream edges'],
['Raque', 'Vallea stipularis', 'Elaeocarpaceae', '5–10', 3, 2, 2, 'P1 P5 P6', 'Flor rosada; colibríes', 'Pink flowers; hummingbirds'],
['Mano de oso', 'Oreopanax floribundus', 'Araliaceae', '8–15', 3, 2, 2, 'P3 P4 P5', 'Frutos para aves', 'Fruit for birds'],
['Cerezo de monte', 'Prunus buxifolia', 'Rosaceae', '8–12', 3, 2, 1, 'P3 P4', 'Floración blanca; frutos', 'White blossom; fruit'],
['Gaque', 'Clusia multiflora', 'Clusiaceae', '6–12', 3, 2, 2, 'P4 P5', 'Hoja coriácea, resistente', 'Leathery, hardy foliage'],
['Encenillo', 'Weinmannia tomentosa', 'Cunoniaceae', '10–20', 3, 2, 2, 'P5', 'Dominante del bosque altoandino; melífera', 'Dominant in high-Andean forest; honey plant'],
['Cucharo', 'Myrsine coriacea', 'Primulaceae', '6–12', 3, 2, 2, 'P1 P5', 'Pionera; frutos para aves', 'Pioneer; fruit for birds'],
['Cucharo blanco', 'Myrsine guianensis', 'Primulaceae', '6–10', 2, 2, 2, 'P1 P5', 'Pionera', 'Pioneer'],
['Tuno esmeraldo', 'Miconia squamulosa', 'Melastomataceae', '4–8', 3, 2, 2, 'P4 P5', 'Frutos para aves', 'Fruit for birds'],
['Siete cueros', 'Andesanthus lepidotus', 'Melastomataceae', '6–10', 2, 2, 2, 'P3 P4', 'Floración morada', 'Purple blossom'],
['Garrocho', 'Viburnum triphyllum', 'Viburnaceae', '4–8', 3, 2, 2, 'P1 P5 P6', 'Sotobosque; frutos', 'Understory; fruit'],
['Mortiño', 'Hesperomeles goudotiana', 'Rosaceae', '3–6', 3, 3, 1, 'P5 P6', 'Frutos rojos para aves', 'Red fruit for birds'],
['Corono', 'Xylosma spiculifera', 'Salicaceae', '4–8', 3, 3, 1, 'P6', 'Espinoso: cerca viva', 'Thorny: living fence'],
['Hayuelo', 'Dodonaea viscosa', 'Sapindaceae', '3–5', 3, 3, 1, 'P2 P6', 'Muy tolerante a sequía; protege suelos', 'Very drought-tolerant; soil protection'],
['Chilco', 'Baccharis latifolia', 'Asteraceae', '2–4', 3, 2, 3, 'P1 P6', 'Pionero y nodriza', 'Pioneer and nurse shrub'],
['Sauce criollo', 'Salix humboldtiana', 'Salicaceae', '10–15', 3, 1, 3, 'P1', 'Estabiliza orillas', 'Stabilises banks'],
['Duraznillo', 'Abatia parviflora', 'Salicaceae', '4–8', 3, 2, 2, 'P1 P5', 'Bordes húmedos', 'Moist edges'],
['Salvio negro', 'Cordia cylindrostachya', 'Boraginaceae', '3–6', 2, 3, 1, 'P5 P6', 'Melífera', 'Honey plant'],
['Laurel de cera', 'Morella pubescens', 'Myricaceae', '4–8', 3, 2, 3, 'P1 P5 P6', 'Fija nitrógeno', 'Nitrogen-fixing'],
['Pegamosco', 'Bejaria resinosa', 'Ericaceae', '2–4', 3, 2, 1, 'P5', 'Flor para colibríes', 'Hummingbird flower'],
['Uvo de monte', 'Cavendishia bracteata', 'Ericaceae', '2–4', 3, 2, 1, 'P5', 'Flor para colibríes', 'Hummingbird flower'],
['Ají de páramo', 'Drimys granadensis', 'Winteraceae', '6–12', 3, 1, 2, 'P5', 'Ladera alta y húmeda', 'Upper, moist slopes'],
['Aguacatillo', 'Persea mutisii', 'Lauraceae', '10–15', 2, 2, 1, 'P5', 'Frutos para aves grandes', 'Fruit for large birds'],
['Amarillo', 'Ocotea calophylla', 'Lauraceae', '10–15', 2, 2, 1, 'P5', 'Dosel de bosque maduro', 'Mature forest canopy'],
['Arboloco', 'Smallanthus pyramidalis', 'Asteraceae', '6–10', 2, 2, 2, 'P5', 'Pionero de crecimiento rápido', 'Fast-growing pioneer'],
['Tabaquillo', 'Verbesina crassiramea', 'Asteraceae', '4–8', 2, 3, 1, 'P5 P6', 'Pionero de ladera', 'Hillside pioneer'],
['Cedrillo', 'Phyllanthus salviifolius', 'Phyllanthaceae', '6–10', 3, 2, 2, 'P4 P5', 'Copa amplia y liviana', 'Wide, light crown'],
['Sauco andino', 'Sambucus peruviana', 'Viburnaceae', '4–8', 3, 2, 2, 'P6', 'No confundir con el sauco europeo', 'Not the European elder'],
['Espino', 'Duranta mutisii', 'Verbenaceae', '2–4', 3, 3, 1, 'P6', 'Espinoso; flor morada', 'Thorny; purple flowers'],
['Gurrubo', 'Lycianthes lycioides', 'Solanaceae', '2–4', 3, 3, 1, 'P6', 'Frutos para aves', 'Fruit for birds'],
['Tinto', 'Cestrum mutisii', 'Solanaceae', '2–4', 3, 2, 2, 'P6', 'Sotobosque y cerca', 'Understory and fence'],
['Jarilla', 'Stevia lucida', 'Asteraceae', '1–2', 3, 3, 1, 'P6', 'Arbusto de borde', 'Edge shrub']
];
const PALETAS = {es: {P1: 'P1 ribereña', P2: 'P2 sabana', P3: 'P3 vial', P4: 'P4 parque', P5: 'P5 ladera', P6: 'P6 cerca viva'}, en: {P1: 'P1 riparian', P2: 'P2 savanna', P3: 'P3 street', P4: 'P4 park', P5: 'P5 hillside', P6: 'P6 living fence'}};
const PRECIOS = [
 ['ronda', 62000, {es: 'Restauración 0,9–1,2 m a 3 × 3 m; preparación, hidrorretenedor, abono, seis mantenimientos, 20 % de reposición. Base: SAMC-012-2025 de Chía indexado 12 %.', en: 'Restoration, 0.9–1.2 m at 3 × 3 m; site preparation, hydrogel, compost, six maintenance visits, 20% replacement. Basis: Chía SAMC-012-2025, indexed 12%.'}],
 ['cerro', 58000, {es: 'Igual que ronda a 4 × 4 m, con menos plateo.', en: 'As riparian, at 4 × 4 m with less weeding.'}],
 ['cerca', 28000, {es: 'Arbusto o arbolito 0,6–0,9 m cada 3 m; dos años de mantenimiento con los propietarios.', en: 'Shrub or small tree 0.6–0.9 m every 3 m; two years of maintenance with landowners.'}],
 ['urbano', 480000, {es: 'Árbol ≥ 2,0 m, bolsa ≥ 20 L, hoyo 60 cm, sustrato, tutor triple, protector, riego y mantenimiento de 36 meses, 15 % de reposición. Base: CYPE Colombia y JBB.', en: 'Tree ≥ 2.0 m, ≥ 20 L bag, 60 cm pit, substrate, triple stake, guard, watering and 36 months of maintenance, 15% replacement. Basis: CYPE Colombia and JBB.'}],
 ['vial', 520000, {es: 'Árbol urbano más manejo de tráfico y protección contra impacto.', en: 'Urban tree plus traffic management and impact protection.'}],
 ['parque', 460000, {es: 'Árbol urbano en grupo, con acolchado y sin manejo de tráfico.', en: 'Urban tree planted in groups, with mulch, no traffic management.'}],
 ['escolar', 450000, {es: 'Árbol urbano con mantenimiento compartido con la comunidad educativa.', en: 'Urban tree with maintenance shared with the school community.'}]
];
const SECOP = [
 ['2025', 'Alcaldía de Chía', {es: 'Material vegetal, preparación de terreno, siembra y mantenimiento en predios de importancia ambiental y rondas (SAMC-012-2025)', en: 'Plant material, site preparation, planting and maintenance in environmental-priority land and stream buffers (SAMC-012-2025)'}, '493.922.201*', {es: '105 días', en: '105 days'}],
 ['2024', 'Alcaldía de Chía', {es: 'Mismo objeto (SAMC-018-2024)', en: 'Same object (SAMC-018-2024)'}, '264.799.990', {es: '45 días', en: '45 days'}],
 ['2025', 'Alcaldía de Chía', {es: 'Plántulas nativas para el vivero forestal', en: 'Native seedlings for the forest nursery'}, '63.905.131', {es: '2 meses', en: '2 months'}],
 ['2025', 'Alcaldía de Chía', {es: 'Insumos y material vegetal del vivero municipal', en: 'Supplies and plant material for the municipal nursery'}, '55.222.000', {es: '124 días', en: '124 days'}],
 ['2023', 'Alcaldía de Chía', {es: 'Cinco contratos de operarios para siembra y mantenimiento de nativas en áreas protegidas', en: 'Five individual worker contracts for native planting and maintenance in protected areas'}, '18.830.000 a 23.666.666', {es: '8–9 meses', en: '8–9 months'}],
 ['2026', 'Alcaldía de Chía', {es: 'Personal del vivero municipal (cinco contratos)', en: 'Municipal nursery staff (five contracts)'}, '36.960.000 a 77.269.500', {es: '11 meses', en: '11 months'}],
 ['2021–2023', 'Mosquera', {es: 'Mantenimiento de plantaciones en humedales y establecimiento de 0,5 a 2,21 ha', en: 'Maintenance of wetland plantings and establishment of 0.5–2.21 ha'}, '249.995.438 a 298.872.546', {es: 'anual', en: 'annual'}],
 ['2021', 'Funza', {es: 'Suministro de árboles nativos', en: 'Supply of native trees'}, '181.803.422', '—'],
 ['2022', 'Tabio', {es: 'Convenio con entidad sin ánimo de lucro para reforestación con niños y jóvenes', en: 'Agreement with a non-profit for reforestation with children and youth'}, '70.778.400', '—'],
 ['2026', 'Jardín Botánico de Bogotá', {es: 'Plantación de 20.000 árboles y mantenimiento de 190.000 árboles jóvenes (licitación JBB-LP-002-2026)', en: 'Planting of 20,000 trees and maintenance of 190,000 young trees (tender JBB-LP-002-2026)'}, '3.499.999.662', {es: '6 meses', en: '6 months'}]
];
const REFS = [
 ['r1', 'DANE. Proyecciones y retroproyecciones de población municipal, base Censo 2018; DNP, Operaciones Efectivas de Caja. Compiladas en <a href="https://github.com/doar95/chia/tree/main/datos">datos/poblacion.csv y datos/hacienda.csv</a> del repositorio Chía, memoria y porvenir.'],
 ['r2', 'Concejo Municipal de Chía. Acuerdo 219 de 2024, por el cual se adopta el Plan de Desarrollo 2024–2027. <a href="https://chia-cundinamarca.gov.co/acuerdos/2024/ACUERDO%20219%20DE%202024%20SANCIONADO.pdf">chia-cundinamarca.gov.co</a>'],
 ['r3', 'Alcaldía de Chía. Decreto 692 de 2024, liquidación del presupuesto 2025 (Acuerdo 232 de 2024). <a href="https://chia-cundinamarca.gov.co/2024/decretos/DECRETO%20692%20DE%202024%20CON%20ANEXO.pdf">chia-cundinamarca.gov.co</a>'],
 ['r4', 'Alcaldía de Chía, Secretaría de Medio Ambiente. Proceso SAMC-012-2025, contrato CO1.PCCNTR.8274239: estudios previos modificados, presupuesto oficial e informe de pago 1. <a href="https://contratacion.chia-cundinamarca.gov.co/VIGENCIA%202025/SECOP%20II/">contratacion.chia-cundinamarca.gov.co</a>'],
 ['r5', 'Colombia Compra Eficiente. SECOP II, contratos electrónicos y procesos, conjuntos jbjy-vk9h y p6dx-8zbt, consultados el 16 de noviembre de 2026. <a href="https://www.datos.gov.co/resource/jbjy-vk9h.json">datos.gov.co</a>'],
 ['r6', 'IDEAM. Catálogo nacional de estaciones (hp9r-jxuu) y datos hidrometeorológicos crudos de temperatura (sbwg-7ju4) y precipitación (s54a-sgyg), estación 2120500135 Universidad de La Sabana. <a href="https://www.datos.gov.co/resource/hp9r-jxuu.json">datos.gov.co</a>'],
 ['r7', 'Congreso de la República. Ley 2173 de 2021, áreas de vida y siembra de árboles por empresas. <a href="https://sidn.ramajudicial.gov.co/SIDN/NORMATIVA/TEXTOS_COMPLETOS/7_LEYES/LEYES%202021/Ley%202173%20de%202021%20(Compromiso%20Ambiental).pdf">ramajudicial.gov.co</a>'],
 ['r8', 'Ministerio de Ambiente. ABC de la Resolución 1491 del 17 de octubre de 2025, reglamentaria de la Ley 2173 de 2021. <a href="https://www.minambiente.gov.co/wp-content/uploads/2025/12/ABC-LEY-DE-ARBOL.pdf">minambiente.gov.co</a>'],
 ['r9', 'Ley 136 de 1994, art. 71; Corte Constitucional, Sentencia C-152 de 1995. <a href="https://www.corteconstitucional.gov.co/relatoria/1995/C-152-95.htm">corteconstitucional.gov.co</a>'],
 ['r10', 'Consejo de Estado, Sección Primera. Sentencia del 28 de marzo de 2014, expediente 2001-00479, recuperación del río Bogotá. Resumen en <a href="https://www.minambiente.gov.co/tenemos-una-oportunidad-enorme-para-recuperar-el-rio-bogota-ministerio-de-ambiente-a-los-47-alcaldes-con-obligaciones-en-cumplimiento-de-sentencia/">minambiente.gov.co</a>'],
 ['r11', 'Juzgado Primero Administrativo del Circuito de Zipaquirá. Sentencia del 17 de octubre de 2025, nulidad simple contra el Acuerdo 100 de 2016. Reseña en <a href="https://www.garrigues.com/es_ES/noticia/novedades-inmobiliarias-urbanisticas-colombia-octubre-2025">garrigues.com</a>'],
 ['r12', 'Konijnendijk, C. C. (2023). Evidence-based guidelines for greener, healthier, more resilient neighbourhoods: Introducing the 3–30–300 rule. Journal of Forestry Research 34, 821–830. <a href="https://doi.org/10.1007/s11676-022-01523-z">doi:10.1007/s11676-022-01523-z</a>'],
 ['r13', 'PNUMA. Medellín se refresca con intervenciones urbanas basadas en la naturaleza. <a href="https://www.unep.org/es/noticias-y-reportajes/reportajes/medellin-se-refresca-con-intervenciones-urbanas-basadas-en-la">unep.org</a>'],
 ['r14', 'Prefeitura de Curitiba. Curitiba é a capital com maior nota em qualidade do meio ambiente; Veja como Curitiba trabalha para mitigar e se adaptar às mudanças climáticas. <a href="https://www.curitiba.pr.gov.br/noticias/curitiba-e-a-capital-com-maior-nota-em-qualidade-do-meio-ambiente/83172">curitiba.pr.gov.br</a>'],
 ['r15', 'National Parks Board, Singapur. Annual Report y movimiento OneMillionTrees. <a href="https://www.nparks.gov.sg/portals/annualreport/chairmans-message">nparks.gov.sg</a>'],
 ['r16', 'City of Melbourne. Urban Forest Strategy. <a href="https://www.melbourne.vic.gov.au/community/greening-the-city/urban-forest/Pages/urban-forest-strategy.aspx">melbourne.vic.gov.au</a>'],
 ['r17', 'La Fabrique de la Cité (2026). 2014–2024: feedback on the Chinese Sponge City Program. <a href="https://www.lafabriquedelacite.com/en/publications/2014-2024-feedback-on-the-chinese-sponge-city-program/">lafabriquedelacite.com</a>'],
 ['r18', 'Jardín Botánico José Celestino Mutis. Resolución 161 de 2026 (adjudicación JBB-LP-002-2026); aviso JBB-LP-003-2026; balance de plantación 2024. <a href="https://jbb.gov.co/documentos/juridica/2026/junio/RESOLUCION_161.pdf">jbb.gov.co</a>; <a href="https://bogota.gov.co/mi-ciudad/ambiente/jardin-botanico-bogota-avanza-en-plantacion-de-nuevos-arboles-urbanos">bogota.gov.co</a>'],
 ['r19', 'CYPE Ingenieros. Generador de precios de la construcción, Colombia: UJP010 Árbol. <a href="https://colombia.generadordeprecios.info/rehabilitacion/Urbanizacion_interior_del_terreno/Jardineria/UJP_Suministro_y_plantacion_de_esp/Arbol.html">generadordeprecios.info</a>'],
 ['r20', 'SITECALI-Res, Centro de Pensamiento. Láminas «Dónde se calienta el suelo de Cali», «A igual edificación, el verde enfría» y «Donde faltan árboles, el suelo se calienta», con Landsat 8 y 9 (2019–2026) y CHMv2 de Meta y WRI (2026).'],
 ['r21', 'IGAC. Cartografía básica 1:25.000 y Base Catastral Pública 2026, procesadas en el repositorio (docs/METODO.md).'],
 ['r22', 'OpenStreetMap, © colaboradores, licencia ODbL. Extracto Overpass del 16 de noviembre de 2026 (insumos/osm_arborizacion_2026-11-16.txt).'],
 ['r23', 'UPRA (2024). Cultivos y áreas vulnerables a las heladas en enero de 2024. <a href="https://upra.gov.co/es-co/Documents/fenomeno_nino/20240125_Heladas-Enero-2024.pdf">upra.gov.co</a>'],
 ['r24', 'Ley 99 de 1993; Decreto 1076 de 2015; Ley 1931 de 2018; Ley 819 de 2003; Ley 1474 de 2011; Ley 850 de 2003; Ley 1712 de 2014; Decreto 1504 de 1998; Ley 607 de 2000; Resolución ICA 78006 de 2020. Gestor normativo de Función Pública, <a href="https://www.funcionpublica.gov.co/eva/gestornormativo/">funcionpublica.gov.co</a>'],
 ['r25', 'Gobernación de Cundinamarca, Secretaría de Bienestar Verde. Siembra del individuo un millón; convenio de semillas forestales nativas. <a href="https://www.cundinamarca.gov.co/noticias/cundinamarca-celebra-el-dia-mundial-del-arbol-con-la-siembra-en-nemocon-del-individuo-un-millon-de-la-estrategia-de-restauracion-ecologica">cundinamarca.gov.co</a>'],
 ['r26', 'Google Research. GEM-15, modelos de superficie y terreno de 15 m. <a href="https://developers.google.com/earth-engine/datasets/catalog/projects_climate-and-sustainability_assets_gem-15_v1">developers.google.com</a>'],
 ['r27', 'Convenio sobre la Diversidad Biológica, Decisión V/6 (2000), enfoque por ecosistemas; UICN (2020), Estándar Global para Soluciones basadas en la Naturaleza. <a href="https://www.cbd.int/decision/cop/?id=7148">cbd.int</a>; <a href="https://portals.iucn.org/library/node/49071">iucn.org</a>'],
 ['r28', 'Santamour, F. S. (1990). Trees for urban planting: diversity, uniformity, and common sense. Proceedings of the 7th Conference of the Metropolitan Tree Improvement Alliance, 57–65.']
];

let L = 'es', Z = [], RES = null;
const fmt = (n, d = 0) => (n == null ? '—' : Number(n).toLocaleString(L === 'es' ? 'es-CO' : 'en-US', {maximumFractionDigits: d, minimumFractionDigits: d}));
const mill = n => fmt(n / 1e6) + (L === 'es' ? ' M' : ' M');
const dots = n => '●'.repeat(n);
const COL = {ronda: '#2a78d6', vial: '#eb6834', parque: '#1baf7a', cerca: '#eda100', urbano: '#e87ba4', cerro: '#008300', escolar: '#6250d6'};
const ORD = ['ronda', 'cerro', 'vial', 'parque', 'escolar', 'urbano', 'cerca'];

function tabla(caption, head, rows, numCols = [], totRow = null) {
  const th = head.map((h, i) => `<th${numCols.includes(i) ? ' class="n"' : ''}>${h}</th>`).join('');
  const tr = r => '<tr>' + r.map((c, i) => `<td${numCols.includes(i) ? ' class="n"' : ''}>${c}</td>`).join('') + '</tr>';
  return `<div class="tabla"><table><caption>${caption}</caption><thead><tr>${th}</tr></thead><tbody>${rows.map(tr).join('')}${totRow ? tr(totRow).replace('<tr>', '<tr class="tot">') : ''}</tbody></table></div>`;
}

let RC = null;
function breve(T, $) {
  const B = T.breve, es = L === 'es';
  const per = e => ({1: '2027–28', 2: '2029–31', 3: '2032–35'})[e];
  const orden = ['urbano', 'vial', 'parque', 'escolar', 'ronda', 'cerro', 'cerca'];
  const filas = orden.map(t => {
    const zz = Z.filter(z => z.tipo === t), et = [...new Set(zz.map(z => z.etapa))].sort();
    const ini = {1: 2027, 2: 2029, 3: 2032}, fin = {1: 2028, 2: 2031, 3: 2035}, cuando = ini[et[0]] + '–' + fin[et[et.length - 1]];
    return [`<span class="chip" style="background:${COL[t]}"></span><b>${B.pref[t]}</b>`, T.tipos[t], B.filas[t], fmt(zz.reduce((a, z) => a + z.arboles, 0)), cuando];
  });
  const u1 = Z.filter(z => z.tipo === 'urbano' && z.etapa === 1).map(z => z.nombre.split(': ')[1]);
  const lista = u1.slice(0, -1).join(', ') + (es ? ' y ' : ' and ') + u1[u1.length - 1];
  const P = RES.presupuesto, n1 = RES.por_etapa['1'][1];
  const r = n => fmt(Math.round(n / 1e6));
  $('#breve').innerHTML = `<p class="ante">${B.ante}</p><h1>${B.titulo}</h1><p class="lead">${B.lead}</p>
  <p class="botones noimp"><a class="btn prim" href="mapa.html">${B.bMapa}</a> <a class="btn" href="descargas/plan_arborizacion_chia_${L}.pdf">${B.bPdf}</a> <a class="btn" href="datos/zonas_arborizacion_chia.xlsx">${B.bXls}</a></p>
  <figure class="fig"><a href="mapa.html"><img src="fig/mapa_zonas_${L}.png" alt="${B.bMapa}" style="width:100%"></a><figcaption>${B.figura}</figcaption></figure>
  <h2>${B.donde}</h2>` + tabla('', B.cab, filas, [3], ['', 'Total', '', fmt(RES.total[1]), '2027–2035']) +
  `<h2>${B.que}</h2><p>${B.queTxt}</p>` + tabla('', B.cabQ, orden.map(t => { const r = RC.recetas[t][L]; return [`<span class="chip" style="background:${COL[t]}"></span><b>${B.pref[t]}</b> ${T.tipos[t]}`, `<b>${es ? 'Principales' : 'Main'}:</b> ${r.principal}<br><b>${es ? 'Intermedias' : 'Secondary'}:</b> ${r.intermedio}<br>${r.acomp}`, `${r.como} ${r.mezcla}`]; })) +
  `<p><b>${es ? 'Cuándo' : 'When'}:</b> ${RC.meses[L]}</p><p class="nota">${RC.limites[L]}</p>
  <h2>${B.primero}</h2>${B.primeroTxt(lista, fmt(n1))}<figure class="fig"><a href="mapa.html"><img src="fig/mapa_urbano_${L}.png" alt="" style="width:100%"></a><figcaption>${B.figuraU}</figcaption></figure><h2>${B.cuanto}</h2>${B.cuantoTxt(r(P.municipio_total), r(P.municipio_anual_promedio), r(P.programa_total_todas_las_fuentes))}
  <h2>${B.plata}</h2>${B.plataTxt}<h2>${B.pide}</h2>${B.pideTxt}<p class="nota">${B.aviso}</p>
  <div class="sigue"><b>${B.sigue}</b><span>${B.sigueTxt}</span></div>`;
}

function render() {
  const T = window.TXT[L];
  document.documentElement.lang = L;
  document.title = T.titulo;
  const $ = s => document.querySelector(s);
  breve(T, $);
  $('#rev').innerHTML = T.revista.map(x => `<span>${x}</span>`).join('');
  $('#tit').textContent = T.titulo;
  $('#aut').innerHTML = T.autores;
  $('#cifras').innerHTML = T.cifras.map(c => `<div><b>${c[0]}</b><span>${c[1]}</span></div>`).join('');
  $('#dest').innerHTML = `<h3>${L === 'es' ? 'Destacados' : 'Highlights'}</h3><ul>${T.destacados.map(d => `<li>${d}</li>`).join('')}</ul>`;
  $('#res').innerHTML = `<h3>${L === 'es' ? 'Resumen' : 'Abstract'}</h3>${T.resumen}<p class="kw">${T.palabras}</p>`;
  $('#cuerpo').innerHTML = T.s.map(s => `<section id="${s.id}"><h2>${s.t}</h2>${s.h}</section>`).join('');
  $('#toc').innerHTML = `<b>${L === 'es' ? 'Contenido' : 'Contents'}</b>` + T.s.map(s => `<a href="#${s.id}">${s.t}</a>`).join('') + `<a href="#anexo">${T.anexo.split('.')[0]}</a><a href="#refs">${T.refs}</a>`;
  document.querySelectorAll('[data-t]').forEach(e => e.textContent = T[e.dataset.t]);
  $('#btn-pdf').href = `descargas/plan_arborizacion_chia_${L}.pdf`;
  $('#btn-lang').textContent = T.otro;

  // Tabla 4: por tipo
  const pt = RES.por_tipo;
  const rows4 = ORD.map(t => [`<span class="chip" style="background:${COL[t]}"></span>${T.tipos[t]}`, pt[t][0], fmt(pt[t][1]), mill(pt[t][2])]);
  $('#tabla-tipos').innerHTML = tabla(T.t4, [L === 'es' ? 'Tipo' : 'Type', L === 'es' ? 'Zonas' : 'Zones', L === 'es' ? 'Individuos' : 'Plants', L === 'es' ? 'Costo, pesos de 2027' : 'Cost, 2027 COP'], rows4, [1, 2, 3],
    ['Total', RES.total[0], fmt(RES.total[1]), mill(RES.total[2])]);
  // Tabla 5: especies
  $('#tabla-especies').innerHTML = tabla(T.t5, [L === 'es' ? 'Nombre común' : 'Common name', L === 'es' ? 'Especie' : 'Species', L === 'es' ? 'Familia' : 'Family', L === 'es' ? 'Altura (m)' : 'Height (m)', 'H', 'S', 'E', L === 'es' ? 'Paletas' : 'Palettes', L === 'es' ? 'Nota' : 'Note'],
    ESPECIES.map(e => [e[0], `<i>${e[1]}</i>`, e[2], e[3], dots(e[4]), dots(e[5]), dots(e[6]), e[7], L === 'es' ? e[8] : e[9]]));
  // Tabla 6: precios
  $('#tabla-precios').innerHTML = tabla(T.t6, [L === 'es' ? 'Tipo' : 'Type', L === 'es' ? 'Costo por individuo' : 'Cost per plant', L === 'es' ? 'Contenido y base' : 'Scope and basis'],
    PRECIOS.map(p => [T.tipos[p[0]], '$' + fmt(p[1]), p[2][L]]), [1]);
  // Tabla 7: etapas
  const P = RES.presupuesto, E = P.etapas;
  const lab = L === 'es' ? ['Etapa 0: preparación (2027-I)', 'Etapa 1: siembra y mantenimiento', 'Etapa 2: siembra y mantenimiento', 'Etapa 3: siembra y mantenimiento', 'Fortalecimiento del vivero municipal', 'Monitoreo, datos abiertos y programa comunitario (9 años)', 'Interventoría (8 % de la obra municipal)', 'Contingencia (5 %)', 'Total']
    : ['Stage 0: preparation (2027-H1)', 'Stage 1: planting and maintenance', 'Stage 2: planting and maintenance', 'Stage 3: planting and maintenance', 'Municipal nursery upgrade', 'Monitoring, open data and community programme (9 years)', 'Independent supervision (8% of municipal works)', 'Contingency (5%)', 'Total'];
  const otras = n => n;
  const rows7 = [
    [lab[0], mill(P.etapa0), mill(P.etapa0)],
    [lab[1], mill(E['1'].obra_total), mill(E['1'].obra_municipio)],
    [lab[2], mill(E['2'].obra_total), mill(E['2'].obra_municipio)],
    [lab[3], mill(E['3'].obra_total), mill(E['3'].obra_municipio)],
    [lab[4], mill(P.supuestos.vivero_fortalecimiento), mill(P.supuestos.vivero_fortalecimiento)],
    [lab[5], mill(P.transversal_total), mill(P.transversal_total)],
    [lab[6], mill(P.interventoria), mill(P.interventoria)],
    [lab[7], mill(P.contingencia), mill(P.contingencia)]];
  $('#tabla-etapas').innerHTML = tabla(T.t7, [L === 'es' ? 'Componente' : 'Component', L === 'es' ? 'Todas las fuentes' : 'All sources', L === 'es' ? 'A cargo del municipio' : 'Municipal share'], rows7, [1, 2],
    [lab[8], mill(P.programa_total_todas_las_fuentes), mill(P.municipio_total)]) +
    `<p class="kw">${L === 'es' ? 'En las zonas mixtas se supone que el municipio aporta la mitad; la otra mitad la aportan la CAR, la Gobernación, las empresas obligadas por la Ley 2173 y los propietarios. Las vías nacionales y departamentales y los predios privados no se cargan al municipio. Detalle de la etapa 0: ' : 'In mixed zones the municipality is assumed to cover half; the rest comes from the CAR, the department, companies under Law 2173 and landowners. National and departmental roads and private land are not charged to the municipality. Stage 0 detail: '}${Object.entries(P.supuestos.etapa0).map(([k, v]) => `${k} (${mill(v)})`).join('; ')}.</p>`;
  // Tabla 8: SECOP
  $('#tabla-secop').innerHTML = tabla(T.t8, [L === 'es' ? 'Año' : 'Year', L === 'es' ? 'Entidad' : 'Entity', L === 'es' ? 'Objeto' : 'Object', L === 'es' ? 'Valor (COP)' : 'Value (COP)', L === 'es' ? 'Plazo' : 'Term'],
    SECOP.map(s => [s[0], s[1], s[2][L], s[3], typeof s[4] === 'string' ? s[4] : s[4][L]]), [3]) +
    `<p class="kw">${L === 'es' ? '* Valor en la base de contratos de SECOP II; el informe de pago 1 del contratista reporta $331.932.534. Fuente: SECOP II, datos abiertos, y portal de contratación de Chía.' : '* Value in the SECOP II contracts dataset; the contractor’s first payment report states COP 331,932,534. Source: SECOP II open data and Chía’s procurement portal.'}</p>`;
  // Anexo
  const C = T.cols;
  const rowsA = Z.map(z => [z.id, z.nombre, `<span class="chip" style="background:${COL[z.tipo]}"></span>${T.tipos[z.tipo]}`, z.etapa, z.vereda, `<span class="coord">${z.lat.toFixed(5)}, ${z.lon.toFixed(5)}</span>`,
    z.longitud_m ? fmt(z.longitud_m) + ' m' : fmt(z.area_ha, 2) + ' ha', fmt(z.arboles), fmt(z.costo_cop), T.fin[z.financia], PALETAS[L][z.paleta.split(' ')[0]]]);
  $('#anexo').innerHTML = `<h2>${T.anexo}</h2><p>${T.anexoTxt}</p>` + tabla('', [C.id, C.nombre, C.tipo, C.etapa, C.vereda, C.coord, C.dim, C.arb, C.costo, C.fin, C.paleta], rowsA, [6, 7, 8]);
  $('#refs').innerHTML = `<h2>${T.refs}</h2>` + REFS.map((r, i) => `<p class="ref" id="${r[0]}">[${i + 1}] ${r[1]}</p>`).join('');
  document.querySelectorAll('img[src^="fig/"]').forEach(im => im.src = im.getAttribute('src').replace(/_(es|en)\.png/, `_${L}.png`));
  if (location.hash) { const t = document.getElementById(location.hash.slice(1)); if (t) t.scrollIntoView(); }
  document.body.dataset.listo = '1';
}

async function iniciar() {
  const q = new URLSearchParams(location.search).get('lang');
  let guard = null; try { guard = localStorage.getItem('chia-arb-lang'); } catch (e) {}
  L = q || guard || 'es';
  const [g, r, rc] = await Promise.all([fetch('datos/zonas.geojson').then(x => x.json()), fetch('datos/resumen.json').then(x => x.json()), fetch('datos/recetas.json').then(x => x.json())]);
  Z = g.features.map(f => f.properties); RES = r; RC = rc;
  render();
  document.getElementById('btn-lang').onclick = () => {
    L = L === 'es' ? 'en' : 'es'; try { localStorage.setItem('chia-arb-lang', L); } catch (e) {}
    const u = new URL(location.href); u.searchParams.set('lang', L); history.replaceState(null, '', u); render(); window.scrollTo(0, 0);
  };
}
iniciar();
