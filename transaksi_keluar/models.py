from django.db import models

class BarangKeluar(models.Model):
    id_keluar = models.AutoField(primary_key=True)
    id_barang = models.IntegerField()
    tanggal = models.DateField()
    penerima = models.CharField(max_length=255)

    class Meta:
        db_table = 'keluar'   # nama tabel sesuai database

    def __str__(self):
        return f"Keluar {self.id_keluar}"
