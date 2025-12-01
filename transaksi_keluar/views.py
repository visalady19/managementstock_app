from django.shortcuts import render, redirect
from django.db import connection
from django.conf import settings
from django.conf.urls.static import static
import os
from django.core.files.storage import FileSystemStorage

def keluar_list(request):
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT k.id_keluar, b.nama_barang, k.tanggal, k.penerima, k.jumlah_k, k.bukti_k
        FROM keluar k
        JOIN barang b ON k.id_barang = b.id_barang
        ORDER BY k.tanggal DESC, k.id_keluar DESC
        """)
        
        rows = cursor.fetchall()

    data = []
    for r in rows:
        data.append({
            "id_keluar": r[0],
            "nama_barang": r[1],
            "tanggal": r[2],
            "penerima": r[3],
            "jumlah_k": r[4],
            "bukti_k": r[5],
        })

    return render(request, "transaksi_keluar/index.html", {"data": data})


def keluar_add(request):

    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT id_barang, nama_barang 
        FROM barang 
        WHERE status = 'aktif'
        """)

        rows = cursor.fetchall()

    barang_list = [{"id_barang": r[0], "nama_barang": r[1]} for r in rows]

    if request.method == "POST":
        id_barang = request.POST.get("id_barang")
        tanggal = request.POST.get("tanggal")
        penerima = request.POST.get("penerima")
        jumlah = request.POST.get("jumlah")
        bukti_k = request.FILES.get("bukti_k")

        if bukti_k:
            upload_path = os.path.join(settings.MEDIA_ROOT, "bukti_keluar")

            fs = FileSystemStorage(location=upload_path)
            saved_name = fs.save(bukti_k.name, bukti_k)

            # path yang disimpan ke database
            filename = f"bukti_keluar/{saved_name}"  
        else:
            filename = None


        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO keluar (id_barang, tanggal, penerima, jumlah_k, bukti_k)
                VALUES (%s, %s, %s, %s, %s)
            """, [id_barang, tanggal, penerima, jumlah, filename])

        # Kurangi stok sesuai jumlah_k
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE barang
                SET stock = stock - %s
                WHERE id_barang = %s
            """, [jumlah, id_barang])

        return redirect("/keluar/")

    return render(request, "transaksi_keluar/add.html", {
        "barang_list": barang_list
    })
