from asyncio.windows_events import NULL
import re
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from validate.models import UserInfo, Userprofile
from .models import Blogdetails, Friend
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
# Create your views here.

def karamel(request):
    if request.session['username'] == "undefined":
        return redirect("/")
    username = request.session['username']
    userinfo = UserInfo.objects.get(username = username)
    userprofile = Userprofile.objects.get(userinfo = userinfo)
    request.POST._mutable = True
    request.POST['userprof'] = userprofile
    request.POST._mutable = False
    return blogfeed(request)

def blogfeed(request):
    if request.session['username'] == "undefined":
        return redirect("/")
    username = request.session['username']
    userinfo = UserInfo.objects.get(username = username)
    userprofile = request.POST['userprof']
    blogs = Blogdetails.objects.all().order_by("-dandt")
    return render(request, "blogfeed.html", {"profile": userprofile, "blogs": blogs})

def blogform(request):
    if request.session['username'] == "undefined":
        return redirect("/")
    return render(request, "uploadblog.html")

def uploadblog(request):
    if request.session['username'] == "undefined":
        return redirect("/")
    if request.method == "POST":
        username = request.session['username']
        title = request.POST['title']
        desc = request.POST['blogdes']
        blogpic = request.FILES['blogpic']
        blogref = request.POST['blogref']
        userinfo = UserInfo.objects.get(username = username)
        now = datetime.now()
        dt = now.strftime("%d/%m/%Y %H:%M:%S")
        blogdetail = Blogdetails.objects.create(userinfo = userinfo, title = title, description = desc, blogpic = blogpic, blogref = blogref, dandt = dt)
        request.POST._mutable = True
        request.POST['userprof'] = Userprofile.objects.get(userinfo = userinfo)
        request.POST._mutable = False
        return redirect('/karamel')

    
def updateform(request):
    if request.session['username'] == "undefined":
        return redirect("/")
    username = request.session['username']
    userprof = Userprofile.objects.get(userinfo = UserInfo.objects.get(username = username))
    return render(request, "updateprofile.html", {"profile": userprof})

def changeprofile(request):
    if request.session['username'] == "undefined":
        return redirect("/")
    if request.method == "POST":
        pic = request.FILES['profilepic']
        username = request.POST['username']
        status = request.POST['status']
        bio = request.POST['bio']

        if UserInfo.objects.get(username = username) == None or request.session['username'] == username:
            userinfo = UserInfo.objects.get(username = username)
            userprofile = Userprofile.objects.get(userinfo = userinfo)
            userinfo.username = username
            userprofile.userinfo = userinfo
            userprofile.status = status
            userprofile.pic = pic
            userprofile.bio = bio
            userinfo.save()
            userprofile.save() 
        else:
            return render(request, 'updateprofile.html', {"error":"username is already taken"})


#Searching user
def addfriend(request):
    if request.session['username'] == "undefined":
        return redirect("/")
    if request.method == "POST":
        username = request.session['username']
        myinfo = UserInfo.objects.filter(username = username).first()
        name = request.POST['name']
        friendlist = Friend.objects.values().filter(Q(fromuser = username) | Q(touser = username))
        flist = list(friendlist)
        userinfo = UserInfo.objects.values().filter(Q(name__icontains = name) | Q(username__icontains = name))
        userinfo2 = UserInfo.objects.filter(Q(name__icontains = name) | Q(username__icontains = name))
        userinfolist = list(userinfo)
        userprofile = []
        for i in userinfo2:
            userprof = Userprofile.objects.filter(userinfo_id = i.id).first()
            image = userprof.pic
            userprofile.append(str(image))

        return JsonResponse({"msg":"Found User with username is", "infolist":userinfolist, "profilelist":userprofile, "my": username, "friends": flist})
    else:
        return render(request, "addfriend.html")


#Request sent fromhere
@csrf_exempt
def linkfriend(request):
    if request.session['username'] == "undefined":
        return redirect("/")
    if request.method == "POST":
        touser = request.POST['username']
        fromuser = request.session['username']
        userinfo = UserInfo.objects.filter(username = fromuser).first()
        friend = Friend(userinfo = userinfo, fromuser = fromuser, touser = touser)
        friend.save()
        return JsonResponse({"msg":"Requested", "user":touser})


#All friends details
def friend(request):
    if request.session['username'] == "undefined":
        return redirect("/")
    username = request.session['username']
    requestlist = Friend.objects.filter(touser = username, status = 'requested')
    friendlist = Friend.objects.filter(touser = username, status = "Friends")
    userprofilelist = []
    friendprofile = []
    for j in friendlist:
        friendinfo = UserInfo.objects.filter(username = j.fromuser).first()
        prof = Userprofile.objects.filter(userinfo = friendinfo).first()
        friendprofile.append(prof)

    friendlist2 = Friend.objects.filter(fromuser = username, status = "Friends")
    for k in friendlist2:
        friendinfo1 = UserInfo.objects.filter(username = k.touser).first()
        prof = Userprofile.objects.filter(userinfo = friendinfo1).first()
        friendprofile.append(prof)
    
    for i in requestlist:
        userinfo = UserInfo.objects.filter(username = i.fromuser).first()
        userprofile = Userprofile.objects.filter(userinfo = userinfo).first()
        userprofilelist.append(userprofile)
    return render(request, "friends.html", {"requests":requestlist,"profile":userprofilelist, "friendlist": friendprofile})

#All requestes are manage here
@csrf_exempt
def managereq(request):
    if request.session['username'] == "undefined":
        return redirect("/")
    username = request.session['username']
    fromuser = request.POST['fromuser']
    manage = request.POST['manage']
    if manage == "accept":
        print("In the accept")
        freq = Friend.objects.filter(fromuser = fromuser, touser = username).first()
        freq.status = "Friends"
        freq.save()
        return JsonResponse({"msg": "Request accepted"})
    
    elif manage == "decline":
        freq = Friend.objects.filter(fromuser = fromuser, touser = username).first()
        freq.delete()
        return JsonResponse({"msg": "Request declined"})
    
    elif manage == "blocked":
        print("In the blocked")
        freq = Friend.objects.filter(fromuser = fromuser, touser = username).first()
        freq.status = "blocked"
        freq.save()
        return JsonResponse({"msg": "user blocked"})

    elif manage == "remove":
        freq = Friend.objects.filter(fromuser = fromuser, touser = username).first()
        if(freq):
            freq.delete()
            return JsonResponse({"msg": "Friend Removed"})
        
        else:
            freq = Friend.objects.filter(fromuser = username, touser = fromuser).first()
            freq.delete()
            return JsonResponse({"msg": "Friend Removed"})