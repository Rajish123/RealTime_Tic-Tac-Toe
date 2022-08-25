from multiprocessing import context
from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages

# Create your views here.

def home(request):
    if request.method == "POST":
        username = request.POST.get('username')
        option = request.POST.get('option')
        room_code = request.POST.get('room_code')

        if option == "1":
            game = Game.objects.filter(room_code = room_code).first()

            if game is None:
                messages.success(request,"Room Code not found!")
                return redirect('/')

            if game.is_over:
                messages.success(request,'Game is over')
                return redirect('/')

            # at this stage we have opponent
            game.game_opponent = username
            game.save()
        else:
            game = Game(game_creator = username, room_code = room_code)
            game.save()
            return redirect('/play/' + room_code +'?username=' + username)

    return render(request,'home/home.html')


def play(request,room_code):
    # get data from query string
    username = request.GET.get('username')
    context = {'room_code':room_code, 'username':username}
    return render(request,'home/play.html',context)
