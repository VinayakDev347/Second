from django.shortcuts import render, HttpResponse, redirect
from frontend.models import UserProfile, Friends, Messages, adsdb, contactdb, wishlistdb
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from frontend.serializers import MessageSerializer
from backend.models import categorydb
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

#Mail

from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
def userlogin(request):
    return render(request,"login.html")


def usave(request):
    if request.method == "POST":
        uu = request.POST.get('un')
        nn = request.POST.get('n')
        mm = request.POST.get('m')
        ee = request.POST.get('e')
        pp = request.POST.get('pa')
        ii = request.FILES['uimage']
        if UserProfile.objects.filter(email=ee).exists():
            messages.error(request,'email already exists.!')
            return redirect(userlogin)
        else:
            if UserProfile.objects.filter(username=uu).exists():
                messages.error(request, 'Username already exists.!')
                return redirect(userlogin)
            else:
                obj = UserProfile(username=uu, name=nn,mob=mm,email=ee,password=pp,img=ii)
                obj.save()
                subject = 'Welcome to Secondstore'
                message = ('We re thrilled to have you join the Secondstore community🎉.This is just a quick note to say thank you for signing up. We re excited to see you start exploring all that Secondstore has to offer.')
                recipient = ee
                send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
                return redirect(userlogin)


def ulogin(request):
    if request.method == "POST":
        ee = request.POST.get('n')
        pwd = request.POST.get('pas')
        if UserProfile.objects.filter(username=ee,password=pwd).exists():
            request.session['username']= ee
            request.session['password']= pwd
            return redirect(homepage)
        else:
            messages.error(request, 'Invalid Data.!')
            return redirect(userlogin)
    return redirect(userlogin)


def ulogout(request):
    del request.session['username']
    del request.session['password']
    return redirect(userlogin)

#Message
def getFriendsList(id):
    """
    Get the list of friends of the  user
    :param: user id
    :return: list of friends
    """
    try:
        user = UserProfile.objects.get(id=id)
        ids = list(user.friends_set.all())
        friends = []
        for id in ids:
            num = str(id)
            fr = UserProfile.objects.get(id=int(num))
            friends.append(fr)
        return friends
    except:
        return []


def getUserId(username):
    """
    Get the user id by the username
    :param username:
    :return: int
    """
    use = UserProfile.objects.get(username=username)
    id = use.id
    return id


def index(request):
    nam = UserProfile.objects.get(username=request.session['username']).name
    username = request.session['username']
    id = getUserId(username)
    friends = getFriendsList(id)
    return render(request, "Base.html", {'friends': friends, 'nam': nam})



def addfriend(request, name):
    """
    Add a user to the friend's list
    :param request:
    :param name:
    :return:
    """

    username = request.session['username']
    id = getUserId(username)
    friend = UserProfile.objects.get(username=name)
    curr_user = UserProfile.objects.get(id=id)
    print(curr_user.name)
    ls = curr_user.friends_set.all()
    flag = 0
    for username in ls:
        if username.friend == friend.id:
            flag = 1
            break
    if flag == 0:
        print("Friend Added!!")
        curr_user.friends_set.create(friend=friend.id)
        friend.friends_set.create(friend=id)
    return redirect(index)


def chat(request, username):
    """
    Get the chat between two users.
    :param request:
    :param username:
    :return:
    """
    nam = UserProfile.objects.get(username=request.session['username']).name
    friend = UserProfile.objects.get(username=username)
    id = getUserId(request.session['username'])
    curr_user = UserProfile.objects.get(id=id)
    messages = Messages.objects.filter(sender_name=id, receiver_name=friend.id) | Messages.objects.filter(sender_name=friend.id, receiver_name=id)
    if request.method == "GET":
        friends = getFriendsList(id)
        return render(request, "messages.html",{'messages': messages,'friends': friends,'curr_user': curr_user, 'friend': friend,'nam':nam})


