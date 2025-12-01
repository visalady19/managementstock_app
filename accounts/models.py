from django.db import models

class Users(models.Model):
    id_user = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)


    class Meta:
        db_table = 'users'
