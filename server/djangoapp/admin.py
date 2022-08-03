from django.contrib import admin
# from .models import related models
from .models import Car, CarMake


# Register your models here.

# CarModelInline class
"""
    carMake = models.ForeignKey(CarMake,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    dealer_id = models.IntegerField()
    car_type = models.CharField(max_length=30)
    year = models.IntegerField()
"""
class CarInline(admin.StackedInline):
    model = Car
    list_display = ['name', 'dealer_id', 'car_type', 'year']

class CarMakeInline(admin.StackedInline):
    model = CarMake
    list_display = ['name', 'description']

# CarModelAdmin class
class CarAdmin(admin.ModelAdmin):
    list_display = ['name', 'dealer_id', 'car_type', 'year']

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarInline]
    list_display = ['name', 'description']
    search_fields = ['name']


# Register models here
admin.site.register(Car, CarAdmin)
admin.site.register(CarMake,CarMakeAdmin)