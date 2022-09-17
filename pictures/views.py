import imp
from multiprocessing import context
from unicodedata import category, name 
from django.shortcuts import render , redirect
from .models import Category, Image, Location
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required




def loginPage(request):

    if request.method == 'POST':
        username= request.POST.get('username')
        password= request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username Or Password incorrect!! Try Again.!!!')
    context = {}
    return render(request, 'pictures/login.html', context )

def logoutPage(request):
    logout(request)
    return redirect('login/')

@login_required(login_url='login/')
def index(request):
    images = Image.objects.all()
    locations = Location.get_locations()
    print(locations)
    return render(request, 'pictures/index.html', {'images': images[::-1], 'locations': locations})

@login_required(login_url='login/')
def image_location(request, location):
    images = Image.filter_by_location(location)
    print(images)
    return render(request, 'pictures/location.html', {'location_images': images})

@login_required(login_url='login/')
def addPhoto(request):
    categories = Category.objects.all()
    locations = Location.objects.all()
    
    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')


        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                
                name=data['category_new'])
        else:
            category = None
            
        if data['location'] != 'none':
            locations = Location.objects.get(id=data['location'])
        elif data['location_new'] != '':
            locations, created = Location.objects.get_or_create(
                name=data['location_new'])
        else:
            locations = None


        for image in images:
            photo = Image.objects.create(
                category=category,
                description=data['description'],
                image=image,
                location = locations,
                name = data['name'],
            )

        return redirect('/')

    


    context = {'categories' : categories,
     'locations': locations}
    return render(request, 'pictures/add.html', context)



@login_required(login_url='login/')
def search_results(request):
    if 'imagesearch' in request.GET and request.GET["imagesearch"]:
        category = request.GET.get("imagesearch")
        searched_images = Image.search_by_category(category)
        message = f"{category}"
        print(searched_images)
        return render(request, 'pictures/search_results.html', {"message": message, "images": searched_images})
    else:
        message = "You haven't searched for any image category"
        return render(request, 'pictures/search_results.html', {"message": message})
