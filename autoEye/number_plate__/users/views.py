from django.shortcuts import redirect, render
from users.models import Car, CarLogin
import difflib
from django.shortcuts import render
from django.http import JsonResponse
import json
from django.http import JsonResponse
from difflib import SequenceMatcher
from django.core.exceptions import ObjectDoesNotExist
import subprocess


def index(request):
    total_cars = Car.objects.count()
    print("00000000000000",total_cars)  # Count the total number of cars
    return render(request, 'index.html', {'total_cars': total_cars})


def available_slot(request):
    total_cars = Car.objects.count()
    print("00000000000000",total_cars)  # Count the total number of cars
    return render(request, 'available_slot.html', {'total_cars': total_cars})


def home(request):
   # Count the total number of cars
    return render(request, 'home.html', )


def extract_text(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        extracted_text = data.get('text', '')
        upload_time = data.get('upload_time', '')

        print('extracted_text:', extracted_text)
        print('upload_time:', upload_time)

        # Fetch only registered cars from the database
        registered_cars = Car.objects.all()

        matching_cars_data = []
        total_cars = Car.objects.count()
        for car in registered_cars:
            match_ratio = SequenceMatcher(None, extracted_text, car.extracted_data).ratio()
            print(match_ratio)
            if match_ratio > 0.2:  # Adjust the threshold as needed
                try:
                    subprocess.run(["python3", "/home/omkar/servo.py", "--angle", "120"], check=True)
                    car_login = Car.objects.filter(number_plate=car.number_plate).latest('entered_timings')
                    time_difference = car.entered_timings

                    matching_cars_data.append({
                        'Username': car.username,
                        'Car model': car.car_name,
                        'Number plate': car.number_plate,
                        'In time': upload_time  # Include upload time in the response
                    })
                except ObjectDoesNotExist:
                    # This block will execute if the car is not found in CarLogin
                    matching_cars_data.append({
                        'status': 'error',
                        'message': 'Car not registered. Please register your car.'
                    })

        if not matching_cars_data:  # If no matching registered cars were found
            matching_cars_data.append({
                'status': 'error',
                'message': 'Do register.'
            })

        return JsonResponse({'status': 'success', 'matching_cars': matching_cars_data,'total_cars':total_cars})

    return JsonResponse({'status': 'error', 'matching_cars': 'Do register'}, status=400)

def registration(request):
    if request.method == 'POST':
        modal = request.POST.get('model')
        number_plate = request.POST.get('number_plate')
        extracted_data = request.POST.get('extracted_text')
        Username = request.POST.get('Username')
        image=request.FILES.get('image')
        car_details=Car.objects.create(car_name=modal,username=Username,number_plate=number_plate,extracted_data=extracted_data,image=image)
        if car_details:
             return redirect('index')
    return render(request,'registration.html')


def getin(request):
    if request.method == 'POST':
        number_plate = request.POST.get('number_plate')
        
        Username = request.POST.get('Username')
        car_details=CarLogin.objects.create(username=Username,number_plate=number_plate)
        if car_details:
            return redirect('index')
    return render(request,'getin.html')
