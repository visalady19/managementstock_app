from django.shortcuts import render, redirect
from django.db import connection
from django.conf import settings
from django.conf.urls.static import static
import os
from django.core.files.storage import FileSystemStorage

def masuk_list(request):
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT m.id_masuk, b.nama_barang, m.tanggal, m.keterangan, m.jumlah_m, m.bukti_m
        FROM masuk m
        JOIN barang b ON m.id_barang = b.id_barang
        ORDER BY m.tanggal DESC
        """)

        rows = cursor.fetchall()

    data = []
    for r in rows:
        data.append({
            "id_masuk": r[0],
            "nama_barang": r[1],
            "tanggal": r[2],
            "keterangan": r[3],
            "jumlah_m": r[4],
            "bukti_m": r[5],
        })

    return render(request, "transaksi_masuk/index.html", {"data": data})


def masuk_add(request):

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
        jumlah = request.POST.get("jumlah")
        keterangan = request.POST.get("keterangan")
        bukti_m = request.FILES.get("bukti_m")


        if bukti_m:
            upload_path = os.path.join(settings.MEDIA_ROOT, "bukti_masuk")

            fs = FileSystemStorage(location=upload_path)
            saved_name = fs.save(bukti_m.name, bukti_m)

            # path yang disimpan ke database
            filename = f"bukti_masuk/{saved_name}"  
        else:
            filename = None  

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO masuk (id_barang, tanggal, jumlah_m, keterangan, bukti_m)
                VALUES (%s, %s, %s, %s, %s)
            """, [id_barang, tanggal, jumlah, keterangan, filename])



        # Naikkan stok
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE barang SET stock = stock + %s WHERE id_barang = %s
            """, [jumlah, id_barang])

        return redirect("/masuk/")

    return render(request, "transaksi_masuk/add.html", {
        "barang_list": barang_list
    })
