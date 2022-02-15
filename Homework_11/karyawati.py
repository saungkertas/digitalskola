class karyawati:
    nama_kantor = 'unilever'
    def __init__(self,nama,umur,nomor_hp):
        self.nama = nama
        self._umur = umur
        self.__nomor_hp = nomor_hp
    
    def nama(self):
        return self.nama

    @property
    def umur(self):
        return self._umur
    
    @property
    def nomor_hp(self):
        return self.__nomor_hp
    
    @nomor_hp.setter
    def nomor_hp(self, nomor_hp):
        self.__nomor_hp = nomor_hp