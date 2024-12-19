from django.shortcuts import render,redirect
from django.contrib import messages
from backend.models import categorydb
from frontend.models import adsdb,contactdb,UserProfile
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import FileSystemStorage

# Create your views here.
def backendindex(request):
    return render(request,"backendindex.html")
def creg(request):
    return render(request,"categ.html")

def save(request):
    if request.method == "POST":
        aa = request.POST.get('n')
        gg = request.POST.get('d')
        hh = request.FILES['img']
        obj = categorydb(name=aa,details=gg,image=hh)
        obj.save()
    messages.success(request, "Category Sucessfully Saved.!")
    return redirect(creg)
def disp(request):
    data = categorydb.objects.all()
    return render(request,"ctable.html",{'data':data})

def categdel(request,sid):
    x = (categorydb.objects.filter(id=sid))
    x.delete()
    messages.success(request, "Deleted Sucessfully.!")
    return redirect(disp)

def ceditpage(request,sid):
    std = categorydb.objects.get(id=sid)
    return render(request,"edit.html",{'std':std})

def ceditsave(request,sid):
    if request.method == "POST":
        aa = request.POST.get('n')
        gg = request.POST.get('d')
        try:
            i = request.FILES["img"]
            fs = FileSystemStorage()
            file = fs.save(i.name,i)
        except MultiValueDictKeyError:
            file = categorydb.objects.get(id=sid).image
        categorydb.objects.filter(id=sid).update(name=aa,details=gg,image=file)
        messages.success(request, "Updated Sucessfully.!")
        return redirect(disp)

def adstable(request):
    data = adsdb.objects.all()
    return render(request,"tableproducts.html",{'data':data})
def contacttable(request):
    data = contactdb.objects.all()
    return render(request,"contact.html",{'data':data})
def usertable(request):
    data = UserProfile.objects.all()
    return render(request,"usertable.html",{'data':data})