from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views import View  
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from django.core.mail import send_mail,EmailMessage
from django.db.models import Q
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
# Create your views here.

class Home(View):
    def get(self,request):
        return render(request,'home.html')
    

class Products_search(View):
    def get(self,request):
        data = Product_Category.objects.filter(Category_name__startswith="A")
        return render(request,'filter.html',{'data':data})
    

class Filter_Category(View):
    def get(self,request,query):
        if Product_Category.objects.filter(Category_name__startswith=query).exists():
          data = Product_Category.objects.filter(Category_name__startswith=query)
          l = {}
          a = ''
          for i in data:
              i = str(i)
              l[i]=i

              a += f'''
                <div class="col-md-4">
                  <a href="/filter_products/{i}" style="color: black">
                    <ul class="list-group">
                      <li class="list-group-item">
                        <b
                          >{i}
                          <div class="pull-right">
                            <i class="fa-solid fa-flask-vial fa-beat-fade"></i>
                          </div>
                        </b>
                      </li>
                    </ul>
                  </a>
                </div>
              '''
          # d = json.dumps(a)
          return JsonResponse(a,safe=False)
        else:
            a = """<h1 class="text-center my-2">No Product Found</h1>"""
            return JsonResponse(a,safe=False)

    
class Filter_products(View):
    def get(self,request,category):
        cat = Product_Category.objects.get(Category_name=category)
        data = Impurity_Chemicals.objects.filter(category=cat)
        return render(request,'category.html',{'data':data})
    

class Product_view(View):
    def get(self,request,slug):
        product = Impurity_Chemicals.objects.get(slug_id=slug)
        return render(request,'product_view.html',{'product':product})
    

class G_online_quote(View):
    def get(self,request):
        return render(request,'get_online_quote.html')
    
    def post(self,request):
      full_name = request.POST['full_name']
      email_id = request.POST['email_id']
      company_name = request.POST['company_name']
      contact_no = request.POST['contact_no']
      product_name = request.POST['product_name']
      chemical_name = request.POST['chemical_name']
      cas_number = request.POST['cas_number']
      quantity = request.POST['count'] + request.POST['quantity']
      
      try:
        structure = request.FILES['structure']
      except:
        structure = ""

      try:
        Get_online_quote.objects.create(full_name=full_name,email_id=email_id,company_name=company_name,contact_no=contact_no,product_name=product_name,chemical_name=chemical_name,cas_number=cas_number,structure=structure,quantity=quantity)
        
        messages.success(request,'Your response is saved')

        send_mail(
          "Online Quote Enquiry Recieved",
          f"We recieved your Online Quote for\n Product Name : {product_name} \n Chemical Name : {chemical_name} \n Cas No. : {cas_number} \n Quantity : {quantity} \n \n we will Contact you soon with the Next Update \n Thank You for Choosing Pharma Impurity and Chemicals",
          "kunal00.kr@gmail.com",
          [f"{email_id}"],
          fail_silently=False,
        ) 

        return redirect('home')
      
      except:
        messages.error(request,'Error Saving this information Please Try Again')
        return redirect('get_online_quote')
          
    
class faciities(View):
    def get(self,request):
        return render(request,'FACILITY.html')


class loginView(View):
    def get(self,request):
        return render(request,'login.html')
    
    def post(self,request):
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Invalid Email/Password Try Again!!')
            return redirect('login')
        
class Signupview(View):
    def get(self,request):
        return render(request,'signup.html')
    
    def post(self,request):
        username = request.POST['username']
        email = request.POST['email']
        mobile = request.POST['mobile']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            
            if User.objects.filter(username=username).exists():
                messages.warning(request,'Username Already Exists')
                return redirect('signup')

            elif User.objects.filter(email=email).exists():
                messages.warning(request,'Email Already Exists')
                return redirect('signup')
            
            else:
                User.objects.create_user(username=username,email=email,mobile=mobile,password=password)
                messages.success(request,"Account Created")
                redirect('login')
        else:
            return redirect('signup')

