from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_

#from django.contrib.auth.models import User
from .models import Room, Message
#from django.contrib.auth.decorators import login_required
import requests

#@login_required(login_url="login")
def index(request):
    try:
        # Kullanıcı listesini almak için user_service_url kullanılır
        user_service_url = "http://user_service_url"
        user_list_url = f"{user_service_url}/api/users/"
        response = requests.get(user_list_url)
        if response.status_code == 200:
            all_users = response.json()  # JSON formatındaki kullanıcı listesi
            # Kendiniz dışındaki kullanıcıları filtreleyin
            users = [user for user in all_users if user["username"] != request.user.username]
        else:
            users = []
    except Exception as e:
        print(f"Error fetching users: {e}")
        users = []

    return render(request, "src/index.html", {"users": users})

#@login_required(login_url="login")
def room(request, room_name):
    room = Room.objects.get(id=room_name)
    messages = Message.objects.filter(room=room)
    users = [
        fetch_user_data(room.first_user_id),
        fetch_user_data(room.second_user_id)
    ]

    return render(request, "src/room_v2.html", {
        'room_name': room_name,
        'room': room,
        'users': users,
        'messages': messages
    })

#@login_required(login_url="login")
def start_chat(request, username):
    second_user = fetch_user_data(username) #kullanıcı adını alıp user_service'den user'ı çekiyor
    try:
        room = Room.objects.get(first_user_id=request.user.id, second_user_id=second_user["id"])
    except Room.DoesNotExist:
        try:
            room = Room.objects.get(first_user_id=second_user["id"], second_user_id=request.user.id)
        except Room.DoesNotExist:
            room = Room.objects.create(first_user_id=request.user.id, second_user_id=second_user["id"])
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

def fetch_user_data(user_name): #user_name'i alıp user_service'den user'ı çekiyor
    user_service_url = "http://user_service_url"
    user_list_url = f"{user_service_url}/api/users/"
    response = requests.get(user_list_url)
    if response.status_code == 200:
       return response.json()
    else:
       raise Exception(f"User not found with username: {user_name}")
    
