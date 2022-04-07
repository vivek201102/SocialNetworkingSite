from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from chat.models import friendmessage

from karamel.models import Friend
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from validate.models import UserInfo, Userprofile
from django.utils.crypto import get_random_string

# Create your views here.

def letchat(request):
    return redirect("/mychat")




def mychat(request):
    if request.session['username'] == "undefined":
        return redirect("/")
    username = request.session['username']
    friend = Friend.objects.filter(Q(touser = username, status = 'Friends') | Q(fromuser = username, status = 'Friends'))
    profile = []
    for i in friend:
        if i.touser == username:
            userinfo = UserInfo.objects.filter(username = i.fromuser).first()
            userprofile = Userprofile.objects.filter(userinfo = userinfo).first()
            profile.append(userprofile)

        if i.fromuser == username:
            userinfo = UserInfo.objects.filter(username = i.touser).first()
            userprofile = Userprofile.objects.filter(userinfo = userinfo).first()
            profile.append(userprofile)
    context = {
        "friends":friend,
        "profile":profile
    }
    return render(request, "mychat.html", context)

@csrf_exempt
def getchat(request):
    if request.method == 'POST':
        tochat = request.POST['chatto']
        fromchat  = request.session['username']
        message = friendmessage.objects.values().filter(Q(fromuser = fromchat, touser = tochat) | Q(fromuser = tochat, touser = fromchat))
        messagelist = list(message)
        return JsonResponse({"message": messagelist, "self": fromchat})


def sendchat(request):

    userFrom = request.session['username']
    userTo = request.POST['touser']
    message = request.POST['message']
    print(userFrom)
    print(userTo)
    print(message)
    messageObj = friendmessage(fromuser = userFrom, touser = userTo, message = message)
    print(messageObj)
    messageObj.save()
    return JsonResponse({"letsgo":"Apna message chala gaya"})