from distutils.command.upload import upload
from django.db import models

# Create your models here.
class Drone(models.Model):
    sn = models.AutoField(db_column='SN', primary_key=True)  # Field name made lowercase.
    did = models.IntegerField(db_column='DID')  # Field name made lowercase.
    tot = models.DateTimeField()
    flight = models.IntegerField()
    landing = models.IntegerField()
    temperature = models.CharField(max_length=500)
    altitude = models.CharField(max_length=500)
    pressure = models.CharField(max_length=500)
    rangeheight = models.CharField(db_column='rangeHeight', max_length=500)  # Field name made lowercase.
    encryptedkey = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'drone'

# Create your models here.
class User(models.Model):
    username = models.CharField(primary_key=True, max_length=20)
    password = models.CharField(max_length=20, blank=True, null=True)
    key = models.FileField()

    class Meta:
        managed = False
        db_table = 'user'
        
    def __str__(self): # 이 함수 추가
        return self.id  # User object 대신 나타낼 문자 

class keyfield(models.Model):
    skey = models.FileField(upload_to="post/keys")
    
        