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
        chaturl = get_random_string(length=4)+tochat+fromchat+get_random_string(length=4)
        chatpage = friendchatpage.objects.filter(Q(fromuser = fromchat, touser = tochat) | Q(fromuser = tochat, touser = fromchat)).first()
        if chatpage is None:
            chatpage = friendchatpage(fromuser = fromchat, touser = tochat, url = chaturl)
            chatpage.save()
        return redirect('/'+chatpage.url+'/interface/?chatto='+tochat+'&chatfrom='+fromchat)

def chat(request, chaturl):
    fromuser = request.GET.get('chatfrom')
    touser = request.GET.get('chatto')
    frominfo = UserInfo.objects.filter(username = fromuser).first()
    toinfo = UserInfo.objects.filter(username = touser).first()
    fromprofile = Userprofile.objects.filter(userinfo = frominfo).first()
    toprofile = Userprofile.objects.filter(userinfo = toinfo).first()
    chatinstance = friendchatpage.objects.filter(Q(fromuser = fromuser, touser = touser) | Q(fromuser = touser, touser = fromuser))
    print(toinfo)
    print(frominfo)
    context = {
        "from":fromuser,
        "to":touser,
        "chatobj": chatinstance,
        "pageurl":chaturl,
        "fromprofile":fromprofile,
        "toprofile":toprofile
    }
    return render(request, "chat.html", context)

@csrf_exempt
def getmsg(request, chaturl):
    username = request.session['username']
    chatmsg = friendmessage.objects.values().filter(url = chaturl)
    chatlist = list(chatmsg)
    return JsonResponse({"msg": chatlist, "myname": username})

def sendchat(request):
    userFrom = request.POST['fromuser']
    userTo = request.POST['touser']
    url = request.POST['url']
    message = request.POST['message']
    messageObj = friendmessage(fromuser = userFrom, touser = userTo, url = url, message = message)
    messageObj.save()
    return HttpResponse("Message sent")