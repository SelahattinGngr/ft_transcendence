import json
from rest_framework.response import Response
from rest_framework import status
from .models import  GameHistory
from django.http import JsonResponse


# post -> usrname/userScore/aiScore/isWin
# isWin boolean olacak, user kazandıysa true kazanmadıysa false dönecek

# get -> son 10 maçın verileri dönecek
# http://localhost:8000/game/get-history/<username>

def save_game(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    try:
        data = json.loads(request.body)
        username = data.get("username")
        userScore = data.get("userScore")
        aiScore = data.get("aiScore")
        aiName = "MOULINETTE"
        isWin = data.get("isWin")

        game = GameHistory.objects.create(username=username, userScore=userScore, aiScore=aiScore, isWin=isWin, aiName=aiName)
        game.save()
        return JsonResponse({"message": "Game saved successfully"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def get_history(request, username):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try: 
        history = GameHistory.objects.filter(username=username).order_by("-id")[:10]
        history_data = list(history.values())
        return JsonResponse({"data": history_data}, safe=False, status=status.HTTP_200_OK)
    except GameHistory.DoesNotExist:
        return JsonResponse({"error": "No game history found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)