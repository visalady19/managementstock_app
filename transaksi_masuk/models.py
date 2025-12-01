from django.db import models

class BarangMasuk(models.Model):
    id_masuk = models.AutoField(primary_key=True)
    id_barang = models.IntegerField()
    tanggal = models.DateField()
    keterangan = models.TextField()

    class Meta:
        db_table = 'masuk'  # nama tabel di database

    def __str__(self):
        return f"Masuk {self.id_masuk}"
