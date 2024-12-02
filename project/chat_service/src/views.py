from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_
from django.contrib.auth.models import User
from .models import Room, Message
from django.contrib.auth.decorators import login_required
import requests

#@login_required(login_url="login")
def index(request):

    users = User.objects.all().exclude(username=request.user)#kendimiz dışındaki kullanıcıları listelemek için
    return render(request, "src/index.html", {'users': users})

#@login_required(login_url="login")
def room(request, room_name):
    users = User.objects.all().exclude(username=request.user)
    room = Room.objects.get(id=room_name)
    messages = Message.objects.filter(room=room)

    return render(request, "src/room_v2.html", {
        'room_name': room_name,
        'room': room,
        'users': users,
        'messages': messages
})

#@login_required(login_url="login")
def start_chat(request, username):
    second_user = User.objects.get(username=username)
    try:
        room = Room.objects.get(first_user=request.user, second_user=second_user) #kullanıcılar arasında bir oda var mı kontrol et(konusmayı birinci kullanıcı başlatmışsa)
    except Room.DoesNotExist:
        try:
            room = Room.objects.get(second_user=request.user, first_user=second_user) #kullanıcılar arasında bir oda var mı kontrol et(konusmayı ikinci kullanıcı başlatmışsa)
        except Room.DoesNotExist:
            room = Room.objects.create(first_user=request.user, second_user=second_user)
    return redirect("room", room.id)


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user:
            login_(request, user)
            return redirect("index")
    
    return render(request, "src/login.html")

#def fetch_user_data(user_name): #user_name'i alıp user_service'den user'ı çekiyor
#    response = requests.get(f'http://localhost:8000/user/{user_name}/')
#    if response.status_code == 200:
#        return response.json()
#    else:
#        raise Exception(f"User not found with username: {user_name}")
    
