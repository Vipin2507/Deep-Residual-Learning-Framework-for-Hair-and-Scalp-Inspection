from django.db import models

class User(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=20, unique=True)  # username as text
    password = models.CharField(max_length=20)  # password as text (later you can hash it)

    def __str__(self):
        return self.username