class logoutView(View):
    def get(self,request):
        logout(request)
        return redirect('login')


class about(View):
    def get(self,request):
        return render(request,'about.html')


class contact(View):
    def get(self,request):
        return render(request,'contact.html')
    
    def post(self,request):
        name = request.POST['name']
        email = request.POST['email']
        phone_no = request.POST['phone_no']
        message = request.POST['message']

        data = Contact_Us.objects.create(name=name,email=email,phone_no=phone_no,message=message)

        if data:
            messages.success(request,"Form Submitted")
            return redirect('home')
        else:
            messages.error(request,'Form not Submitted,Try Again')
            return redirect('contact')


@login_required(login_url="login")
def add2cart(request,slug):
    if request.user.is_authenticated:
      if request.method == "POST":
        pdata = Impurity_Chemicals.objects.get(slug_id=slug)
        quantity = int(request.POST['quantity'])
        if RFQ_list.objects.filter(Q(product_name=pdata.product_name) & Q(ordered_by=request.user)) :
            predata = RFQ_list.objects.get(Q(product_name=pdata.product_name) & Q(ordered_by=request.user))
            new_quantity = int(predata.quantity)+quantity
            RFQ_list(id=predata.id,product_name=pdata.product_name,quantity=new_quantity,ordered_by=request.user).save()
            return redirect('cart')
        else:
            RFQ_list.objects.create(product_name=pdata.product_name,quantity=quantity,ordered_by=request.user)
            return redirect('cart')
      else:
          return redirect('product_view',slug = slug)
    else:
          return redirect('login')        

class cart(View):
    def get(self,request):      
        if request.user.is_authenticated:
            product_img = Impurity_Chemicals.objects.all()
            cart_items = RFQ_list.objects.filter(ordered_by=request.user)  
            return render(request,'cart.html',{'cart_items':cart_items,'product_img':product_img})
        else:
            return redirect('login')

@login_required(login_url="login")
def cart_items_delete(request,pname):
    RFQ_list.objects.get(Q(product_name=pname) & Q(ordered_by=request.user)).delete()
    return redirect('cart')

class CheckOutConfirm(View):
    @login_required(login_url="login")
    def get(self,request):
        if RFQ_list.objects.filter(ordered_by=request.user).exists():
          cart_items = RFQ_list.objects.filter(ordered_by=request.user)  
          return render(request,'checkoutpage.html',{'cart_items':cart_items})
        else:
            return redirect('cart')

@login_required(login_url="login")    
def checkOut(request):
    if RFQ_list.objects.filter(ordered_by=request.user).exists():
        cart_items = RFQ_list.objects.filter(ordered_by=request.user)
        context = {"cart_items":cart_items,"user":request.user.username}
        messsage = get_template('checkoutdone.html').render(context)
        msg = EmailMessage(
          "Order details recieved",
          # f"We recieved your Order for\n Product Name : {i.product_name} \n  Quantity : {i.quantity} \n \n we will Contact you soon with the Next Update \n Thank You for Choosing Pharma Impurity and Chemicals",
          messsage,
          "kunal00.kr@gmail.com",
          [f"{request.user}","kunal00.kr@gmail.com"],
          # fail_silently=False,
        )
        msg.content_subtype ="html"
        msg.send()
        return redirect('cart')
    else:
        return redirect('cart')

class SearchProduct(View):
    def get(self,request):
        data = Impurity_Chemicals.objects.all().order_by('?')
        return render(request,'searchproduct.html',{'data':data})

    def post(self,request):
        searchinp = request.POST['searchinp']
        if Impurity_Chemicals.objects.filter(product_name__contains=searchinp).exists():
            data = Impurity_Chemicals.objects.filter(product_name__contains=searchinp)
            return render(request,'searchproduct.html',{'data':data})
        else:
            messages.warning(request,'No search Result')
            return redirect('search')