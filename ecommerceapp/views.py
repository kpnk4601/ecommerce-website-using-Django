from django.shortcuts import render, redirect
from ecommerceapp.models import Contact,Product  # Ensure the model name is capitalized
from django.contrib import messages
from math import ceil

# Create your views here.
def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nslides + 1), nslides])
        
    params = {'allprods': allProds}
    return render(request, "index.html", params)

def contact(request):  # Renamed to avoid name conflict
    if request.method == "POST":  # Fixed typo from 'methof' to 'method'
        name = request.POST.get("name")
        email = request.POST.get("email")
        pnumber = request.POST.get("pnumber")
        desc = request.POST.get("desc")
        
        # Create and save a new contact instance
        contact_instance = Contact(name=name, email=email, phonenumber=pnumber, desc=desc)
        contact_instance.save()
        
        messages.success(request, "Your message has been sent successfully!")  # Add success message
        return redirect('index')  # Redirect to the index page after submission
        
    return render(request, "contact.html")

def about(request):
    return render(request, "about.html")
