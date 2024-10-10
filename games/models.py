from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.hashers import make_password

# Create your models here.

class Game(models.Model):
    name = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to='thumbnails/')

    def __str__(self):
        return self.name

from django.db import models

class VisitorLog(models.Model):
    visitor_id = models.UUIDField()
    user = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL)
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.visitor_id} - {self.path} ({self.method}) - {self.ip_address} - {self.timestamp}"

class Player(models.Model):
    email = models.EmailField(unique=True)  
    password = models.CharField(max_length=128) 
    balance = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password) 

    def __str__(self):
        return f"Player {self.email} - Balance: {self.balance}"

    class Meta:
        ordering = ['-created_at']