@csrf_exempt
def message_list(request, sender=None, receiver=None):
    if request.method == 'GET':
        messages = Messages.objects.filter(sender_name=sender, receiver_name=receiver, seen=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.seen = True
            message.save()
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

#website

def homepage(request):
    if 'username' in request.session:
        uname = UserProfile.objects.get(username=request.session['username']).name
        v = categorydb.objects.get(id=1).name
        e = categorydb.objects.get(id=2).name
        m = categorydb.objects.get(id=3).name
        fu = categorydb.objects.get(id=4).name
        j = categorydb.objects.get(id=5).name
        r = categorydb.objects.get(id=6).name
        a = categorydb.objects.get(id=7).name
        ed = categorydb.objects.get(id=8).name
        lap = categorydb.objects.get(id=9).name
        se = categorydb.objects.get(id=10).name
        use = UserProfile.objects.all()
        pro = adsdb.objects.exclude(username=request.session['username'])
        late = adsdb.objects.exclude(username=request.session['username'])[::-1][:3]
        u = 0
        p = 0
        ea = 0
        ka = 0
        th = 0
        ko = 0
        tv = 0
        al = 0
        for i in use:
            u += 1
        for k in pro:
            p += 1
            if k.district == "Ernakulam":
                ea += 1
            if k.district == "Kannur":
                ka += 1
            if k.district == "Thrissur":
                th += 1
            if k.district == "Kozhikode":
                ko += 1
            if k.district == "Thiruvananthapuram":
                tv += 1
            if k.district == "Alappuzha":
                al += 1
        return render(request, "website/homepage.html",{'v': v, 'e': e, 'm': m, 'fu': fu, 'j': j, 'r': r, 'a': a, 'ed': ed, 'lap': lap, 'se': se, 'u': u,'p': p, 'pro': pro, 'late': late, 'ea': ea, 'ka': ka, 'th': th, 'ko': ko, 'tv': tv, 'al': al,'uname':uname})
    else:
        v = categorydb.objects.get(id=1).name
        e = categorydb.objects.get(id=2).name
        m = categorydb.objects.get(id=3).name
        fu = categorydb.objects.get(id=4).name
        j = categorydb.objects.get(id=5).name
        r = categorydb.objects.get(id=6).name
        a = categorydb.objects.get(id=7).name
        ed = categorydb.objects.get(id=8).name
        lap = categorydb.objects.get(id=9).name
        se = categorydb.objects.get(id=10).name
        use = UserProfile.objects.all()
        pro = adsdb.objects.all()
        late = adsdb.objects.all()[::-1][:3]
        u = 0
        p = 0
        ea = 0
        ka = 0
        th = 0
        ko = 0
        tv = 0
        al = 0
        for i in use:
            u += 1
        for k in pro:
            p += 1
            if k.district == "Ernakulam":
                ea += 1
            if k.district == "Kannur":
                ka += 1
            if k.district == "Thrissur":
                th += 1
            if k.district == "Kozhikode":
                ko += 1
            if k.district == "Thiruvananthapuram":
                tv += 1
            if k.district == "Alappuzha":
                al += 1
        for i in use:
            u += 1
        for k in pro:
            p += 1
        return render(request, "website/homepage.html",{'v': v, 'e': e, 'm': m, 'fu': fu, 'j': j, 'r': r, 'a': a, 'ed': ed, 'lap': lap, 'se': se, 'u': u,'p': p, 'pro': pro, 'late': late, 'ea': ea, 'ka': ka, 'th': th, 'ko': ko, 'tv': tv, 'al': al})


def post(request):
    if 'username' in request.session:
        cat = categorydb.objects.all()
        e = UserProfile.objects.get(username=request.session['username']).email
        f = UserProfile.objects.get(username=request.session['username']).mob
        g = UserProfile.objects.get(username=request.session['username']).img
        user = UserProfile.objects.get(username=request.session['username']).name
        return render(request, "website/postad.html", {'cat': cat, 'e': e, 'f': f, 'g': g, 'user': user})
    else:
        messages.error(request,"Please login")
        return redirect(homepage)

def products(request):
    if request.method == "POST":
        aa = request.POST.get('pn')
        bb = request.POST.get('bn')
        cc = request.POST.get('c')
        dd = request.POST.get('p')
        ee = request.POST.get('d')
        ff = request.POST.get('n')
        gg = request.POST.get('m')
        usern = request.POST.get('username')
        hh = request.POST.get('e')
        ii = request.POST.get('add')
        jj = request.POST.get('st')
        kk = request.POST.get('ci')
        ll = request.FILES['img']
        mm = request.FILES['img1']
        nn = request.FILES['img2']
    obj = adsdb(pname=aa,bname=bb,category=cc,price=dd,details=ee,uname=ff,username=usern,phone=gg,email=hh,address=ii,district=jj,city=kk,image=ll,image1=mm,image2=nn)
    obj.save()
    messages.success(request, "Item Sucessfully Saved.!")
    return redirect(post)

def myads(request):
    data = adsdb.objects.filter(username=request.session['username'])
    g = UserProfile.objects.get(username=request.session['username']).img
    n = 0
    for i in data:
        n += 1
    return render(request,"website/myads.html",{'data':data,'n':n,'g':g})

def allp(request):
    if 'username' in request.session:
        cat = categorydb.objects.all()
        data = adsdb.objects.exclude(username=request.session['username'])[::-1]
        no = 0
        for nu in data:
            no += 1
        paginator = Paginator(data, 4)
        page_number = request.GET.get('page')
        dataa = paginator.get_page(page_number)
        return render(request, "website/allproducts.html", {'dataa': dataa, 'cat': cat, 'no': no})
    else:
        cat = categorydb.objects.all()
        data = adsdb.objects.all()[::-1]
        no = 0
        for nu in data:
            no += 1
        paginator = Paginator(data, 4)
        page_number = request.GET.get('page')
        dataa = paginator.get_page(page_number)
        return render(request, "website/allproducts.html", {'dataa': dataa, 'cat': cat, 'no': no})

def editprod(request,pid):
    cat = categorydb.objects.all()
    data = adsdb.objects.get(id=pid)
    e = UserProfile.objects.get(username=request.session['username']).email
    f = UserProfile.objects.get(username=request.session['username']).mob
    g = UserProfile.objects.get(username=request.session['username']).img
    return render(request,"website/pedit.html",{'cat':cat,'data':data,'e':e,'f':f,'g':g})

def epsave(request,pid):
    if request.method == "POST":
        aa = request.POST.get('pn')
        bb = request.POST.get('bn')
        cc = request.POST.get('c')
        dd = request.POST.get('p')
        ee = request.POST.get('d')
        ff = request.POST.get('n')
        gg = request.POST.get('m')
        hh = request.POST.get('e')
        ii = request.POST.get('add')
        jj = request.POST.get('st')
        kk = request.POST.get('ci')
        try:
            i = request.FILES["img"]
            fs = FileSystemStorage()
            file = fs.save(i.name,i)
        except MultiValueDictKeyError:
            file = adsdb.objects.get(id=pid).image
        try:
            j = request.FILES["img1"]
            fs = FileSystemStorage()
            file1 = fs.save(j.name,j)
        except MultiValueDictKeyError:
            file1 = adsdb.objects.get(id=pid).image1
        try:
            k = request.FILES["img2"]
            fs = FileSystemStorage()
            file2 = fs.save(k.name,k)
        except MultiValueDictKeyError:
            file2 = adsdb.objects.get(id=pid).image2
        adsdb.objects.filter(id=pid).update(pname=aa,bname=bb,category=cc,price=dd,details=ee,uname=ff,phone=gg,email=hh,address=ii,district=jj,city=kk,image=file,image1=file1,image2=file2)
        wishlistdb.objects.filter(pid=pid).update(pname=aa,bname=bb,category=cc,price=dd,details=ee,uname=ff,phone=gg,email=hh,address=ii,district=jj,city=kk,image=file,image1=file1,image2=file2)
        messages.success(request, "Updated Sucessfully.!")
        return redirect(myads)

def pdetails(request,pid):
    dataa = adsdb.objects.get(id=pid)
    un= adsdb.objects.get(id=pid).uname
    g = UserProfile.objects.get(name=un).img
    return render(request,"website/productdetails.html",{'dataa':dataa,'g':g})

def editprofile(request):
    g = UserProfile.objects.get(username=request.session['username']).img
    dataa = UserProfile.objects.get(username=request.session['username'])
    return render(request,"website/editprof.html",{'g':g,'dataa':dataa})
def updateprof(request,uid):
    if request.method == "POST":
        nn = request.POST.get('n')
        mm = request.POST.get('m')
        ee = request.POST.get('e')
        try:
            i = request.FILES["img"]
            fs = FileSystemStorage()
            file = fs.save(i.name, i)
        except MultiValueDictKeyError:
            file = UserProfile.objects.get(id=uid).img
        UserProfile.objects.filter(id=uid).update(name=nn, mob=mm, email=ee, img=file)
        ads = list(adsdb.objects.all())
        for ad in ads:
            if ad.username == request.session['username']:
                x = ad.id
                adsdb.objects.filter(id=x).update(uname=nn, phone=mm, email=ee)
                wishlistdb.objects.filter(pid=x).update(uname=nn, phone=mm, email=ee)
    messages.success(request, "Updated Successfully.!")
    return redirect(editprofile)

def myproduct(request,pid):
    dataa = adsdb.objects.get(id=pid)
    un = adsdb.objects.get(id=pid).uname
    g = UserProfile.objects.get(name=un).img
    return render(request, "website/productdetails.html", {'dataa': dataa, 'g': g})

def pdel(request,pid):
    w = (wishlistdb.objects.filter(pid=pid))
    w.delete()
    x = (adsdb.objects.filter(id=pid))
    x.delete()
    messages.success(request, "Deleted Sucessfully.!")
    return redirect(myads)

def contact(request):
    if 'username' in request.session:
        g = UserProfile.objects.get(username=request.session['username']).email
        return render(request,"website/contactpg.html",{'g':g})
    else:
        return render(request, "website/contactpg.html")

def csave(request):
    if 'username' in request.session:
        g = UserProfile.objects.get(username=request.session['username']).email
        if request.method == "POST":
            ss = request.POST.get('s')
            me = request.POST.get('m')
        obj = contactdb(name=request.session['username'], email=g, sub=ss, msg=me)
        obj.save()
        messages.success(request, "Successfully Uploaded.!")
        return redirect(contact)
    else:
        if request.method == "POST":
            nn = request.POST.get('n')
            ee = request.POST.get('e')
            ss = request.POST.get('s')
            me = request.POST.get('m')
        obj = contactdb(name=nn, email=ee, sub=ss, msg=me)
        obj.save()
        messages.success(request, "Successfully Uploaded.!")
        return redirect(contact)

def about(request):
    use = UserProfile.objects.all()
    pro = adsdb.objects.all()
    u=0
    p=0
    for i in use:
        u+=1
    for j in pro:
        p+=1
    return render(request,"website/aboutus.html",{'u':u,'p':p})

def catfilter(request,cn):
    if 'username' in request.session:
        cat = categorydb.objects.all()
        data = adsdb.objects.filter(category=cn).exclude(username=request.session['username'])
        paginator = Paginator(data, 3)
        page_number = request.GET.get('page')
        dataa = paginator.get_page(page_number)
        return render(request, "website/allproducts.html", {'dataa': dataa, 'cat': cat})
    else:
        cat = categorydb.objects.all()
        data = adsdb.objects.filter(category=cn)
        paginator = Paginator(data, 4)
        page_number = request.GET.get('page')
        dataa = paginator.get_page(page_number)
        return render(request, "website/allproducts.html", {'dataa': dataa, 'cat': cat})

def passchange(request):
    g = UserProfile.objects.get(username=request.session['username']).img
    dataa = UserProfile.objects.get(username=request.session['username'])
    return render(request,"website/passchange.html",{'dataa':dataa,'g':g})

def pasupd(request,uid):
    if request.method == "POST":
        nn = request.POST.get('n')
        cp = request.POST.get('pas')
        pp = request.POST.get('npas')
        if UserProfile.objects.filter(name=nn,password=cp).exists():
            UserProfile.objects.filter(id=uid).update(password=pp)
            messages.success(request, "Updated Sucessfully Please login.!")
            return redirect(userlogin)
        else:
            messages.warning(request, "Invalid Password.!")
            return redirect(passchange)

def priv(request):
    g = UserProfile.objects.get(username=request.session['username']).img
    return render(request,"website/privacypage.html",{'g':g})

def deleteacc(request):
    if request.method == "POST":
        nn = request.POST.get('n')
        pp = request.POST.get('pas')
        if UserProfile.objects.filter(username=nn, password=pp).exists():
            w = (wishlistdb.objects.filter(username=nn))
            w.delete()
            v = (wishlistdb.objects.filter(user=nn))
            v.delete()
            y = (adsdb.objects.filter(username=nn))
            y.delete()
            x = (UserProfile.objects.filter(username=nn))
            x.delete()
            messages.success(request, "Deleted Sucessfully.!")
            return redirect(userlogin)
        else:
            messages.error(request, "Invalid Password.!")
            return redirect(priv)

def cityallp(request,dis):
    if 'username' in request.session:
        cat = categorydb.objects.all()
        data = adsdb.objects.exclude(username=request.session['username']).filter(district=dis)
        paginator = Paginator(data, 4)
        page_number = request.GET.get('page')
        dataa = paginator.get_page(page_number)
        return render(request, "website/allproducts.html", {'dataa': dataa, 'cat': cat})
    else:
        cat = categorydb.objects.all()
        data = adsdb.objects.filter(district=dis)
        paginator = Paginator(data, 4)
        page_number = request.GET.get('page')
        dataa = paginator.get_page(page_number)
        return render(request, "website/allproducts.html", {'dataa': dataa, 'cat': cat})

def searchpro(request):
    if 'username' in request.session:
        if request.method == "POST":
            pp = request.POST.get('pro')
            ll = request.POST.get('loc')
            cc = request.POST.get('cat')
        cat = categorydb.objects.all()
        if pp == '' and ll == '':
            data = adsdb.objects.filter(category__icontains=cc).exclude(username=request.session['username'])
        elif pp == '' and cc == '':
            data = adsdb.objects.filter(Q(city__icontains=ll) | Q(district__icontains=ll)).exclude(
                username=request.session['username'])
        elif ll == '' and cc == '':
            data = adsdb.objects.filter(Q(pname__icontains=pp) | Q(bname__icontains=pp)).exclude(
                username=request.session['username'])
        elif pp == '':
            data = adsdb.objects.filter(
                Q(category__icontains=cc) | Q(city__icontains=ll) | Q(district__icontains=ll)).exclude(
                username=request.session['username'])
        elif ll == '':
            data = adsdb.objects.filter(
                Q(pname__icontains=pp) | Q(bname__icontains=pp) | Q(category__icontains=cc)).exclude(
                username=request.session['username'])
        elif cc == '':
            data = adsdb.objects.filter(Q(pname__icontains=pp) | Q(bname__icontains=pp) | Q(city__icontains=ll) | Q(
                district__icontains=ll)).exclude(username=request.session['username'])
        else:
            data = adsdb.objects.filter(
                Q(pname__icontains=pp) | Q(bname__icontains=pp) | Q(category__icontains=cc) | Q(city__icontains=ll) | Q(
                    district__icontains=ll)).exclude(username=request.session['username'])
        paginator = Paginator(data, 4)
        page_number = request.GET.get('page')
        dataa = paginator.get_page(page_number)
        return render(request, "website/allproducts.html", {'dataa': dataa, 'cat': cat})
    else:
        if request.method == "POST":
            pp = request.POST.get('pro')
            ll = request.POST.get('loc')
            cc = request.POST.get('cat')
        cat = categorydb.objects.all()
        if pp == '' and ll == '':
            data = adsdb.objects.filter(category__icontains=cc)
        elif pp == '' and cc == '':
            data = adsdb.objects.filter(Q(city__icontains=ll) | Q(district__icontains=ll))
        elif ll == '' and cc == '':
            data = adsdb.objects.filter(Q(pname__icontains=pp) | Q(bname__icontains=pp))
        elif pp == '':
            data = adsdb.objects.filter(
                Q(category__icontains=cc) | Q(city__icontains=ll) | Q(district__icontains=ll))
        elif ll == '':
            data = adsdb.objects.filter(
                Q(pname__icontains=pp) | Q(bname__icontains=pp) | Q(category__icontains=cc))
        elif cc == '':
            data = adsdb.objects.filter(Q(pname__icontains=pp) | Q(bname__icontains=pp) | Q(city__icontains=ll) | Q(district__icontains=ll))
        else:
            data = adsdb.objects.filter(
                Q(pname__icontains=pp) | Q(bname__icontains=pp) | Q(category__icontains=cc) | Q(city__icontains=ll) | Q(district__icontains=ll))
        paginator = Paginator(data, 4)
        page_number = request.GET.get('page')
        dataa = paginator.get_page(page_number)
        return render(request, "website/allproducts.html", {'dataa': dataa, 'cat': cat})

def searchproducts(request):
    if 'username' in request.session:
        if request.method == "POST":
            pp = request.POST.get('pro')
        cat = categorydb.objects.all()
        data = adsdb.objects.filter(Q(pname__icontains=pp) | Q(bname__icontains=pp)).exclude(username=request.session['username'])
        paginator = Paginator(data, 4)
        page_number = request.GET.get('page')
        dataa = paginator.get_page(page_number)
        return render(request, "website/allproducts.html", {'dataa': dataa, 'cat': cat})
    else:
        if request.method == "POST":
            pp = request.POST.get('pro')
        cat = categorydb.objects.all()
        data = adsdb.objects.filter(Q(pname__icontains=pp) | Q(bname__icontains=pp))
        paginator = Paginator(data, 4)
        page_number = request.GET.get('page')
        dataa = paginator.get_page(page_number)
        return render(request, "website/allproducts.html", {'dataa': dataa, 'cat': cat})

def userp(request,un):
    if 'username' in request.session:
        data = adsdb.objects.filter(username=un)
        g = UserProfile.objects.get(username=request.session['username']).img
        name = UserProfile.objects.get(username=un).name
        ui = UserProfile.objects.filter(username=un)
        n = 0
        for i in data:
            n += 1
        return render(request, "website/othersprofile.html", {'data': data, 'n': n, 'g': g, 'name': name, 'ui': ui})
    else:
        data = adsdb.objects.filter(username=un)
        name = UserProfile.objects.get(username=un).name
        ui = UserProfile.objects.filter(username=un)
        n = 0
        for i in data:
            n += 1
        return render(request, "website/othersprofile.html", {'data': data, 'n': n, 'name': name, 'ui': ui})


def addwishlist(request, id):
    xx = list(wishlistdb.objects.all())
    for yy in xx:
        if yy.pid == id and yy.user == request.session['username']:
            return redirect(allp)
    else:
        aa = adsdb.objects.get(id=id).pname
        bb = adsdb.objects.get(id=id).bname
        cc = adsdb.objects.get(id=id).category
        dd = adsdb.objects.get(id=id).price
        ee = adsdb.objects.get(id=id).details
        ff = adsdb.objects.get(id=id).time
        gg = adsdb.objects.get(id=id).uname
        hh = adsdb.objects.get(id=id).username
        ii = adsdb.objects.get(id=id).phone
        jj = adsdb.objects.get(id=id).email
        kk = adsdb.objects.get(id=id).address
        ll = adsdb.objects.get(id=id).district
        mm = adsdb.objects.get(id=id).city
        nn = adsdb.objects.get(id=id).image
        oo = adsdb.objects.get(id=id).image1
        pp = adsdb.objects.get(id=id).image2
        obj = wishlistdb(pid=id, user=request.session['username'], pname=aa, bname=bb, category=cc, price=dd,
                         details=ee, time=ff, uname=gg, username=hh, phone=ii, email=jj, address=kk, district=ll,
                         city=mm, image=nn, image1=oo, image2=pp)
        obj.save()
        return redirect(allp)

def favads(request):
    data = wishlistdb.objects.filter(user=request.session['username'])
    g = UserProfile.objects.get(username=request.session['username']).img
    n = 0
    for i in data:
        n += 1
    return render(request, "website/favadd.html", {'data': data, 'n': n, 'g': g})

def deletewish(request,itemid):
    x = wishlistdb.objects.filter(id=itemid)
    x.delete()
    return redirect(favads)
