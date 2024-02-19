from django.db import models

# Create your models here.

class User(models.Model):
    name =models.CharField(max_length=50)
    username =models.CharField(max_length=20, unique=True)
    email =models.CharField(max_length=50)
    phone =models.CharField(max_length=20)
    password =models.CharField(max_length=20)
    status =models.CharField(max_length=20)
    change = models.IntegerField()
    emoji = models.IntegerField()

     

    def __str__(self):
        return self.name
    




# Create your models here.
class GameServer(models.Model):
    player1 =models.IntegerField()
    player2 =models.IntegerField()

    ans_player1 =models.CharField(max_length=20)
    ans_player2 =models.CharField(max_length=20)
    winner =models.CharField(max_length=20)


    player1Win =models.IntegerField()
    player2Win =models.IntegerField()
    status =models.CharField(max_length=20)
    
    cnt =models.IntegerField()
    player1_click =models.IntegerField()
    player2_click =models.IntegerField()

    change =models.IntegerField()

    player1name =models.CharField(max_length=50)
    player2name =models.CharField(max_length=50)


    emoji =models.IntegerField()


    emoji2 =models.IntegerField()


  

    def __str__(self):
        return self.status


 




