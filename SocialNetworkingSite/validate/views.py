import bcrypt
from django.shortcuts import redirect, render
from .models import UserInfo, Userprofile
from karamel.views import blogfeed

# Create your views here.
def index(request):
    return render(request, "home.html")

def login(request):
    return render(request, "login.html")

def signup(request):
    return render(request, "signup.html")

def about(request):
    return render(request, "about.html")

def register(request):

    #Fetching all data comming from post method
    name = request.POST['name']
    email = request.POST['email']
    mobile = request.POST['mobile']
    dob = request.POST['dob']
    gender = request.POST['gender']
    username = request.POST['uname']
    password = request.POST['pass']
 
    #duplicate username check
    if UserInfo.objects.filter(username = username).exists():
        context = {"duplicate_user": "Username already taken!!!"}
        print(context)
        return render(request, "signup.html", context)

    #password encryption
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14))
    #Add to the database
    userinfo = UserInfo.objects.create(name = name, email = email, mobile = mobile, gender = gender, dob = dob, username = username, password = hashed_pw.decode('utf-8'))
    userinfo.save()
    return render(request, "setup.html", {"username": username})



def auth(request):
    #Method Check
    if request.method == "POST":
        #Fetching Data
        username = request.POST['uname']
        password = request.POST['pass']

        
        #Database Check
    
        user = UserInfo.objects.filter(username=username).first()
        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                userprof = Userprofile.objects.filter(userinfo = user).first()
                request.session['username'] = user.username
                return redirect('/karamel')
            else:
                return render(request, "login.html", {"login_error":"Username and password does not match!!!"})

        else:
            return render(request, "login.html", {"login_error":"User with this username does not exists"})



def setup(request):
    if request.method == "POST":
        profile = Userprofile()
        username = request.POST['uname']
        userinfo = UserInfo.objects.filter(username = username).first()
        profile.userinfo = userinfo
        profile.status = request.POST['status']
        profile.bio = request.POST['bio']
        profile.pic = request.FILES['profilepic']
        profile.save()
        request.session['username'] = username

    return redirect('/karamel')

def logout(request):
    request.session['username'] = "undefined"
    return redirect('/')

