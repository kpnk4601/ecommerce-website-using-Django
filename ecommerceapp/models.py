from django.db import models

# Create your models here.
class Contact(models.Model):
    name =models.CharField(max_length=30)
    email=models.EmailField()
    desc=models.TextField(max_length=500)
    phonenumber=models.IntegerField(max_length=10)



    def __str__(self):
        return self.name
    

class Product(models.Model):
    product_id = models.AutoField  # Auto-incrementing ID
    product_name = models.CharField(max_length=100)  # Name of the product
    category = models.CharField(max_length=50)  # Category of the product
    subcategory = models.CharField(max_length=50)  # Subcategory of the product
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the product
    desc = models.TextField()  # Description of the product
    image = models.ImageField(upload_to='images/images')  # Path for the uploaded image

    def __str__(self):
        return self.product_name  # Returns the product name for display in the admin panel
