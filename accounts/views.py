from django.shortcuts import render, redirect
from .models import Users
from django.db import connection
import hashlib


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("username")     # ini email
        password = request.POST.get("password")

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id_user, email, password 
                FROM users 
                WHERE email=%s
            """, [email])
            user = cursor.fetchone()

        if user:
            db_id = user[0]
            db_password = user[2]

            if password == db_password:
                request.session["id_user"] = db_id
                request.session["email"] = email
                return redirect("/dashboard/")

            return render(request, "accounts/login.html", {"error": "Password salah!"})

        return render(request, "accounts/login.html", {"error": "Akun tidak ditemukan!"})

    return render(request, "accounts/login.html")

def register_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO users (email, password) VALUES (%s, %s)",
            [email, password]
        )

        return redirect("/login/")

    return render(request, "accounts/register.html")


from django.shortcuts import redirect

def logout_view(request):
    request.session.flush()  # hapus semua session
    return redirect('/accounts/login/')

