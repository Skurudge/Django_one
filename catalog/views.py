from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'home.html')

def contacts(request):
    return render(request, 'contacts.html')

def my_contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение {message} и телефон {phone} получены.")
    return render(request, 'contacts.html')
