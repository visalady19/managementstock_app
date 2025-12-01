from django.shortcuts import render, redirect
from django.db import connection


# LIST BARANG
def barang_list(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id_barang, nama_barang, deskripsi, stock
            FROM barang
            WHERE status = 'aktif'
        """)
        barang = cursor.fetchall()

    return render(request, "inventory/barang_list.html", {
        "barang": barang
    })


# TAMBAH BARANG
def barang_add(request):
    if request.method == "POST":
        nama_barang = request.POST.get("nama_barang")
        deskripsi = request.POST.get("deskripsi")
        stok = request.POST.get("stok")

        with connection.cursor() as cursor:
            # Cek apakah barang sudah ada sebelumnya
            cursor.execute("""
                SELECT id_barang, status 
                FROM barang 
                WHERE nama_barang = %s
            """, [nama_barang])

            existing = cursor.fetchone()

        # === CASE 1: Barang belum pernah ada ===
        if not existing:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO barang (nama_barang, deskripsi, stock, status)
                    VALUES (%s, %s, %s, 'aktif')
                """, [nama_barang, deskripsi, stok])

            return redirect("/inventory/")

        # === CASE 2: Barang ada & status AKTIF → TOLAK ===
        if existing and existing[1] == "aktif":
            return render(request, "inventory/add.html", {
                "error": "Barang dengan nama ini sudah ada dan masih aktif!"
            })

        # === CASE 3: Barang ada & status NONAKTIF → RESTORE (aktifkan ulang) ===
        if existing and existing[1] == "nonaktif":
            id_barang = existing[0]

            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE barang 
                    SET deskripsi=%s, stock=%s, status='aktif'
                    WHERE id_barang=%s
                """, [deskripsi, stok, id_barang])

            return redirect("/inventory/")

    return render(request, "inventory/barang_add.html")


# EDIT BARANG
def barang_edit(request, id_barang):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM barang WHERE id_barang=%s", [id_barang])
        barang = cursor.fetchone()

    if request.method == "POST":
        nama = request.POST.get("nama_barang")
        deskripsi = request.POST.get("deskripsi")
        stock = request.POST.get("stock")

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE barang
                SET nama_barang=%s, deskripsi=%s, stock=%s
                WHERE id_barang=%s
            """, [nama, deskripsi, stock, id_barang])

        return redirect("/inventory/")

    return render(request, "inventory/barang_edit.html", {"barang": barang})


def barang_delete(request, id_barang):
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE barang
            SET status = 'nonaktif'
            WHERE id_barang = %s
        """, [id_barang])

    return redirect("/inventory/")

