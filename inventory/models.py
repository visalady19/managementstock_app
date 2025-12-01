from django.db import models

class Barang(models.Model):
    id_barang = models.AutoField(primary_key=True)
    nama_barang = models.CharField(max_length=255)
    deskripsi = models.TextField(null=True, blank=True)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.nama_barang
