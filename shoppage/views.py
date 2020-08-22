from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Dress,Quickform,Contact,Userdetails,Orders
from django.core.files.storage import FileSystemStorage
from math import ceil
import stripe
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.
def index(request):
    allProds=[]
    vendorlist=[]
    catProds=Dress.objects.values('category','dress_id')
    cats={item['category'] for item in catProds}
    for cat in cats:
        prod=Dress.objects.filter(category=cat)
        for i in range(len(prod)):
            if(prod[i].vendor_name not in vendorlist):
                vendorlist.append(prod[i].vendor_name)
    for cat in cats:
        prod=Dress.objects.filter(category=cat)
        n=len(prod)
        nSlides=n//4 + ceil((n/4)-(n//4)) 
        allProds.append([prod,range(1,nSlides),nSlides])
    params={'allProds':allProds,'vendors':vendorlist}
    return render(request,'shoppage/index.html',params)
def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.desc.lower() or query in item.dress_name.lower() or query in item.category.lower() or query in item.vendor_name.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Dress.objects.values('category', 'dress_id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Dress.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shoppage/search.html', params)
def postad(request):
    if request.method=="POST":
        vendor_name=request.POST.get('vendor_name','')
        dress_name=request.POST.get('dress_name','')
        category=request.POST.get('category','')
        desc=request.POST.get('desc','')
        price=request.POST.get('price','')
        colours=request.POST.get('colours','')
        size=request.POST.get('size','')
        quantity=request.POST.get('quantity','')
        material=request.POST.get('material','')
        stitching=request.POST.get('stitching','')
        contact=request.POST.get('contact','')
        image=request.FILES['image']
        fs=FileSystemStorage()
        im=fs.save(image.name,image)
        dress=Dress(dress_name=dress_name,category=category,desc=desc,price=price,contact=contact,colours=colours,quantity=quantity,size=size,material=material,stitching=stitching,image=im)
        dress.save()
    return render(request,"shoppage/postad.html")
def productview(request,myid):
    product=Dress.objects.filter(dress_id=myid)
    return render(request,"shoppage/prodview.html",{'product':product[0]})
def quickform(request):
    if request.method=="POST":
        dress_name=request.POST.get('dress_name','')
        dress_id=request.POST.get('dress_id','')
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phonenumber=request.POST.get('phonenumber','')
        address=request.POST.get('address','')
        city=request.POST.get('city','')
        state=request.POST.get('state','')
        zipcode=request.POST.get('zipcode','0')
        product=Dress.objects.filter(dress_id=dress_id) 
        quickform=Quickform(dress_name=dress_name,dress_id=dress_id,name=name,email=email,phonenumber=phonenumber,address=address,city=city,state=state,zipcode=zipcode)
        quickform.save()
    return render(request,"shoppage/prodview.html",{'product':product})
def categoryview(request,category):
    if category=='bridaldress':
        category="Bridal dress"
    elif category=="fancydress":
        category="Fancy Dress"
    else:
        category="Party Dress"
    categoryview=Dress.objects.filter(category=category)
    return render(request,"shoppage/category.html",{'product':categoryview})
def contact(request):
    if request.method=="POST":
        name=request.POST.get('name','')
        number=request.POST.get('number','')
        email=request.POST.get('email','')
        desc=request.POST.get('desc','')
        contact=Contact(name=name,number=number,email=email,desc=desc)
        contact.save()
    return render(request,"shoppage/contact.html") 
def about(request):
    return render(request,"shoppage/about.html")
def login(request):
    return render(request,"shoppage/login.html")
def userdetails(request):
    if request.method=="POST":
        email=request.POST.get('email','')
        password=request.POST.get('password','')
        status=request.POST.get('status','')
        userdetails=Userdetails(email=email,password=password,status=status)
        userdetails.save()
    return render(request,"shoppage/signup.html")
def signin(request):
    test=False
    if request.method=="POST":
        email=request.POST.get('email','')
        password=request.POST.get('password','')
        User=Userdetails.objects.filter(email=email,password=password)
        userlength=len(User)
        if(userlength != 0):
            test=True
            return render(request,'shoppage/index.html',{'test':test})
        else:
            param=True
        return render(request,'shoppage/login.html',{'test':param})
            #return redirect('',{'test':test}) 
    return render(request,"shoppage/login.html")

def checkout(request):
    if request.method=="POST":
        thanks=False
        items_json=request.POST.get('items_json','')
        amount=request.POST.get('amount','')
        name=request.POST.get('name','')
        phonenumber=request.POST.get('phonenumber','') #there is no default value
        email=request.POST.get('email','')
        address=request.POST.get('address1','')+" "+request.POST.get('address2','')
        city=request.POST.get('city','')
        state=request.POST.get('state','')
        zip_code=request.POST.get('zip_code','')
        orders=Orders(amount=amount,items_json=items_json,name=name,phonenumber=phonenumber,email=email,address=address,state=state,zip_code=zip_code,city=city)
        logincheck=Userdetails.objects.filter(email=email)
        cats=len(logincheck)
        if cats == 0:
            return render(request,"shoppage/login.html")
        if (name and phonenumber and email and city and state and address and orders and zip_code) == "":
            thanks=True
            return render(request,"shoppage/checkout.html")
        orders.save()
        return render(request, 'shoppage/stripee.html', {'amount':amount,'thanks':thanks,'email':email})

    return render(request,'shoppage/checkout.html')
def stripee(request):
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == 'POST':
        token = request.POST.get('stripeToken', False)
        email=request.POST.get('emailid','')
        amount=request.POST.get('amount','')
        if token:
            try:
                charge = stripe.Charge.create(
                    amount=100+int(amount),
                    currency='usd',
                    description=email,
                    source=token,
                )
              
                return redirect('ShopHome') 
            except Exception as e:
               print("card error",e)
    return render(request, 'shoppage/stripee.html')
def vendorsearch(request,vendorname):
    categoryview=Dress.objects.filter(vendor_name=vendorname)
    return render(request,"shoppage/category.html",{'product':categoryview,'status':True})