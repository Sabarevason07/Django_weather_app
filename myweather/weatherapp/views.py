from django.shortcuts import render,redirect, get_object_or_404
from .form import CityForm
from .models import City
import requests
from django.contrib import messages

# Create your views here.

def home(request):
    url='http://api.openweathermap.org/data/2.5/weather?q={},&appid=3b8f235d09f128b41221bec076ef81cb&units=metric'

    if request.method=="POST":
        form=CityForm(request.POST)        
        if form.is_valid():
            NCity=form.cleaned_data['name']            
            CCity=City.objects.filter(name=NCity).count()
            if CCity==0:
                res=requests.get(url.format(NCity)).json()                
                if res['cod']==200:
                    form.save()
                    messages.success(request," "+NCity+" Added Successfully...!!!")
                else: 
                    messages.error(request,"City Does Not Exists...!!!")
            else:
                messages.error(request,"City Already Exists...!!!")      

    form=CityForm()
    cities=City.objects.all()
    data=[]
    for city in cities:        
        res=requests.get(url.format(city)).json()   
        city_weather={
            'city':city,
            'temperature' : res['main']['temp'],
            'description' : res['weather'][0]['description'],
            'country' : res['sys']['country'],
            'icon' : res['weather'][0]['icon'],
        }
        data.append(city_weather)  
    context={'data' : data,'form':form}
    return render(request,"home.html",context)

def delete_city(request,CName):
    City.objects.get(name=CName).delete()
    messages.success(request," "+CName+" Removed Successfully...!!!")
    return redirect('Home')

def edit_city(request, CName):
    # Get the city object that needs to be edited
    city = get_object_or_404(City, name=CName)

    if request.method == "POST":
        form = CityForm(request.POST, instance=city)
        if form.is_valid():
            NCity = form.cleaned_data['name']
            CCity = City.objects.filter(name=NCity).exclude(id=city.id).count()  # Exclude current city from duplicate check

            if CCity == 0:
                url = 'http://api.openweathermap.org/data/2.5/weather?q={},&appid=3b8f235d09f128b41221bec076ef81cb&units=metric'
                res = requests.get(url.format(NCity)).json()

                if res['cod'] == 200:
                    form.save()
                    messages.success(request, f"{NCity} updated successfully!")
                    return redirect('Home')
                else:
                    messages.error(request, "City does not exist.")
            else:
                messages.error(request, "City already exists.")
    else:
        form = CityForm(instance=city)

    context = {
        'form': form,
        'city': city
    }
    return render(request, 'edit_city.html', context)