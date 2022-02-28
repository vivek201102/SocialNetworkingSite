from asyncio.windows_events import NULL
import re
from django.shortcuts import redirect, render
from validate.models import UserInfo, Userprofile
from .models import Blogdetails
# Create your views here.

def karamel(request):
    username = request.session['username']
    userinfo = UserInfo.objects.get(username = username)
    userprofile = Userprofile.objects.get(userinfo = userinfo)
    request.POST._mutable = True
    request.POST['userprof'] = userprofile
    request.POST._mutable = False
    return blogfeed(request)

def blogfeed(request):
    username = request.session['username']
    userinfo = UserInfo.objects.get(username = username)
    userprofile = request.POST['userprof']
    blogs = Blogdetails.objects.all()
    return render(request, "blogfeed.html", {"profile": userprofile, "blogs": blogs})

def blogform(request):
    return render(request, "uploadblog.html")

def uploadblog(request):
    if request.method == "POST":
        username = request.session['username']
        title = request.POST['title']
        desc = request.POST['blogdes']
        blogpic = request.FILES['blogpic']
        blogref = request.POST['blogref']
        userinfo = UserInfo.objects.get(username = username)
        blogdetail = Blogdetails.objects.create(userinfo = userinfo, title = title, description = desc, blogpic = blogpic, blogref = blogref)
        request.POST._mutable = True
        request.POST['userprof'] = Userprofile.objects.get(userinfo = userinfo)
        request.POST._mutable = False
        return redirect('/karamel')

    
def updateform(request):
    username = request.session['username']
    userprof = Userprofile.objects.get(userinfo = UserInfo.objects.get(username = username))
    return render(request, "updateprofile.html", {"profile": userprof})

def changeprofile(request):
    print("Entered")
    if request.method == "POST":
        pic = request.FILES['profilepic']
        username = request.POST['username']
        status = request.POST['status']
        bio = request.POST['bio']

        if UserInfo.objects.get(username = username) == None or request.session['username'] == username:
            print("ON")
            userinfo = UserInfo.objects.get(username = username)
            print("ON 1")
            userprofile = Userprofile.objects.get(userinfo = userinfo)
            print("ON 2")
            userinfo.username = username
            userprofile.userinfo = userinfo
            userprofile.status = status
            userprofile.pic = pic
            userprofile.bio = bio
            userinfo.save()
            userprofile.save()
            print("ON 4")
            return redirect('karamel')
        else:
            print("Second")
            return render(request, 'updateprofile.html', {"error":"username is already taken"})
    else:
        print("First If")