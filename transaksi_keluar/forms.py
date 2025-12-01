from django import forms
from .models import BarangKeluar

class BarangKeluarForm(forms.ModelForm):
    class Meta:
        model = BarangKeluar
        fields = ['id_barang', 'tanggal', 'penerima']

        widgets = {
            'tanggal': forms.DateInput(attrs={'type': 'date'}),
            'penerima': forms.TextInput(attrs={'class': 'p-2 border rounded w-full'}),
        }
