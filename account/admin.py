from django.contrib import admin
from .models import Bill, Users

admin.site.register(Bill)
admin.site.register(Users)
# admin.site.register(Product)