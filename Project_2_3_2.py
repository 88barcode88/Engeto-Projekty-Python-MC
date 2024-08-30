kandidati = ['Bruno', 'Anežka']
zamestnanci = ['František', 'Bruno', 'Anna', 'Jakub', 'Klára']
bez_bruna = kandidati.copy()
bez_bruna.remove('Bruno')
print('Bruno odstraněn:', bez_bruna)
opakovani_kandidati = bez_bruna * 3
print('Opakování kandidáti:', opakovani_kandidati)
spojeni_zamestnanci = zamestnanci + opakovani_kandidati
print('Spojeni zaměstnanci:', spojeni_zamestnanci)
