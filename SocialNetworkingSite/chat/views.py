from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from chat.models import friendchatpage, friendmessage

from karamel.models import Friend
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from validate.models import UserInfo, Userprofile
from django.utils.crypto import get_random_string

# Create your views here.
def mychat(request):
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
        friendchat = friendchatpage.objects.filter(Q(fromuser = fromchat, touser = tochat) | Q(fromuser = tochat, touser = fromchat)).first()
        if friendchat is None:
            url = get_random_string(length=4)+fromchat + tochat +get_random_string(length=4)
            friendchat = friendchatpage(fromuser = fromchat, touser = tochat, url = url)
            friendchat.save()
        message = friendmessage.objects.values().filter(url = friendchat.url)
        print(friendchat.url)
        messagelist = list(message)
        return JsonResponse({"message": messagelist, "self": fromchat})





def sendchat(request):
    userFrom = request.session['username']
    userTo = request.POST['touser']
    fd = friendchatpage.objects.filter(Q(fromuser = userFrom, touser = userTo) | Q(fromuser = userTo, touser = userFrom)).first()
    url = fd.url
    message = request.POST['message']
    messageObj = friendmessage(fromuser = userFrom, touser = userTo, url = url, message = message)
    messageObj.save()
    request.POST['chatto'] = userTo
    return getchat(request)