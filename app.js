/* Chía, memoria y porvenir. Lógica del portal. */
(function () {
  const D = window.CHIA_DATOS, TX = window.CHIA_TXT;
  const LOC = { es: "es-CO", pt: "pt-BR", fr: "fr-FR", zh: "zh-CN", ar: "ar-u-nu-latn" };
  const $ = (id) => document.getElementById(id);
  let lang = "es", cap = 0, anio = 2026, evAct = -1, tarAct = null, map, listo = false;
  try { const g = localStorage.getItem("chia-idioma"); if (g && TX[g]) lang = g; } catch (e) {}
  const T = () => TX[lang];
  const nf = (n, o) => new Intl.NumberFormat(LOC[lang], o || {}).format(n);

  /* Fuentes. Tipo: of oficial, ju judicial, ac académica, pr prensa */
  const F = {
    esap: ["ESAP, Cundinamarca. Particularidades histórico-políticas de su formación, 2017", "", "ac"],
    cont: ["Alcaldía de Chía, Plan de contingencia municipal", "https://www.chia-cundinamarca.gov.co/2023/banner/PLAN%20DE%20CONTINGENCIA%20MUNICIPIO%20DE%20CHIA%20C.pdf", "of"],
    c1886: ["Constitución Política de Colombia de 1886", "", "of"],
    pob: ["Alcaldía de Chía, Población actualizada con censos DANE, 2019", "https://chia-cundinamarca.gov.co/2019/Informe%20final%20de%20empalme%202016%20-%202019/INFORME%20FINAL%20EMPALME%202016-2019/4%20RESPUESTAS%20OBSERVACIONES%20EMPALME/Secretaria%20de%20Planeacion/Direccion%20Sistemas%20de%20Informacion%20y%20Estadistica/POBLACION%20ACTUALIZADA%20NOV%202019.docx", "of"],
    mfmp: ["Alcaldía de Chía, Marco Fiscal de Mediano Plazo 2020", "https://chia-cundinamarca.gov.co/hacienda/marcofiscal/1.3.1.MFMP%202020%20CHIA.pdf", "of"],
    tesis: ["Aguilar Ramírez, D. O., tesis de maestría, Universidad Nacional de Colombia, 2019", "https://bffrepositorio.unal.edu.co/server/api/core/bitstreams/5d85a50d-de8f-43da-8500-9301427c0700/content", "ac"],
    seg: ["Municipio de Chía, Documento de seguimiento y evaluación del Acuerdo 17 de 2000", "https://www.chia-cundinamarca.gov.co/POT/Acuerdo100de2016/Documento%20de%20Seguimiento%20Acuerdo%2017%20de%202000.pdf", "of"],
    res: ["Resguardo Indígena de Fonquetá y Cerca de Piedra, Circular 001 de 2024", "https://chia-cundinamarca.gov.co/2024/resguardo/CIRCULAR%20001%20resguardo%20indigena.pdf", "of"],
    mga: ["Alcaldía de Chía, ficha MGA BPIN 202500000028984, lengua propia", "https://chia-cundinamarca.gov.co/2026/PROYECTOS%20DE%20INVERSI%C3%93N/Fichas%20MGA%20proyectos%20registrados%202024-2027/BPINMGA202500000028984.pdf", "of"],
    mga2: ["Alcaldía de Chía, ficha MGA BPIN 202500000028979, censo del resguardo", "https://chia-cundinamarca.gov.co/2026/PROYECTOS%20DE%20INVERSI%C3%93N/Fichas%20MGA%20proyectos%20registrados%202024-2027/BPINMGA202500000028979.pdf", "of"],
    pomca: ["Alcaldía de Chía, informe Sentencia río Bogotá y POMCA", "http://chia-cundinamarca.gov.co/2020/sentenciariobogota/POMCA%20CH%C3%8DA.pdf", "of"],
    a164: ["Concejo de Chía, Acuerdo 164 de 2019", "https://www.ceta.org.co/html/archivos/CETAEnlaces/Chia-Cundinamarca/ACUERDO%20164%20DE%202019.pdf", "of"],
    car: ["CAR Cundinamarca, PTAR Chía II", "https://www.car.gov.co/saladeprensa/ptar-chia-ii-la-obra-que-saneara-las-aguas-residuales-del-70-de-esa-ciudad", "of"],
    sspd: ["Superservicios, informe de vigilancia a Emserchía", "https://www.superservicios.gov.co/sites/default/files/inline-files/Informe%20de%20Evaluaci%C3%B3n%20Ch%C3%ADa.pdf", "of"],
    ptar2: ["Alcaldía de Chía, PTAR II", "https://chia-cundinamarca.gov.co/web/2023/12/26/9-2-ptar-ii/", "of"],
    accen: ["Accenorte, concesionario de la ANI, avances del proyecto", "https://accenorte.com/estado-de-la-via/avances-del-proyecto", "of"],
    alctr: ["Alcaldía de Chía, convenio con la ANI para la Troncal de los Andes", "https://www.chia-cundinamarca.gov.co/index.php/24-paginaprincipal/principaldonoso/1163-ani-construira-y-financiara-troncal-de-los-andes-en-chia-y-se-modifica-restriccion-a-trasporte-de-carga", "of"],
    tac: ["Tribunal Administrativo de Cundinamarca, expediente 2020 00720, medida cautelar", "https://www.ramajudicial.gov.co/documents/2271812/102526134/auto+estado+01-03-22.pdf/c5220e22-9a64-4158-b632-33f928b1a604", "ju"],
    anla: ["ANLA, licencia ambiental de Accesos Norte fase II, 7 de enero de 2026", "https://www.anla.gov.co/noticias-anla/la-anla-otorgo-licencia-ambiental-al-proyecto-de-ampliacion-de-la-autopista-norte-en-bogota", "of"],
    ani: ["ANI, aval de inicio de obras de la Autopista Norte, 15 de agosto de 2026", "https://www.ani.gov.co/en/w/anla-da-v%C3%ADa-libre-a-las-obras-de-ampliaci%C3%B3n-de-la-autopista-norte", "of"],
    idu: ["IDU, respuesta oficial sobre la ALO, noviembre de 2025", "https://www.idu.gov.co/Archivos_Portal/2025/servicio-a-la-ciudadania/consulte-sus-requerimientos/11-noviembre/07-11-25/202520501193981.pdf", "of"],
    etpot: ["El Tiempo, sentencia del Juzgado Primero Administrativo de Zipaquirá, 2025", "https://www.eltiempo.com/justicia/investigacion/juzgado-de-zipaquira-avala-legalidad-del-pot-de-chia-y-rechaza-demanda-por-supuestas-fallas-en-su-aprobacion-3501546", "pr"],
    al: ["Asuntos Legales, análisis de la sentencia del POT, 2025", "https://www.asuntoslegales.com.co/analisis/nicolas-valencia-4262676/se-reactiva-el-pot-de-chia-tras-suspension-judicial-un-giro-decisivo-para-su-desarrollo-territorial-4262667", "pr"],
    eesusp: ["El Espectador, suspensión provisional del POT, 2019", "https://www.elespectador.com/bogota/suspenden-provisionalmente-el-pot-de-chia-por-denuncias-de-volteo-de-tierras-article-851874/", "pr"],
    ettr: ["El Tiempo, Resolución 003736 de 2025 de la ANLA", "https://www.eltiempo.com/bogota/se-destraba-el-proyecto-de-la-troncal-de-los-andes-via-entre-el-norte-de-bogota-y-chia-tras-suspension-judicial-hay-cambios-y-reubicaciones-3520648", "pr"],
    ens: ["El Nuevo Siglo, 9 de noviembre de 2026", "https://www.elnuevosiglo.com.co/nacion/troncal-de-los-andes-destraba-obras-en-chia-despues-de-nueve-anos-de-espera", "pr"],
    etchu: ["El Tiempo, sanción de la CAR por la Chucua de Fagua", "https://www.eltiempo.com/bogota/secan-humedal-la-facua-en-chia-300202", "pr"],
    eechu: ["El Espectador, el caso de la Chucua de Chía", "https://www.elespectador.com/bogota/corrupcion-negligencia-o-mala-suerte-el-caso-de-la-chucua-de-chia-article-850451/", "pr"],
    danef: ["DANE, ficha del Censo 2018 para Chía", "https://sitios.dane.gov.co/cnpv/app/views/informacion/fichas/25175.pdf", "of"],
    danep: ["DANE, proyecciones y retroproyecciones de población municipal", "https://www.dane.gov.co/index.php/estadisticas-por-tema/demografia-y-poblacion/proyecciones-de-poblacion", "of"],
    danev: ["DANE, capa de referencia de veredas 2024", "https://geoportal.dane.gov.co/", "of"],
    dnp: ["DNP, ejecuciones presupuestales y Operaciones Efectivas de Caja, panel municipal 1984 a 2025", "https://github.com/doar95/carga-tributaria-ciudades", "of"],
    diag: ["Alcaldía de Chía, Diagnóstico del POT, tomo II, dimensión económica, 2020", "https://www.chia-cundinamarca.gov.co/2020/POT/2.%20DIMENSI%C3%93N%20ECON%C3%93MICA.pdf", "of"],
    icde: ["IGAC, Mapa digital catastral urbano de Chía, metadato ICDE", "https://metadatos.icde.gov.co/geonetwork/srv/api/records/14160649", "of"],
    a227: ["Concejo de Chía, Acuerdo 227 de 2024", "https://chia-cundinamarca.gov.co/acuerdos/2024/ACUERDO%20227.pdf", "of"]
  };
  /* Hitos: año, fuentes, veredas que se resaltan */
  const EV = [
    [1500, ["esap"], null], [1537, ["cont"], null], [1815, ["esap"], null], [1857, ["esap"], null], [1886, ["c1886"], null],
    [1951, ["pob"], null], [1954, ["mfmp"], null], [1989, ["tesis"], null], [2000, ["seg"], "*"],
    [2013, ["res", "mga"], ["Fonqueta", "Cerca De Piedra"]], [2014, ["pomca", "tesis"], "*"], [2016, ["a164", "etpot"], "*"],
    [2018, ["accen", "alctr"], null], [2019, ["a164", "pomca", "eesusp"], "*"], [2025, ["etpot", "al", "ettr"], "*"], [2026, ["ens", "tac"], null]
  ];
  const TAR = {
    a1: [["tesis"], ["Fagua", "Tiquiza", "Fonqueta", "Cerca De Piedra", "La Balsa"]], a2: [["tesis"], null], a3: [["car", "ptar2", "sspd"], ["La Balsa"]],
    a4: [["pomca", "tesis"], "*"], a5: [["etchu", "eechu"], ["Fagua"]],
    p1: [["seg", "a164"], "*"], p2: [["etpot", "al", "eesusp"], "*"], p3: [["seg"], null], p4: [["accen", "alctr", "tac", "ettr"], null],
    p5: [["accen", "anla", "ani"], null], p6: [["idu"], null], p7: [["res", "mga", "mga2"], ["Fonqueta", "Cerca De Piedra"]]
  };
  const CENSOS = [[1951, 9514, 2698, 6816], [1964, 15793, 5655, 10138], [1973, 20602, 9355, 11247], [1985, 38852, 24709, 14143], [1993, 45696, 41632, 4064], [2005, 97444, 73087, 24357], [2018, 132181, 105509, 26672]];
  const RANGOS = ["< 500 m²", "500 – 1.000", "1.000 – 3.000", "3.000 – 10.000", "1 – 2 ha", "> 2 ha"];
  const PANIO = { 2010: [4703, 2056, 2806, 1431, 885, 463], 2011: [5112, 2127, 2873, 1422, 886, 465], 2012: [5403, 2164, 2894, 1431, 880, 467], 2013: [5834, 2270, 2914, 1429, 882, 468], 2014: [6409, 2399, 2947, 1427, 880, 461], 2015: [5728, 2199, 2579, 1219, 786, 460], 2016: [7446, 2573, 2931, 1434, 804, 454], 2017: [7807, 2691, 2987, 1448, 808, 451], 2018: [10147, 4226, 4325, 2174, 1120, 676], 2019: [10542, 4250, 4314, 2193, 1121, 726] };
  const PVER = { "Fagua": [625, 319, 549, 316, 63, 74], "Tiquiza": [1332, 150, 202, 141, 51, 42], "Fonqueta": [1133, 387, 365, 198, 39, 27], "Cerca De Piedra": [919, 347, 330, 136, 50, 10], "La Balsa": [2235, 789, 930, 259, 43, 108], "Yerbabuena": [99, 240, 634, 398, 680, 246], "Fusca": [77, 75, 157, 284, 135, 159] };
  const DENS = [["Fusca", 672, 1443, 0.47], ["Yerbabuena", 1565, 2421, 0.65], ["Fagua", 1343, 695, 1.93], ["Tíquiza", 1325, 484, 2.74], ["La Balsa", 3214, 838, 3.84], ["Fonquetá", 1654, 385, 4.29], ["Cerca de Piedra", 1663, 336, 4.96], ["Bojacá", 6321, 838, 7.54], ["U", 27710, 562, 49.31], ["UMC", 3452, 41, 84.78]];
  const VNOM = { "Fonqueta": "Fonquetá", "Tiquiza": "Tíquiza", "Cerca De Piedra": "Cerca de Piedra", "Calahorra 1": "Calahorra" };

  /* Escala de tiempo: 1500 a 1950 ocupa un cuarto de la pista */
  const v2a = (v) => Math.round(v < 250 ? 1500 + (v / 250) * 450 : 1950 + ((v - 250) / 750) * 76);
  const a2v = (a) => a < 1950 ? ((a - 1500) / 450) * 250 : 250 + ((a - 1950) / 76) * 750;

  const fts = (ids) => '<div class="fts">' + ids.map((id) => {
    const f = F[id], tag = f[1] ? "a" : "span";
    return `<${tag} class="ft t-${f[2]}" ${f[1] ? `href="${f[1]}" target="_blank" rel="noopener"` : ""}><b>${T().ui.types[f[2]]}</b>${f[0]}</${tag}>`;
  }).join("") + "</div>";

  /* Gráficas en SVG */
  function linea(serie, w, h, color, marca) {
    const xs = serie.map((d) => d[0]), ys = serie.map((d) => d[1]);
    const x0 = Math.min(...xs), x1 = Math.max(...xs), y1 = Math.max(...ys) * 1.08, L = 44, B = 18, Tp = 6, R = 18;
    const X = (x) => L + ((x - x0) / (x1 - x0)) * (w - L - R), Y = (y) => Tp + (1 - y / y1) * (h - Tp - B);
    let g = "";
    for (let i = 0; i <= 3; i++) { const y = (y1 / 1.08) * i / 3; g += `<line x1="${L}" x2="${w - R}" y1="${Y(y)}" y2="${Y(y)}" stroke="#22344a"/><text x="${L - 5}" y="${Y(y) + 3}" text-anchor="end">${nf(y, { notation: "compact" })}</text>`; }
    [x0, 1995, 2005, 2015, x1].forEach((x) => g += `<text x="${X(x)}" y="${h - 4}" text-anchor="middle">${x}</text>`);
    const p = serie.map((d, i) => (i ? "L" : "M") + X(d[0]).toFixed(1) + " " + Y(d[1]).toFixed(1)).join("");
    const m = serie.find((d) => d[0] === marca);
    return `<svg viewBox="0 0 ${w} ${h}" width="100%" role="img" style="direction:ltr">${g}<path d="${p}L${X(x1)} ${Y(0)}L${X(x0)} ${Y(0)}Z" fill="${color}22"/><path d="${p}" fill="none" stroke="${color}" stroke-width="2"/>${m ? `<circle cx="${X(m[0])}" cy="${Y(m[1])}" r="4.5" fill="${color}" stroke="#0a1420" stroke-width="2"/>` : ""}</svg>`;
  }
  function piramide(w, h) {
    const a = D.pir[2005], b = D.pir[2017], n = 18, mx = Math.max(...b.h, ...b.m) * 1.05, c = w / 2, bh = (h - 16) / n, half = c - 22;
    let g = "";
    for (let i = 0; i < n; i++) {
      const y = h - 16 - (i + 1) * bh, lab = i === 17 ? "85+" : (i * 5) + "";
      const r = (v) => (v / mx) * half;
      g += `<rect x="${c - 16 - r(b.h[i])}" y="${y + 1}" width="${r(b.h[i])}" height="${bh - 2}" fill="#63b8c4"/><rect x="${c + 16}" y="${y + 1}" width="${r(b.m[i])}" height="${bh - 2}" fill="#e3b04b"/>`;
      g += `<rect x="${c - 16 - r(a.h[i])}" y="${y + 1}" width="${r(a.h[i])}" height="${bh - 2}" fill="none" stroke="#efe9dc" stroke-width="1" opacity=".75"/><rect x="${c + 16}" y="${y + 1}" width="${r(a.m[i])}" height="${bh - 2}" fill="none" stroke="#efe9dc" stroke-width="1" opacity=".75"/>`;
      if (i % 2 === 0 || i === 17) g += `<text x="${c}" y="${y + bh - 2}" text-anchor="middle">${lab}</text>`;
    }
    g += `<text x="${c - 20}" y="${h - 3}" text-anchor="end">${T().ui.men}</text><text x="${c + 20}" y="${h - 3}">${T().ui.women}</text>`;
    return `<svg viewBox="0 0 ${w} ${h}" width="100%" role="img" style="direction:ltr">${g}</svg>`;
  }
  function apilada(w, h, marca) {
    const f = D.fis.filter((d) => d.trib != null), L = 44, B = 18, Tp = 6, R = 8, mx = Math.max(...f.map((d) => d.trib)) * 1.05;
    const bw = (w - L - R) / f.length, Y = (v) => (v / mx) * (h - Tp - B), cols = ["#e3b04b", "#63b8c4", "#b79ad6"];
    let g = "";
    for (let i = 0; i <= 3; i++) { const v = (mx / 1.05) * i / 3, y = h - B - Y(v); g += `<line x1="${L}" x2="${w - R}" y1="${y}" y2="${y}" stroke="#22344a"/><text x="${L - 5}" y="${y + 3}" text-anchor="end">${nf(v, { notation: "compact" })}</text>`; }
    f.forEach((d, i) => {
      let y = h - B; const x = L + i * bw;
      [d.pred, d.ica, d.otros].forEach((v, k) => { const hh = Y(v || 0); y -= hh; g += `<rect x="${x + .5}" y="${y}" width="${Math.max(bw - 1, 1)}" height="${hh}" fill="${cols[k]}" opacity="${d.a === marca ? 1 : .72}"/>`; });
      if (d.a % 10 === 0 || d.a === 2025) g += `<text x="${x + bw / 2}" y="${h - 4}" text-anchor="middle">${d.a}</text>`;
    });
    return `<svg viewBox="0 0 ${w} ${h}" width="100%" role="img" style="direction:ltr">${g}</svg>`;
  }
  function barrasAnio(w, h, cols) {
    const ys = Object.keys(PANIO), L = 44, B = 18, Tp = 6, R = 8, mx = 24000, bw = (w - L - R) / ys.length; let g = "";
    for (let i = 0; i <= 3; i++) { const v = mx * i / 3, y = h - B - (v / mx) * (h - Tp - B); g += `<line x1="${L}" x2="${w - R}" y1="${y}" y2="${y}" stroke="#22344a"/><text x="${L - 5}" y="${y + 3}" text-anchor="end">${nf(v, { notation: "compact" })}</text>`; }
    ys.forEach((a, i) => { let y = h - B; PANIO[a].forEach((n, k) => { const hh = (n / mx) * (h - Tp - B); y -= hh; g += `<rect x="${L + i * bw + 3}" y="${y}" width="${bw - 6}" height="${hh}" fill="${cols[k]}"/>`; }); g += `<text x="${L + i * bw + bw / 2}" y="${h - 4}" text-anchor="middle">${a}</text>`; });
    return `<svg viewBox="0 0 ${w} ${h}" width="100%" role="img" style="direction:ltr">${g}</svg>`;
  }
  function ranking(a) {
    const fs = D.mun.features.map((m) => [m.properties, (D.pop[m.properties.c] || {})[a]]).filter((x) => x[1]).sort((x, y) => y[1][0] - x[1][0]).slice(0, 8);
    const mx = fs[0][1][0];
    return fs.map(([p, v]) => `<div style="display:flex;align-items:center;gap:8px;font-size:12.5px;margin:3px 0"><span style="width:86px;${p.c === 25175 ? "color:var(--oro);font-weight:600" : "color:var(--tenue)"}">${p.n}</span><span style="flex:1;height:8px;background:#1b2b3f;border-radius:4px;overflow:hidden"><i style="display:block;height:100%;width:${(v[0] / mx) * 100}%;background:${p.c === 25175 ? "var(--oro)" : p.p === "centro" ? "#63b8c4" : "#8fb47a"}"></i></span><span style="width:60px;text-align:end">${nf(v[0])}</span></div>`).join("");
  }

  /* Capítulos */
  function pintar() {
    const t = T(), c = $("cont"); let h = t.ui.trans ? `<div class="trad">${t.ui.trans}</div>` : "";
    const ap = Math.min(Math.max(anio, 1985), 2025);
    if (cap === 0) {
      h += EV.map((e, i) => `<div class="ev ${e[0] <= anio ? "on" : ""} ${i === evAct ? "act" : ""}" data-ev="${i}"><div class="a">${i === 0 ? "≤ 1537" : e[0]}</div><h3>${t.ev[i][0]}</h3><p>${t.ev[i][1]}</p>${fts(e[1])}</div>`).join("");
    } else if (cap === 1) {
      const s = Object.keys(D.pop[25175]).map((y) => [+y, D.pop[25175][y][0]]);
      h += `<p>${t.gente.g1}</p><h2>${t.gente.chartT}</h2>${linea(s, 370, 170, "#e3b04b", ap)}${fts(["danep"])}`;
      h += `<h2>${t.ui.rank} ${ap}</h2>${ranking(ap)}<div class="ley" style="margin-top:8px"><span><i style="background:#63b8c4"></i>${t.ui.lgCentro}</span><span><i style="background:#8fb47a"></i>${t.ui.lgOcc}</span></div>`;
      h += `<h2>${t.gente.censT}</h2><table><tr><th>${t.ui.census}</th><th>${t.ui.total}</th><th>${t.ui.urban}</th><th>${t.ui.rural}</th></tr>${CENSOS.map((r) => `<tr><td>${r[0]}</td><td>${nf(r[1])}</td><td>${nf(r[2])}</td><td>${nf(r[3])}</td></tr>`).join("")}</table><p class="nota">${t.gente.censN}</p>${fts(["pob", "danef"])}`;
      h += `<h2>${t.gente.pirT}</h2>${piramide(370, 300)}<p class="nota">${t.gente.pirN}</p>${fts(["danep"])}`;
    } else if (cap === 2) {
      h += `<p>${t.hacienda.h1}</p><h2>${t.hacienda.chartT}</h2><div class="ley">${t.hacienda.k.map((k, i) => `<span><i style="background:${["#e3b04b", "#63b8c4", "#b79ad6"][i]}"></i>${k}</span>`).join("")}</div>${apilada(370, 190, Math.min(Math.max(anio, 1984), 2025))}<p class="nota">${t.ui.mill}. ${t.hacienda.n}</p>${fts(["dnp"])}<p>${t.hacienda.h2}</p><p>${t.hacienda.h3}</p><p>${t.hacienda.debt}</p>${fts(["a227"])}<p><a href="datos/hacienda.csv" download>${t.ui.download}</a></p>`;
    } else if (cap === 3) {
      const z = t.suelo, cols = ["#f3d58a", "#e3b04b", "#dd7a55", "#b79ad6", "#63b8c4", "#8fb47a"];
      h += `<p>${z.s1}</p><h2>${z.t1}</h2><div class="ley">${RANGOS.map((r, i) => `<span><i style="background:${cols[i]}"></i>${r}</span>`).join("")}</div>${barrasAnio(370, 180, cols)}`;
      h += `<h2>${z.t2}</h2>` + Object.keys(PVER).map((v) => { const tot = PVER[v].reduce((a, b) => a + b, 0); return `<div style="display:flex;align-items:center;gap:8px;font-size:12.5px;margin:4px 0;cursor:pointer" data-ver="${v}"><span style="width:104px;color:var(--tenue)">${VNOM[v] || v}</span><span style="flex:1;height:12px;display:flex;border-radius:3px;overflow:hidden;direction:ltr">${PVER[v].map((n, i) => `<i style="width:${n / tot * 100}%;background:${cols[i]}" title="${RANGOS[i]}: ${nf(n)}"></i>`).join("")}</span><span style="width:44px;text-align:end">${nf(tot)}</span></div>`; }).join("");
      const mx = 84.78;
      h += `<h2>${z.t3}</h2>` + DENS.map(([v, pr, ha, d]) => `<div style="display:flex;align-items:center;gap:8px;font-size:12.5px;margin:3px 0"><span style="width:104px;color:var(--tenue)">${v === "U" ? z.u : v === "UMC" ? z.u + " Calahorra" : v}</span><span style="flex:1;height:8px;background:#1b2b3f;border-radius:4px;overflow:hidden"><i style="display:block;height:100%;width:${Math.sqrt(d / mx) * 100}%;background:var(--teja)"></i></span><span style="width:44px;text-align:end">${nf(d, { maximumFractionDigits: 1 })}</span></div>`).join("");
      h += `<p class="nota" style="margin-top:8px">${z.n}</p>${fts(["diag"])}<p>${z.p}</p>${fts(["diag", "icde"])}`;
    } else {
      const grupo = cap === 4 ? t.agua : t.planes;
      h += Object.keys(grupo).map((k) => `<div class="tar ${tarAct === k ? "act" : ""}" data-tar="${k}"><h3>${grupo[k][0]}</h3><p>${grupo[k][1]}</p>${fts(TAR[k][0])}</div>`).join("");
    }
    c.innerHTML = h;
  }
  function interfaz() {
    const t = T();
    document.documentElement.lang = lang; document.documentElement.dir = lang === "ar" ? "rtl" : "ltr";
    document.title = t.ui.title;
    $("t-title").textContent = t.ui.title; $("t-sub").textContent = t.ui.sub;
    $("b-tour").textContent = t.ui.tour; $("b-src").textContent = t.ui.src;
    $("rec-rep").textContent = t.ui.replay; $("rec-fin").textContent = t.ui.skip;
    $("caps").innerHTML = t.ui.chapters.map((n, i) => `<button role="tab" aria-selected="${i === cap}" data-c="${i}">${n}</button>`).join("");
    document.querySelectorAll("#idi button").forEach((b) => b.setAttribute("aria-pressed", b.dataset.l === lang));
    $("leym").innerHTML = `<div><i style="border-color:#e3b04b"></i>${t.ui.lgChia}</div><div><i style="border-color:#63b8c4"></i>${t.ui.lgCentro}</div><div><i style="border-color:#8fb47a"></i>${t.ui.lgOcc}</div><div><i style="border-color:#e3b04b;border-top-style:dotted"></i>${t.ui.lgVer}</div><div style="margin-top:4px">${t.ui.legend}</div>`;
    pintar(); cabAnio();
  }
  function cabAnio() {
    $("anio-n").textContent = anio <= 1500 ? "≤ 1537" : anio;
    const p = (D.pop[25175] || {})[Math.min(anio, 2025)];
    if (anio >= 1985 && p) { $("anio-p").textContent = nf(p[0]); $("anio-l").textContent = T().ui.popLabel; }
    else { $("anio-p").textContent = ""; $("anio-l").textContent = T().ui.noPop; }
  }

  /* Mapa */
  function centro(geom) {
    const polys = geom.type === "Polygon" ? [geom.coordinates] : geom.coordinates; let best = polys[0][0];
    polys.forEach((p) => { if (p[0].length > best.length) best = p[0]; });
    let x0 = 180, x1 = -180, y0 = 90, y1 = -90; best.forEach(([x, y]) => { x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y); });
    return [(x0 + x1) / 2, (y0 + y1) / 2];
  }
  const puntos = { type: "FeatureCollection", features: D.mun.features.map((m) => ({ type: "Feature", properties: { c: m.properties.c, p: m.properties.p, n: m.properties.n, pob: 0 }, geometry: { type: "Point", coordinates: centro(m.geometry) } })) };
  function actualizaPuntos() {
    const a = Math.min(Math.max(anio, 1985), 2025), vis = anio >= 1985;
    puntos.features.forEach((f) => { const v = (D.pop[f.properties.c] || {})[a]; f.properties.pob = vis && v ? v[0] : 0; });
    if (listo) map.getSource("pts").setData(puntos);
  }
  function resalta(v) {
    if (!listo) return;
    const filtro = v === "*" ? ["has", "n"] : v ? ["in", ["get", "n"], ["literal", v]] : ["==", ["get", "n"], "__"];
    map.setFilter("ver-res", filtro);
  }
  function mapa() {
    map = new maplibregl.Map({
      container: "map", center: [-74.12, 4.86], zoom: 9.6, minZoom: 8, maxZoom: 15, pitch: 0, attributionControl: false,
      style: { version: 8, sources: {
        dem: { type: "raster-dem", tiles: ["https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"], tileSize: 256, encoding: "terrarium", maxzoom: 13, attribution: "Relieve: AWS Terrain Tiles" }
      }, layers: [
        { id: "fondo", type: "background", paint: { "background-color": "#0a1420" } },
        { id: "relieve", type: "hillshade", source: "dem", paint: { "hillshade-exaggeration": 0.6, "hillshade-shadow-color": "#02060c", "hillshade-highlight-color": "#c9b78e", "hillshade-accent-color": "#0a1420" } }
      ] }
    });
    map.addControl(new maplibregl.NavigationControl({ visualizePitch: true }), "top-right");
    map.addControl(new maplibregl.AttributionControl({ compact: true, customAttribution: "Límites y veredas: DANE 2024" }), "bottom-left");
    map.once("style.load", () => {
      map.addSource("mun", { type: "geojson", data: D.mun });
      map.addSource("ver", { type: "geojson", data: D.ver });
      map.addSource("pts", { type: "geojson", data: puntos });
      map.addLayer({ id: "mun-f", type: "fill", source: "mun", paint: { "fill-color": ["case", ["==", ["get", "c"], 25175], "#e3b04b", ["==", ["get", "p"], "centro"], "#63b8c4", "#8fb47a"], "fill-opacity": ["case", ["==", ["get", "c"], 25175], 0.1, 0.05] } });
      map.addLayer({ id: "mun-l", type: "line", source: "mun", paint: { "line-color": ["case", ["==", ["get", "p"], "centro"], "#63b8c4", "#8fb47a"], "line-width": 1, "line-opacity": 0.65 } });
      map.addLayer({ id: "chia-h", type: "line", source: "mun", filter: ["==", ["get", "c"], 25175], paint: { "line-color": "#e3b04b", "line-width": 9, "line-blur": 9, "line-opacity": 0.5 } });
      map.addLayer({ id: "chia-l", type: "line", source: "mun", filter: ["==", ["get", "c"], 25175], paint: { "line-color": "#e3b04b", "line-width": 2 } });
      map.addLayer({ id: "ver-res", type: "fill", source: "ver", filter: ["==", ["get", "n"], "__"], paint: { "fill-color": "#e3b04b", "fill-opacity": 0.28 } });
      map.addLayer({ id: "ver-l", type: "line", source: "ver", minzoom: 10.2, paint: { "line-color": "#e3b04b", "line-width": 1, "line-dasharray": [1, 2], "line-opacity": 0.8 } });
      map.addLayer({ id: "pts-h", type: "circle", source: "pts", paint: { "circle-radius": ["interpolate", ["linear"], ["sqrt", ["get", "pob"]], 0, 0, 450, 30], "circle-color": ["case", ["==", ["get", "c"], 25175], "#e3b04b", ["==", ["get", "p"], "centro"], "#63b8c4", "#8fb47a"], "circle-opacity": 0.22, "circle-blur": 0.6 } });
      map.addLayer({ id: "pts", type: "circle", source: "pts", paint: { "circle-radius": ["interpolate", ["linear"], ["sqrt", ["get", "pob"]], 0, 0, 450, 15], "circle-color": ["case", ["==", ["get", "c"], 25175], "#e3b04b", ["==", ["get", "p"], "centro"], "#63b8c4", "#8fb47a"], "circle-opacity": 0.85, "circle-stroke-color": "#0a1420", "circle-stroke-width": 1 } });
      D.mun.features.forEach((m) => { const e = document.createElement("div"); e.className = "etq" + (m.properties.c === 25175 ? " c" : ""); e.textContent = m.properties.n; const c = centro(m.geometry); new maplibregl.Marker({ element: e, anchor: "top", offset: [0, 12] }).setLngLat(c).addTo(map); });
      const ev = [];
      D.ver.features.forEach((v) => { const e = document.createElement("div"); e.className = "etq v"; e.textContent = VNOM[v.properties.n] || v.properties.n; e.style.display = "none"; ev.push(e); new maplibregl.Marker({ element: e }).setLngLat(centro(v.geometry)).addTo(map); });
      const zv = () => ev.forEach((e) => e.style.display = map.getZoom() > 11.3 ? "" : "none"); map.on("zoom", zv);
      map.on("click", "ver-res", () => {});
      const pop = new maplibregl.Popup({ closeButton: false, closeOnClick: false, offset: 10 });
      map.on("mousemove", "mun-f", (e) => {
        const p = e.features[0].properties, a = Math.min(Math.max(anio, 1985), 2025), v = (D.pop[p.c] || {})[a];
        let h = `<b>${p.n}</b>` + (v ? `<br>${nf(v[0])} · ${a}` : "");
        pop.setLngLat(e.lngLat).setHTML(`<div style="color:#0a1420;font:13px Inter,sans-serif">${h}</div>`).addTo(map); map.getCanvas().style.cursor = "pointer";
      });
      map.on("mouseleave", "mun-f", () => { pop.remove(); map.getCanvas().style.cursor = ""; });
      map.on("click", "mun-f", (e) => { if (e.features[0].properties.c === 25175) vista("chia"); });
      listo = true; actualizaPuntos(); vista("chia", 0);
      map.once("idle", actualizaPuntos); setTimeout(actualizaPuntos, 1500);
      setTimeout(() => { const at = document.querySelector(".maplibregl-ctrl-attrib"); at && at.classList.remove("maplibregl-compact-show"); }, 300);
      if (!/sin-recorrido/.test(location.search)) setTimeout(recorrido, 700);
    });
  }
  const VISTAS = { region: { center: [-74.16, 4.86], zoom: 9.3, pitch: 0, bearing: 0 }, chia: { center: [-74.058, 4.868], zoom: 11.7, pitch: 35, bearing: -12 }, oeste: { center: [-74.078, 4.858], zoom: 12.7, pitch: 55, bearing: 70 }, rios: { center: [-74.052, 4.84], zoom: 12.6, pitch: 50, bearing: -30 }, plano: { center: [-74.045, 4.868], zoom: 12, pitch: 0, bearing: 0 } };
  function vista(k, ms) {
    const v = Object.assign({}, VISTAS[k]); if (innerWidth < 820) { v.zoom -= 0.8; v.padding = { bottom: innerHeight * 0.42, top: 0, left: 0, right: 0 }; } else v.padding = { left: 430, top: 0, right: 0, bottom: 60 };
    if (ms === 0) map.jumpTo(v); else map.flyTo(Object.assign(v, { duration: ms || 2600, essential: true }));
  }

  /* Tiempo */
  function ponAnio(a, desdeSl) {
    anio = a; if (!desdeSl) $("sl").value = a2v(a);
    cabAnio(); actualizaPuntos();
    if (cap <= 2) pintar();
  }
  let reproduciendo = null;
  function play() {
    if (reproduciendo) { clearInterval(reproduciendo); reproduciendo = null; $("b-play").textContent = "▶"; return; }
    if (+$("sl").value >= 1000) $("sl").value = cap === 0 ? 0 : a2v(1985);
    $("b-play").textContent = "❚❚";
    reproduciendo = setInterval(() => {
      const v = Math.min(+$("sl").value + 4, 1000); $("sl").value = v; ponAnio(v2a(v), true);
      if (v >= 1000) play();
    }, 60);
  }
  function marcas() {
    const m = $("marcas"); let h = "";
    EV.forEach((e) => h += `<i style="left:${a2v(e[0]) / 10}%"></i>`);
    [1537, 1815, 1950, 1985, 2000, 2026].forEach((a) => h += `<span style="left:${a2v(a) / 10}%">${a}</span>`);
    m.innerHTML = h;
  }

  /* Recorrido de 30 segundos */
  const PASOS = [["region", 1985], ["oeste", 2013], ["chia", 2025], ["rios", 2025], ["plano", 2026], ["chia", 2026]];
  let rec = { i: 0, t0: 0, acum: 0, pausa: false, raf: 0 }; const DUR = 5000;
  function recPaso(i) {
    rec.i = i; const t = T().tour[i];
    $("rec-txt").innerHTML = `<h2>${t[0]}</h2><p>${t[1]}</p>`;
    vista(PASOS[i][0], 4200); ponAnio(PASOS[i][1]);
    resalta(i === 1 ? ["Fonqueta", "Cerca De Piedra"] : i === 3 ? ["La Balsa", "Fagua"] : i === 4 ? "*" : null);
  }
  function recTick(ts) {
    if (!rec.pausa) { if (!rec.t0) rec.t0 = ts; const el = rec.acum + (ts - rec.t0); $("rec-bar").style.width = Math.min(el / (DUR * PASOS.length) * 100, 100) + "%";
      const i = Math.floor(el / DUR); if (i >= PASOS.length) return recFin(); if (i !== rec.i) recPaso(i); }
    rec.raf = requestAnimationFrame(recTick);
  }
  function recorrido() {
    cancelAnimationFrame(rec.raf); rec = { i: -1, t0: 0, acum: 0, pausa: false, raf: 0 };
    document.body.classList.add("enrec"); $("rec").classList.add("ab"); $("rec-pausa").textContent = T().ui.pause;
    recPaso(0); rec.raf = requestAnimationFrame(recTick);
  }
  function recFin() { cancelAnimationFrame(rec.raf); document.body.classList.remove("enrec"); $("rec").classList.remove("ab"); resalta(null); ponAnio(2026); vista("chia"); }
  $("rec-pausa").onclick = () => { rec.pausa = !rec.pausa; if (rec.pausa) { rec.acum += performance.now() - rec.t0; } rec.t0 = 0; $("rec-pausa").textContent = rec.pausa ? T().ui.play : T().ui.pause; };
  $("rec-rep").onclick = () => recorrido(); $("rec-fin").onclick = recFin; $("b-tour").onclick = () => recorrido();

  /* Fuentes y método */
  function modal() {
    const t = T(), orden = ["of", "ju", "ac", "pr"];
    let h = `<div style="display:flex;justify-content:space-between;gap:12px;align-items:start"><h2>${t.ui.src}</h2><button class="pld" id="m-x">${t.ui.close}</button></div><h3>${t.ui.methodT}</h3><ul>${t.metodo.m.map((x) => `<li>${x}</li>`).join("")}</ul><h3>${t.ui.pendingT}</h3><ul>${t.metodo.pend.map((x) => `<li>${x}</li>`).join("")}</ul>`;
    orden.forEach((k) => { const l = Object.values(F).filter((f) => f[2] === k); h += `<h3>${t.ui.types[k]}</h3><ul class="lf">${l.map((f) => `<li>${f[1] ? `<a href="${f[1]}" target="_blank" rel="noopener">${f[0]}</a>` : f[0]}</li>`).join("")}</ul>`; });
    h += `<p><a href="datos/poblacion.csv" download>${t.ui.download}: poblacion.csv</a> · <a href="datos/hacienda.csv" download>hacienda.csv</a> · <a href="https://github.com/doar95/chia" target="_blank" rel="noopener">GitHub</a></p>`;
    $("caja").innerHTML = h; $("modal").classList.add("ab"); $("m-x").onclick = () => $("modal").classList.remove("ab");
  }
  $("b-src").onclick = modal; $("modal").onclick = (e) => { if (e.target.id === "modal") $("modal").classList.remove("ab"); };

  /* Eventos */
  $("idi").onclick = (e) => { const l = e.target.dataset.l; if (!l) return; lang = l; try { localStorage.setItem("chia-idioma", l); } catch (x) {} interfaz(); if ($("rec").classList.contains("ab")) recPaso(Math.max(rec.i, 0)); };
  $("caps").onclick = (e) => { const c = e.target.dataset.c; if (c == null) return; cap = +c; evAct = -1; tarAct = null; resalta(null); interfaz(); $("cont").scrollTop = 0; if (listo) vista(cap === 1 ? "region" : cap === 4 ? "rios" : cap === 3 ? "plano" : "chia"); };
  $("cont").onclick = (e) => {
    if (e.target.closest("a")) return;
    const ev = e.target.closest("[data-ev]"), ta = e.target.closest("[data-tar]"), ve = e.target.closest("[data-ver]");
    if (ve) resalta([ve.dataset.ver]);
    if (ev) { evAct = +ev.dataset.ev; ponAnio(EV[evAct][0]); resalta(EV[evAct][2]); pintar(); const el = document.querySelector(`[data-ev="${evAct}"]`); el && el.scrollIntoView({ block: "nearest" }); }
    if (ta) { tarAct = ta.dataset.tar; resalta(TAR[tarAct][1]); pintar(); if (listo) vista(tarAct === "p7" ? "oeste" : tarAct === "a3" || tarAct === "a1" ? "rios" : "plano"); }
  };
  $("sl").oninput = () => ponAnio(v2a(+$("sl").value), true);
  $("b-play").onclick = play;

  marcas(); interfaz(); mapa();
})();
