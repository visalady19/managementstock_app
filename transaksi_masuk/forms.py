from django import forms
from .models import BarangMasuk

class BarangMasukForm(forms.ModelForm):
    class Meta:
        model = BarangMasuk
        fields = ['id_barang', 'tanggal', 'keterangan']
        widgets = {
            'tanggal': forms.DateInput(attrs={'type': 'date'}),
            'keterangan': forms.Textarea(attrs={'rows': 3}),
        }
