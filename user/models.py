from django.db import models

# Create your models here.
class User(models.Model):
    class Meta:
        db_table = 'user'
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=48,null=False)
    email = models.CharField(max_length=64,unique=True,null=False)
    password = models.CharField(max_length=128, null=False)


class Content(models.Model):
    class Meta:
        db_table = 'content'
    cid = models.AutoField(primary_key=True,null=False)
    content = models.TextField(null=False)
    tid = models.IntegerField(null=False)

class Title(models.Model):
    class Meta:
        db_table = 'title'
    tid = models.AutoField(primary_key=True,null=False)
    uid = models.IntegerField(null=False)
    title = models.CharField(max_length=128,null=False)
    postdate= models.DateTimeField(auto_now_add=True,null=False)
