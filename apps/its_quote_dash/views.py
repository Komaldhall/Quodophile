from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import datetime
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
now = datetime.datetime.today().strftime("%Y-%m-%d")


def register(request):
    if request.method == 'POST':
        
        form=request.POST
        errors = []
        if len(form['first_name']) < 2:
            errors.append('First name must be at least 2 characters.')
        if len(form['last_name']) < 2:
            errors.append('Last name must be at least 2 characters.')
        if len(form['password']) < 8:
            errors.append('Password must be at least 8 characters.')
        if not form['password'] == form['cpassword']:
            errors.append('Passwords do not match.')
        if not EMAIL_REGEX.match(form['email']):
            errors.append('Please provide a valid email') 
        if form['birthday']>now:
            errors.append("Birthday refers to a future date.")
        
        if errors:
            for e in errors:
                messages.error(request, e)
                
        else:        
            try:
                User.objects.get(email=form['email'])
                messages.error(request, 'Email already exists. Please Login!')
            except User.DoesNotExist:
                hashed_pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt())
                c_hashed_pw = hashed_pw.decode('utf-8')
                birthday=str(form['birthday'])
                User.objects.create(first_name=form['first_name'], last_name=form['last_name'], email=form['email'], password=c_hashed_pw, birth=birthday)
                messages.success(request,"You successfully registered. Please login!")
                return redirect('/')
        return redirect('/signup')          
    else:
        return render(request, 'its_quote_dash/signup.html')
    
    
def login(request):
    if request.method == 'POST':
        
        errors = []
        form=request.POST
        # if len(form['emaill']) < 0:
        #     errors.append('Please provide email')  
        if not EMAIL_REGEX.match(form['emaill']):
            errors.append('Please provide a valid email') 
        else:
            try:
                user=User.objects.get(email=form['emaill'])
                result = bcrypt.checkpw(request.POST['passwordl'].encode(), user.password.encode())
                if result:
                    request.session['user_id'] = user.id
                    return redirect('/dashboard')
                else:
                    messages.error(request, 'Password does not match.')    
            except User.DoesNotExist:
                messages.error(request, 'Email does not exists. Please signup.')
                return redirect('/')
        
        if errors:
            for e in errors:
                messages.error(request, e)   
        return redirect('/')  
    else:
        return render(request, 'its_quote_dash/index.html')

    

def logout(request):
    if not 'user_id' in request.session:
        messages.error(request, 'You need to login.')
        return redirect('/')
    request.session.clear()
    return redirect('/')  

def dashboard(request): 
    if not 'user_id' in request.session:
        messages.error(request, 'You need to login.')
        return redirect('/')
        
    user = User.objects.get(id=request.session['user_id'])
    quote = Quote.objects.all().order_by('-created_at')
    first_user = user.first_name.split()
    first_user = first_user[0][0]
    last_user = user.last_name.split()
    last_user = last_user[0][0]
    context = {
        'user': user,   
        'quote':quote,
        'first':first_user,
        'last':last_user,
    }

    return render(request,'its_quote_dash/dashboard.html', context)      

def add(request):
    
    if not 'user_id' in request.session:
        messages.error(request, 'You need to login.')
        return redirect('/')
    if request.POST:
        errors=[]
        
        form=request.POST
        if len(form['author'])<3:
            errors.append('Author must be at least 3 characters.')
        if len(form['quote']) < 10:
            errors.append('Quote must be at least 10 characters.')
      
        if errors:
            for e in errors:
                messages.error(request, e)
        else:
            Quote.objects.create(author=form['author'], quote=form['quote'], users_id=request.session['user_id'])                   
    user = User.objects.get(id=request.session['user_id'])
    first_user = user.first_name.split()
    first_user = first_user[0][0]
    last_user = user.last_name.split()
    last_user = last_user[0][0]
    context = {
        'first':first_user,
        'last':last_user,
    }

    return render(request,'its_quote_dash/newquote.html', context)      

def edit(request, user_id):
    if not 'user_id' in request.session:
        messages.error(request, 'You need to login.')
        return redirect('/')

    user=User.objects.get(id=user_id)    
    first_user = user.first_name.split()
    first_user = first_user[0][0]
    last_user = user.last_name.split()
    last_user = last_user[0][0]
    context={   
        'user':user,
        'first':first_user,
        'last':last_user,
    }
    
    if request.POST:

        errors=[]
    
        form=request.POST
        if len(form['first_name']) < 2:
            errors.append('First name must be at least 2 characters.')
        if len(form['last_name']) < 2:
            errors.append('Last name must be at least 2 characters.')
        if not EMAIL_REGEX.match(form['email']):
            errors.append('Please provide a valid email') 
        # if len(form['birthday'])<1:
        #     errors.append("Please provide Birth info")
        if form['birthday']>now:
            errors.append("Your birthday refers to a future date. Please check!!")

        user=User.objects.get(id=user_id)     
            
        if errors:
            for e in errors:
                messages.error(request, e)
        else:
            
            if user.email != form['email']:
                try:
                    user=User.objects.get(email=form['email'])
                    messages.error(request, 'This email already exists. Please change.')
                except User.DoesNotExist:
                    user.email=form['email']
                    
            user.first_name=form['first_name']
            user.last_name=form['last_name']
            
            user.birth=form['birthday']
            user.save() 
               
            user=User.objects.get(id=user_id)    
            first_user = user.first_name.split()
            first_user = first_user[0][0]
            last_user = user.last_name.split()
            last_user = last_user[0][0]
            context={   
                'user':user,
                'first':first_user,
                'last':last_user,
            }   
            
    return render(request, 'its_quote_dash/editaccount.html', context)

def show(request, user_id):
    if not 'user_id' in request.session:
        messages.error(request, 'You need to login.')
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    quote = Quote.objects.filter(users_id=user_id).order_by('-created_at') 
    
    quser=User.objects.get(id=user_id) 
    first_user = user.first_name.split()
    first_user = first_user[0][0]
    last_user = user.last_name.split()
    last_user = last_user[0][0]
    context={
        'quote':quote,
        'quser':quser,
        'user':user,
        'first':first_user,
        'last':last_user,
    }
    return render(request, 'its_quote_dash/userposts.html', context)    

def delete(request, quote_id):
    if not 'user_id' in request.session:
        messages.error(request, 'You need to login.')
        return redirect('/')
    quote = Quote.objects.get(id=quote_id) 
    quote.delete()
    return redirect('/dashboard')     

def like(request, user_id, quote_id):
    if not 'user_id' in request.session:
        messages.error(request, 'You need to login.')
        return redirect('/')
    like=Liked.objects.filter(users_liked_id = user_id).filter(quotes_liked_id = quote_id)
    if not like:
        like = Liked.objects.create(users_liked_id = user_id, quotes_liked_id = quote_id)
        like.save()
        quote = Quote.objects.get(id=quote_id) 
        quote.like=int(quote.like)+int(1)
        quote.save()
    return redirect('/dashboard') 
   