from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False,max_length=30)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class Car(models.Model):
    car_make = models.ForeignKey(CarMake,on_delete=models.CASCADE)
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    
    SEDAN = 'Sedan'
    SUV = 'SUV'
    ROADSTER = 'Roadster'
    CABRIOLET = 'Cabriolet'
    PICKUP = 'Pickup'

    CAR_TYPES = [
        (SEDAN,'Sedan'),
        (SUV,'SUV'),
        (ROADSTER,'Roadster'),
        (CABRIOLET,'Cabriolet'),
        (PICKUP,'Pickup'),
    ]

    car_type = models.CharField(max_length=30, choices=CAR_TYPES, default=SEDAN)

    current_year = int(now().strftime("%Y"))

    year = models.IntegerField(default=current_year,validators=[MaxValueValidator(current_year), MinValueValidator(current_year-50)])

    def __str__(self):
        return (self.name + ", " + str(self.car_make))
# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, id, city, state, st, address, zip, lat, long, short_name, full_name):
        # Dealer id
        self.id = id
        # Dealer city
        self.city = city
        # Dealer state
        self.state = state
        # Dealer state
        self.st = st
        # Dealer address
        self.address = address
        # Dealer zip
        self.zip = zip
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer Full Name
        self.full_name = full_name

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id
