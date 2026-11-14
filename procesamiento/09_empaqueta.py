"""09. Empaqueta los datos que lee el mapa en datos/datos.js. Correr después de 01 y 02."""
import json
D = json.load(open('datos/_base.json', encoding='utf-8'))
D['cat'] = json.load(open('datos/_catastro.json', encoding='utf-8'))
open('datos/datos.js', 'w', encoding='utf-8').write('window.CHIA_DATOS=' + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + ';')
print('datos/datos.js listo')
