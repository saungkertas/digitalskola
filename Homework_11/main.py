from karyawan import *
from karyawati import *

joko = karyawan('Joko','32','08139999887')
rita = karyawati('Rita','28','085788889928')

print(f'Seorang karyawan bernama {joko.nama} di kantor {joko.nama_kantor} berusia {joko.umur} tahun dan nomor handphonenya adalah {joko.nomor_hp}')
print(f'Seorang karyawati bernama {rita.nama} di kantor {rita.nama_kantor} berusia {rita.umur} tahun dan nomor handphonenya adalah {rita.nomor_hp}')