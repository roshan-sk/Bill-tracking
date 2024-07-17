from django.db import models

class Bill(models.Model):
    name_of_item = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class Users(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    otp = models.IntegerField(null=True, blank=True)
    otp_expiration = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


# class Product(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     image = models.ImageField(upload_to='products/')

#     def __str__(self):
#         return self.title