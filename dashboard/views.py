from django.shortcuts import render, redirect
from django.db import connection

def dashboard_view(request):
    if "id_user" not in request.session:
        return redirect("/login/")

    # Hitung total barang
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM barang WHERE status = 'aktif'")
        total_barang = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM masuk")
        total_masuk = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM keluar")
        total_keluar = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM users")
        total_user = cursor.fetchone()[0]

        cursor.execute("""
            SELECT nama_barang, stock, deskripsi 
            FROM barang
            WHERE status = 'aktif'
            ORDER BY id_barang DESC
            LIMIT 10
            """)
        barang_rows = cursor.fetchall()

        barang_list = [
        {"nama_barang": r[0], "stock": r[1],"deskripsi": r[2]}
        for r in barang_rows
        ]   

    return render(request, "dashboard/index.html", {
        "total_barang": total_barang,
        "total_masuk": total_masuk,
        "total_keluar": total_keluar,
        "total_user": total_user,
        "email": request.session.get("email"),
        "barang_list": barang_list,

    })

