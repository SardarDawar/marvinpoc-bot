from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from . forms import ResellerForm, CustomerForm, registerForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import logging,traceback
from django.conf import settings
import os
import re, json
import pandas as pd
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from datetime import date
from datetime import datetime
import datetime
import shutil
from dnsimple import DNSimple #pip install dnsimple
import requests
import fileinput
import subprocess
import threading
import stat
#logger = logging.getlogger('django')
bot_location = "/home/ubuntu/rasabot/"  #Prod: change it to /home/ubuntu/bot/prod

# Create your views here.
#****************************************************#
#                 Login Page View                    #
#****************************************************#
def loginpage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            url = request.POST.get('urlvalue')
            domainfind=url.split('.')
            domainfindprocess=domainfind[0]
            domain=domainfindprocess[7::]
            print(domain)
            user = authenticate(request, username=username, password=password)
            print(username)
            user_check = Profile.objects.get(user__username=username)
            print(user_check.domain[0])
            print(user)
            if user is not None and user_check.domain[0] == domain  :
                print('se')
                login(request, user)
                return redirect('dashboard')

    return render(request, 'main/login/login.html')

#****************************************************#
#                 Logout View                        #
#****************************************************#
def logoutUser(request):
    logout(request)
    return redirect('login')

#****************************************************#
#           Application Dashboard                    #
#****************************************************#
@login_required(login_url='login')
def dashboard(request):
    ########################### Index logic #########################
    resellers = None
    customers = None
    res=None
    customers_profile=None
    user=Profile.objects.get(user=request.user)
    print(user.domain)
    if user.customer == True :
        customers=Customer.objects.get(user=request.user)
    if user.reseller == True:
        resellers=Reseller.objects.get(user=request.user).get_descendants(include_self=True)

    ########################### Index logic #########################

    context = { 'resellers' : resellers, 'customers' : customers, 'user':user }
    return render(request, 'main/dashboard/index.html', context)

#****************************************************#
#           Create Reseller Account                  #
#****************************************************#
@login_required(login_url='login')
def CreateReseller(request):
    ########################### Index logic #########################
    resellers = None
    customers = None
    res=None
    user=Profile.objects.get(user=request.user)
    if user.customer == True :
        customers=Customer.objects.get(user=request.user)
    if user.reseller == True:
        resellers=Reseller.objects.get(user=request.user).get_descendants(include_self=True)

    ########################### Index logic #########################
    form = ResellerForm()
    form_1 = registerForm()    
    if request.method == 'POST':
        form = ResellerForm(request.POST, request.FILES)
        form_1 = registerForm(request.POST, request.FILES)
        if form.is_valid() & form_1.is_valid():
            user = form_1.save(commit=False)
            user.is_active = True
            user.set_password(form_1.cleaned_data['password2'])
            #user.email = form_1.cleaned_data['email'].lower()
            user.save()
            Reseller_1 = form.save(commit=False) 
            Profile.objects.create(user=user,email=user,domain=form_1.cleaned_data['domain'] ,logo=form_1.cleaned_data['logo'], reseller=True)
            Reseller_1.user=user
            Reseller_1.reseller_name=user.first_name + user.last_name
            #Reseller_1.reseller_email=user.email
            
            form.save()
            
            return redirect('/dashboard/') 
    context = { 'resellers' : resellers, 'customers' : customers, 'user':user, 'form' : form ,'form_1':form_1}
    return render(request, 'main/dashboard/create_reseller.html', context)
    
#****************************************************#
#           View Reseller Account                    #
#****************************************************#
@login_required(login_url='login')
def ViewReseller(request, pk):
    ########################### Index logic #########################
    resellers = None
    customers = None
    res=None
    user=Profile.objects.get(user=request.user)
    if user.customer == True :
        customers=Customer.objects.get(user=request.user)
    if user.reseller == True:
        resellers=Reseller.objects.get(user=request.user).get_descendants(include_self=True)

    ########################### Index logic #########################

    reseller_details = Reseller.objects.get(id=pk)
    context = { 'resellers' : resellers, 'customers' : customers, 'user':user, 'reseller_details' : reseller_details }
    return render(request, 'main/dashboard/view_reseller.html', context)


#****************************************************#
#             Edit Reseller Account                  #
#****************************************************#
@login_required(login_url='login')
def EditReseller(request, pk):
    ########################### Index logic #########################
    resellers = None
    customers = None
    res=None
    user=Profile.objects.get(user=request.user)
    if user.customer == True :
        customers=Customer.objects.get(user=request.user)
    if user.reseller == True:
        resellers=Reseller.objects.get(user=request.user).get_descendants(include_self=True)

    ########################### Index logic #########################

    resellers = Reseller.objects.all()
    customers = Customer.objects.all()
    reseller_details = Reseller.objects.get(id=pk)
    form = ResellerForm(instance=reseller_details)
    context = { 'resellers' : resellers, 
                'customers' : customers, 
                'reseller_details' : reseller_details,
                'form' : form }
    if request.method == 'POST':
        form = ResellerForm(request.POST, instance=reseller_details)
        if form.is_valid():
            form.save()
            return redirect('/dashboard/')
    return render(request, 'main/dashboard/create_reseller.html', context)


#****************************************************#
#           Delete Reseller Account                  #
#****************************************************#
@login_required(login_url='login')
def DeleteReseller(request, pk):
    ########################### Index logic #########################
    resellers = None
    customers = None
    res=None
    user=Profile.objects.get(user=request.user)
    if user.customer == True :
        customers=Customer.objects.get(user=request.user)
    if user.reseller == True:
        resellers=Reseller.objects.get(user=request.user).get_descendants(include_self=True)

    ########################### Index logic #########################

    resellers = Reseller.objects.all()
    customers = Customer.objects.all()
    reseller_details = Reseller.objects.get(id=pk)
    if request.method == 'POST':
        reseller_details.delete()
        return redirect('/dashboard/')
    context = { 'resellers' : resellers, 'customers' : customers, 'user':user, 'reseller_details' : reseller_details }
    return render(request, 'main/dashboard/index.html', context)

#****************************************************#
#           Create Customer Account                  #
#****************************************************#
# @login_required(login_url='login')
# def CreateCustomer(request):
#     ########################### Index logic #########################
#     resellers = None
#     customers = None
#     res=None
#     user=Profile.objects.get(user=request.user)
#     if user.customer == True :
#         customers=Customer.objects.get(user=request.user)
#     if user.reseller == True:
#         resellers=Reseller.objects.get(user=request.user).get_descendants(include_self=True)

#     ########################### Index logic #########################
#     form = CustomerForm()
#     form_1 = registerForm()    
#     if request.method == 'POST':
#         form = CustomerForm(request.POST)
#         form_1 = registerForm(request.POST)
#         if form.is_valid() & form_1.is_valid():
#             user = form_1.save(commit=False)
#             user.is_active = True
#             user.set_password(form_1.cleaned_data['password2'])
#             #user.email = form_1.cleaned_data['email'].lower()
#             user.save()
#             customer_1 = form.save(commit=False) 
#             Profile.objects.create(user=user,email=user,domain=form_1.cleaned_data['domain'] ,logo=form_1.cleaned_data['logo'], customer=True)
#             customer_1.user=user
#             customer_1.customer_name=user.first_name + user.last_name
#             #customer_1.customer_email=user.email

    #         ########################### Create Chatbot #########################
    #         #Prod: Change the number of characater removal based on prod domain name
    #         customername = form_1.cleaned_data['domain'][:-16]

    #         # Create customer filesystem
    #         path = str(bot_location+customername)
    
    #         # Copy template bot files inside the new directory
    #         shutil.copytree('/home/ubuntu/app/template', path)  # Prod: change it to /home/ubuntu/bot/template

    #         # Keep directoy ownership and permissions
    #         #st = os.stat('/home/ubuntu/app/template')
    #         #os.chown(path, st[stat.ST_UID], st[stat.ST_GID])
    #         #shutil.chown(path, user='ubuntu', group='ubuntu')
    #         user='ubuntu'
    #         group='ubuntu'
    #         for dirpath, dirnames, filenames in os.walk(path):
    #             shutil.chown(dirpath, user, group)
    #             #os.chmod(dirpath, 0o655)
    #             for filename in filenames:
    #                shutil.chown(os.path.join(dirpath, filename), user, group)
    #                #os.chmod(os.path.join(dirpath, filename), 0o655)
            

    #         # Create DNS-A record (customername) in DNSimple with EC2 public IP - via API 
    #         dns = DNSimple(api_token='eIqf5mTjNE2wVPgwaAJwmj3ycpnssg84')              # Prod: Change API token as per new Domain Name
    #         url = 'https://api.dnsimple.com/v2/91349/zones/marvinaiapp.com/records'   # Prod: Change Domain ID (91349)
    #         payload = { "name" : customername, "type" : "A", "content" : "3.249.183.13", "ttl" : "3600", "priority" : "20" }  # Prod: Change EC2 public IP
    #         headers = {'Authorization': 'Bearer eIqf5mTjNE2wVPgwaAJwmj3ycpnssg84', 'Accept': 'application/json', 'Content-Type': 'application/json'}
    #         res = requests.post(url, data=json.dumps(payload), headers=headers)
    #         #print(res)

    #         # Update docker-compose file and docker container name with Customer Account Name 
    #         for line in fileinput.FileInput(path + "/docker-compose.yml",inplace=1):
    #             line = line.replace("rasa_server","rasa_server_" + customername)
    #             line = line.replace("action_server","action_server_" + customername)
    #             line = line.replace("rasa_postgres","rasa_postgres_" + customername)
    #             line = line.replace("customername", customername)
    #             print(line)
    #         fileinput.close()
    #         shutil.chown(path + "/docker-compose.yml", user, group)
   
    #         # Change endpoint.yml to update action server name and postgres db address with Customer Account Name
    #         for line in fileinput.FileInput("/home/ubuntu/rasabot/" + customername + "/backend/endpoints.yml",inplace=1):
    #             line = line.replace("action_server", "action_server_" + customername)
    #             line = line.replace("rasa_postgres", "rasa_postgres_" + customername)
    #             print(line)
    #         fileinput.close()
    #         shutil.chown(path + "/backend/endpoints.yml", user, group)
    
    #         # Change default action Action response for the bot with Customer Account Name - This is OPTIONAL 
    #         for line in fileinput.FileInput("/home/ubuntu/rasabot/" + customername + "/actions/actions.py",inplace=1):
    #             line = line.replace("TemplateBot", customername)
    #             print(line)
    #         fileinput.close()
    #         shutil.chown(path + "/actions/actions.py", user, group)
  
    #         # Run docker-compose in new customer directory - via API
    #         def run_docker():
    #             os.chdir(path)
    #             os.system("docker-compose up -d")


    #         th = threading.Thread(target=run_docker)
    #         th.start()
            
    #         form.save()
            
    #         return redirect('/dashboard/') 

    

    # context = { 'resellers' : resellers, 'customers' : customers, 'user':user, 'form' : form,'form_1':form_1 }
    # return render(request, 'main/dashboard/create_customer.html', context)

#****************************************************#
@login_required(login_url='login')
def CreateCustomer(request):
    ########################### Index logic #########################
    resellers = None
    customers = None
    res=None
    user=Profile.objects.get(user=request.user)
    if user.customer == True :
        customers=Customer.objects.get(user=request.user)
    if user.reseller == True:
        resellers=Reseller.objects.get(user=request.user).get_descendants(include_self=True)

    ########################### Index logic #########################
    form = CustomerForm()
    form_1 = registerForm()    
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        form_1 = registerForm(request.POST , request.FILES)
        if form.is_valid() & form_1.is_valid():
            user = form_1.save(commit=False)
            user.is_active = True
            user.set_password(form_1.cleaned_data['password2'])
            #user.email = form_1.cleaned_data['email'].lower()
            user.save()
            customer_1 = form.save(commit=False) 
            Profile.objects.create(user=user,email=user,domain=form_1.cleaned_data['domain'] ,logo=form_1.cleaned_data['logo'], customer=True)
            customer_1.user=user
            customer_1.customer_name=user.first_name + user.last_name
            customer_1.customer_email=user.email
            
            
            form.save()
            
            return redirect('/dashboard/') 
    context = { 'resellers' : resellers, 'customers' : customers, 'user':user , 'form' : form,'form_1':form_1 }
    return render(request, 'main/dashboard/create_customer.html', context)

#             View Customer Account                  #
#****************************************************#
@login_required(login_url='login')
def ViewCustomer(request, pk):
    ########################### Index logic #########################
    resellers = None
    customers = None
    res=None
    user=Profile.objects.get(user=request.user)
    if user.customer == True :
        customers=Customer.objects.get(user=request.user)

    if user.reseller == True:
        resellers=Reseller.objects.get(user=request.user).get_descendants(include_self=True)
    ########################### Index logic #########################

    customer_details = Customer.objects.get(id=pk)
    context = { 'resellers' : resellers, 'customers' : customers, 'user':user, 'customer_details' : customer_details }
    return render(request, 'main/dashboard/view_customer.html', context)


#****************************************************#
#             Edit Customer Account                  #
#****************************************************#
@login_required(login_url='login')
def EditCustomer(request, pk):
    logging.debug('Inside EditCustomer')
    ########################### Index logic #########################
    resellers = None
    customers = None
    res=None
    user=Profile.objects.get(user=request.user)
    if user.customer == True :
        customers=Customer.objects.get(user=request.user)

    if user.reseller == True:
        resellers=Reseller.objects.get(user=request.user).get_descendants(include_self=True)
    ########################### Index logic #########################
    resellers = Reseller.objects.all()
    customers = Customer.objects.all()
    customer_details = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer_details)
    form_1 = registerForm(instance=customer_details)
    context = { 'resellers' : resellers, 
                'customers' : customers, 
                'customer_details' : customer_details,
                'form' : form,
                'form_1' : form_1}
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer_details)
        form_1 = registerForm(request.POST, instance=customer_details)
        if form.is_valid() & form_1.is_valid():
            form.save()
            form_1.save()
            return redirect('/dashboard/')

    return render(request, 'main/dashboard/create_customer.html', context)

#****************************************************#
#           Delete Customer Account                  #
#****************************************************#
@login_required(login_url='login')
def DeleteCustomer(request, pk):
    ########################### Index logic #########################
    resellers = None
    customers = None
    res=None
    user=Profile.objects.get(user=request.user)
    if user.customer == True :
        customers=Customer.objects.get(user=request.user)

    if user.reseller == True:
        resellers=Reseller.objects.get(user=request.user).get_descendants(include_self=True)
    ########################### Index logic #########################
    resellers = Reseller.objects.all()
    customers = Customer.objects.all()
    customer_details = Customer.objects.get(id=pk)
    if request.method == 'POST':
        
        ########################### Delete Chatbot #########################
        #Prod: Change the number of characater removal based on prod domain name
        customername = customer_details.customer_domain[:-16]

        # Create customer filesystem
        path = str(bot_location + customername)

        # Shutdown Chatbot Docker containers
        os.chdir(path)
        os.system("docker-compose down")

        # Delete chatbot docker directory
        shutil.rmtree(path)

        # Delete DNS-A record (customername) in DNSimple with EC2 public IP - via API 
        #url = 'https://api.dnsimple.com/v2/91349/zones/marvinaiapp.com/records/5'   # Prod: Change Domain ID (91349)
        #payload = { "name" : customername, "type" : "A", "content" : "3.249.183.13", "ttl" : "3600", "priority" : "20" }  # Prod: Change EC2 public IP
        #headers = {'Authorization': 'Bearer eIqf5mTjNE2wVPgwaAJwmj3ycpnssg84', 'Accept': 'application/json', 'Content-Type': 'application/json'}
        #res = requests.delete(url, data=json.dumps(payload), headers=headers)

        customer_details.delete()

        return redirect('/dashboard/')
    context = { 'resellers' : resellers, 'customers' : customers, 'user':user, 'reseller_details' : reseller_details }
    return render(request, 'main/dashboard/index.html', context)


#****************************************************#
#           View Reseller Dashboard                  #
#****************************************************#
@login_required(login_url='login')
def ResellerDashboard(request, pk):
    ########################### Index logic #########################
    resellers = None
    customers = None
    res=None
    user=Profile.objects.get(user=request.user)
    if user.customer == True :
        customers=Customer.objects.get(user=request.user)
    if user.reseller == True:
        resellers=Reseller.objects.get(user=request.user).get_descendants(include_self=True)
    ########################### Index logic #########################

    reseller_details = Reseller.objects.get(id=pk)
    context = { 'resellers' : resellers, 'customers' : customers, 'user':user, 'reseller_details' : reseller_details }
    return render(request, 'main/dashboard/reseller/dashboard.html', context)

#****************************************************#
#           View Reseller Settings                   #
#****************************************************#
@login_required(login_url='login')
def ResellerSettings(request, pk):
    ########################### Index logic #########################
    resellers = None
    customers = None
    res=None
    user=Profile.objects.get(user=request.user)
    if user.customer == True :
        customers=Customer.objects.get(user=request.user)

    if user.reseller == True:
        resellers=Reseller.objects.get(user=request.user).get_descendants(include_self=True)
    ########################### Index logic #########################

    reseller_details = Reseller.objects.get(id=pk)
    context = { 'resellers' : resellers, 'customers' : customers, 'user':user, 'reseller_details' : reseller_details }
    return render(request, 'main/dashboard/reseller/settings.html', context)


#****************************************************#
#           View Customer Dashboard                  #
#****************************************************#
@login_required(login_url='login')
def CustomerDashboard(request, pk):
    ########################### Index logic #########################
    resellers = None
    customers = None
    res=None
    user=Profile.objects.get(user=request.user)
    if user.customer == True :
        customers=Customer.objects.get(user=request.user)

    if user.reseller == True:
        resellers=Reseller.objects.get(user=request.user).get_descendants(include_self=True)
    ########################### Index logic #########################

    customer_details = Customer.objects.get(id=pk)
    
    #Prod: Change the number of characater removal based on prod domain name
    customername = customer_details.customer_domain[:-16]
    # Count of Conversations
    counter = os.popen("docker exec -i rasa_postgres_" + customername + " psql -t -Upostgres -a rasa_db -c 'SELECT COUNT(id), COUNT(DISTINCT sender_id) FROM events;' &").read()

    # Count of New Users on Daily basis
    session_timestamp = os.popen("docker exec -i rasa_postgres_" + customername + " psql -t -Upostgres -a rasa_db -c 'select distinct on (sender_id) timestamp from events;' &").read()

    counter = counter.split(';')[1].strip()
    conv_count = counter.split('|')[0]
    user_count = counter.split('|')[1]
    logging.debug("Conversation Count:", conv_count)
    logging.debug("Total User:", user_count)


    # Check Bot URL response time and show on dashboard
    url = 'https://' + customer_details.customer_domain
    responetime = ''
    if url:
       r = requests.get(url, timeout=5)
       r.raise_for_status()
       respTime = str(round(r.elapsed.total_seconds(),2))
       logging.debug(float(respTime)*1000)
       responetime = float(respTime)*1000
    else:
       #requests.exceptions.RequestException as err04
       logging.debug ("Error: ", requests.exceptions.RequestException)

   
    # LetsEncrypt Cert Validity Check
    up_time = subprocess.check_output(["openssl", "x509", "-noout", "-dates", "-in", "/home/ubuntu/rasabot/letsencrypt-nginx-sidecar/sidecar/certs/" + customername + ".marvinaiapp.com/cert.pem"])
    # Trim result output
    up_date_split = str(up_time).split("notBefore=", 1)
    up_date = up_date_split[1].split('notAfter')
    up_date = up_date[0].split('+')[0]
    #logging.debug(pd.to_datetime(str(up_date[0])[:-6]))

    # Calculate how many hours the license been assigned
    hours_diff = str((pd.to_datetime("today") - pd.to_datetime(str(up_date.split('GMT')[0]))).total_seconds() / 3600.0).split('.')[0]
    logging.debug(hours_diff)

   
    timestamp_array = session_timestamp.split(';')[1].split('\n')
    date_arr = []
    dictOfElems = dict()
    
    for i in timestamp_array:
        #logging.debug(i.strip())
        tval = i.strip().split('.')
        logging.debug(str(tval[0]))
        if str(tval[0]):
            curr_date = datetime.datetime.fromtimestamp(int(str(tval[0]))).strftime('%d-%m-%Y')
            date_arr.append(int(str(tval[0])))
            if curr_date in timestamp_array:
                dictOfElems[int(str(tval[0]))] += 1
            else:
                dictOfElems[int(str(tval[0]))] = 1

    dictOfElems = { key:value for key, value in dictOfElems.items() if value >= 1 }

    context = { 'resellers' : resellers, 'customers' : customers, 'user':user, 'customer_details' : customer_details, 'response' : responetime, 'user_count' : user_count, 'conv_final' : conv_count, 'hours' : hours_diff, 'min_date' : min(date_arr), 'timeline_val' : dictOfElems }
    return render(request, 'main/dashboard/customer/dashboard.html', context)


#****************************************************#
#           View Customer Account Settings           #
#****************************************************#
@login_required(login_url='login')
def CustomerSettings(request, pk):
    ########################### Index logic #########################
    resellers = None
    customers = None
    res=None
    user=Profile.objects.get(user=request.user)
    if user.customer == True :
        customers=Customer.objects.get(user=request.user)

    if user.reseller == True:
        resellers=Reseller.objects.get(user=request.user).get_descendants(include_self=True)
    ########################### Index logic #########################

    customer_details = Customer.objects.get(id=pk)
    context = { 'resellers' : resellers, 'customers' : customers, 'user':user, 'customer_details' : customer_details }
    return render(request, 'main/dashboard/customer/settings.html', context)


#****************************************************#
#           View Customer Bot NLU Training           #
#****************************************************#
@login_required(login_url='login')
def CustomerNLUTraining(request, pk):
    ########################### Index logic #########################
    resellers = None
    customers = None
    res=None
    user=Profile.objects.get(user=request.user)
    if user.customer == True :
        customers=Customer.objects.get(user=request.user)

    if user.reseller == True:
        resellers=Reseller.objects.get(user=request.user).get_descendants(include_self=True)
    ########################### Index logic #########################

    customer_details = Customer.objects.get(id=pk)

    customername = customer_details.customer_domain[:-16]
    os.chdir("/home/ubuntu/rasabot/" + customername)
    text = open("/home/ubuntu/rasabot/" + customername + "/backend/data/nlu.md", "r")
    content = text.read()
    text.close()

    context = { 'resellers' : resellers, 'customers' : customers, 'user':user, 'customer_details' : customer_details, 'text' : content }
    return render(request, 'main/dashboard/customer/nlutraining.html', context)


#****************************************************#
#        AJAX Update - Customer Bot NLU Data Add     #
#****************************************************#
@login_required(login_url='login')
@csrf_exempt
def NLUTrainingUpdate(request):
    logging.debug('inside NLUTrainingUpdate')
    customername = ""
    if request.is_ajax and request.method == 'POST':
       data = [] # capture POST request array value coming from ajax
       nlu = []  # capture modified intent and entity value in correct format
       intent_name = ''

       logging.debug(json.loads(request.body))
       #data = request.POST.decode('utf-8') # chop off unnecessary utf-8 characters coming from JQuery
       dataset = json.loads(request.body)
       data = dataset["msgval"]
       customername = dataset["cust_name"][:-16]

       m = 0
       for i in range(len(data)):
           logging.debug(i)
           for j in data:
               if m == 0:
                   nlu.append(str("## intent:" + data[m].replace('"', '')).lower()) # Create Entity value - correct format
                   intent_name = str("  - " + data[m].replace('"', '').lower())
                   break
               else:
                   nlu.append(str("- " + data[m].replace('"', '')))                 #  Create Intent value - correct format
                   break
           m += 1
        
       str_input = '\n' # Put the entire array into a single string
       for k in nlu:
           #logging.debug(k)
           str_input += str(k + '\n')

       logging.debug('*******************')
       #logging.debug(str_input)
       # Write the data to nlu.md 
       os.chdir("/home/ubuntu/rasabot/" + customername)
       content = open("/home/ubuntu/rasabot/" + customername + "/backend/data/nlu.md", "a")
       content.write(str_input)
       content.close()


       # Add Intent name to domain file
       with open("/home/ubuntu/rasabot/" + customername + "/backend/domain.yml") as fp:
           lines = fp.readlines()

       with open("/home/ubuntu/rasabot/" + customername + "/backend/domain.yml", 'w') as fp:
           for line in lines:
               if line == "intents:\n":
                  line = line + intent_name + '\n'
               fp.write(''.join(line))


       # Read the updated NLU file to update Div
       text = open("/home/ubuntu/rasabot/" + customername + "/backend/data/nlu.md", "r")
       updated_nlu = text.read()
       text.close()

    
    return JsonResponse(updated_nlu, safe=False)



#****************************************************#
#           View Customer Bot Resoponse              #
#****************************************************#
@login_required(login_url='login')
def CustomerResponse(request, pk):
    ########################### Index logic #########################
    resellers = None
    customers = None
    res=None
    user=Profile.objects.get(user=request.user)
    if user.customer == True :
        customers=Customer.objects.get(user=request.user)

    if user.reseller == True:
        resellers=Reseller.objects.get(user=request.user).get_descendants(include_self=True)
    ########################### Index logic #########################

    customer_details = Customer.objects.get(id=pk)

    customername = customer_details.customer_domain[:-16]
    os.chdir("/home/ubuntu/rasabot/" + customername)
    start = "responses"
    end = "session_config"
    buffer = ""
    log = False
    # Select bot response specific config from domain.yml file and pass to template
    #for line in open("/home/ubuntu/rasabot/" + customername + "/backend/domain.yml"):
    #    if line.startswith(start):
    #       buffer = line
    #       log = True
    #    elif line.startswith(end):
    #       buffer += line
    #       log = False
    #    elif log:
    #       buffer += line
    #buffer = buffer[:-16]
    text = open("/home/ubuntu/rasabot/" + customername + "/backend/data/responses.md", "r")
    content = text.read()
    text.close()


    context = { 'resellers' : resellers, 'customers' : customers, 'user':user, 'customer_details' : customer_details, 'text' : content }
    return render(request, 'main/dashboard/customer/response.html', context)


#****************************************************#
#    AJAX Update - Customer Bot Response Data Add    #
#****************************************************#
@login_required(login_url='login')
@csrf_exempt
def ResponseUpdate(request):
    if request.is_ajax and request.method == 'POST':
       customername = "" 
       data = [] # capture POST request array value coming from ajax
       response = []  # capture modified response value in correct format

       dataset = json.loads(request.body)
       data = dataset["msgval"]
       customername = dataset["cust_name"][:-16]

       #m = 0
       #for i in range(len(data)):
           #logging.debug(i)
           #for j in data:
               #if m == 0:
                   #data[m].strip()
                   #response.append(str("  utter_" + data[m].replace('"', '')).lower() + ':')  # Create Utter value - correct format
                   #break
               #else:
                   #response.append(str("  - text: " + '"' + data[m].replace('"', '').strip() + '"'))  #  Create Utter response - correct format
                   #break
          # m += 1

       #str_input = '' # Put the entire array into a single string
       #for k in response:
           #logging.debug(k)
           #str_input += str(k + '\n')

       #logging.debug('*******************')
       #logging.debug(str_input)

       # Write the data to domain.yml
       #with open("/home/ubuntu/rasabot/" + customername + "/backend/domain.yml") as fp:
           #lines = fp.readlines()

       #locs = [i for i, val in enumerate(lines) if val == 'session_config:\n']
       #lines.insert(locs[-1], str_input + '\n')

       #with open("/home/ubuntu/rasabot/" + customername + "/backend/domain.yml", 'w') as fp:
           #fp.write(''.join(lines))


       # Fetch the updated Bot Response data from config
       #start = "responses"
       #end = "session_config"
       #updated_response = ""
       #log = False
       #for line in open("/home/ubuntu/rasabot/" + customername + "/backend/domain.yml"):
           #if line.startswith(start):
              #updated_response = line
              #log = True
           #elif line.startswith(end):
              #updated_response += line
              #log = False
           #elif log:
              #updated_response += line
       #updated_response = updated_response[:-16]
       #logging.debug(updated_response) 

       os.chdir("/home/ubuntu/rasabot/" + customername)
       content = open("/home/ubuntu/rasabot/" + customername + "/backend/data/responses.md", "a")
       content.write('\n' + data + '\n')
       content.close()

       text = open("/home/ubuntu/rasabot/" + customername + "/backend/data/responses.md", "r")
       updated_response = text.read()
       text.close()

    return JsonResponse(updated_response, safe=False)



#****************************************************#
#           View Customer Bot Stories Data           #
#****************************************************#
@login_required(login_url='login')
def CustomerStories(request, pk):
    ########################### Index logic #########################
    resellers = None
    customers = None
    res=None
    user=Profile.objects.get(user=request.user)
    if user.customer == True :
        customers=Customer.objects.get(user=request.user)

    if user.reseller == True:
        resellers=Reseller.objects.get(user=request.user).get_descendants(include_self=True)
    ########################### Index logic #########################

    customer_details = Customer.objects.get(id=pk)

    customername = customer_details.customer_domain[:-16]
    os.chdir("/home/ubuntu/rasabot/" + customername)
    text = open("/home/ubuntu/rasabot/" + customername + "/backend/data/stories.md", "r")
    content = text.read()
    #logging.debug(content)
    text.close()

    context = { 'resellers' : resellers, 'customers' : customers, 'user':user, 'customer_details' : customer_details, 'text' : content }
    return render(request, 'main/dashboard/customer/stories.html', context)


#****************************************************#
#    AJAX Update - Customer Bot Stories Data Add     #
#****************************************************#
@login_required(login_url='login')
@csrf_exempt
def StoriesUpdate(request):
   data = ""
   customername = ""
   if request.is_ajax and request.method == 'POST':
       dataset = json.loads(request.body)
       data = dataset["msgval"]
       customername = dataset["cust_name"][:-16]

   os.chdir("/home/ubuntu/rasabot/" + customername)
   content = open("/home/ubuntu/rasabot/" + customername + "/backend/data/stories.md", "a")
   content.write('\n' + data + '\n')
   content.close()

   text = open("/home/ubuntu/rasabot/" + customername + "/backend/data/stories.md", "r")
   updated_stories = text.read()
   text.close()

   return JsonResponse(updated_stories, safe=False)



#****************************************************#
#         View Customer Bot Domain Data              #
#****************************************************#
@login_required(login_url='login')
def CustomerDomain(request, pk):
    ########################### Index logic #########################
    resellers = None
    customers = None
    res=None
    user=Profile.objects.get(user=request.user)
    if user.customer == True :
        customers=Customer.objects.get(user=request.user)

    if user.reseller == True:
        resellers=Reseller.objects.get(user=request.user).get_descendants(include_self=True)
    ########################### Index logic #########################

    customer_details = Customer.objects.get(id=pk)

    customername = customer_details.customer_domain[:-16]
    os.chdir("/home/ubuntu/rasabot/" + customername)
    # Read bot specific domain.yml file
    text = open("/home/ubuntu/rasabot/" + customername + "/backend/domain.yml", "r")
    content = text.read()
    text.close()
    context = { 'resellers' : resellers, 'customers' : customers, 'user':user, 'customer_details' : customer_details, 'text' : content }
    return render(request, 'main/dashboard/customer/domain.html', context)


#****************************************************#
#       View Customer Bot Configuration Data         #
#****************************************************#
@login_required(login_url='login')
def CustomerConfiguration(request, pk):
    ########################### Index logic #########################
    resellers = None
    customers = None
    res=None
    user=Profile.objects.get(user=request.user)
    if user.customer == True :
        customers=Customer.objects.get(user=request.user)

    if user.reseller == True:
        resellers=Reseller.objects.get(user=request.user).get_descendants(include_self=True)
    ########################### Index logic #########################

    customer_details = Customer.objects.get(id=pk)

    customername = customer_details.customer_domain[:-16]
    os.chdir("/home/ubuntu/rasabot/" + customername)
    # Read bot specific config.yml file
    text = open("/home/ubuntu/rasabot/" + customername + "/backend/config.yml", "r")
    content = text.read()
    text.close()
    context = { 'resellers' : resellers, 'customers' : customers, 'user':user, 'customer_details' : customer_details, 'text' : content }
    return render(request, 'main/dashboard/customer/config.html', context)


#****************************************************#
#         View Customer Bot Logs                     #
#****************************************************#
@login_required(login_url='login')
def CustomerLogs(request, pk):
    ########################### Index logic #########################
    resellers = None
    customers = None
    res=None
    user=Profile.objects.get(user=request.user)
    if user.customer == True :
        customers=Customer.objects.get(user=request.user)

    if user.reseller == True:
        resellers=Reseller.objects.get(user=request.user).get_descendants(include_self=True)
    ########################### Index logic #########################

    customer_details = Customer.objects.get(id=pk)

    customername = customer_details.customer_domain[:-16]
    os.chdir("/home/ubuntu/rasabot/" + customername)
    # Ftech docker logs from runtime and write to bot-app.log file
    os.system("docker logs rasa_server_" + customername + " > /home/ubuntu/rasabot/" + customername + "/logs/bot-app.log 2>&1")
    # Read log file content to pass on to template
    log_content = open("/home/ubuntu/rasabot/" + customername + "/logs/bot-app.log", "r")
    content = log_content.read()
    log_content.close()
    context = { 'resellers' : resellers, 'customers' : customers, 'user':user, 'customer_details' : customer_details, 'log' : content }
    return render(request, 'main/dashboard/customer/logs.html', context)


#****************************************************#
#         View Customer Bot Training                 #
#****************************************************#
@login_required(login_url='login')
def CustomerTrainBot(request, pk):
    ########################### Index logic #########################
    resellers = None
    customers = None
    res=None
    user=Profile.objects.get(user=request.user)
    if user.customer == True :
        customers=Customer.objects.get(user=request.user)

    if user.reseller == True:
        resellers=Reseller.objects.get(user=request.user).get_descendants(include_self=True)
    ########################### Index logic #########################

    customer_details = Customer.objects.get(id=pk)
    context = { 'resellers' : resellers, 'customers' : customers, 'user':user, 'customer_details' : customer_details }
    return render(request, 'main/dashboard/customer/bottraining.html', context)


#****************************************************#
#    AJAX Update - Customer Bot Training             #
#****************************************************#
@login_required(login_url='login')
@csrf_exempt
def TrainBotBackend(request):
    # Ajax call on button
    data = ""
    customername = ""
    if request.is_ajax and request.method == 'POST':
       dataset = json.loads(request.body)
       data = dataset["msgval"]
       customername = dataset["cust_name"][:-16]

       if data == "start training":
           logging.debug('lets start train your bot')
           os.chdir("/home/ubuntu/rasabot/" + customername)
           # Ftech docker logs from runtime and write to bot-app.log file
           os.system("docker-compose up --build --renew-anon-volumes -d &")

    return JsonResponse({'status':'Training Completed'})


#****************************************************#
#       View Customer Bot Licese Information         #
#****************************************************#
@login_required(login_url='login')
def CustomerLicense(request, pk):
    ########################### Index logic #########################
    resellers = None
    customers = None
    res=None
    user=Profile.objects.get(user=request.user)
    if user.customer == True :
        customers=Customer.objects.get(user=request.user)

    if user.reseller == True:
        resellers=Reseller.objects.get(user=request.user).get_descendants(include_self=True)
    ########################### Index logic #########################

    customer_details = Customer.objects.get(id=pk)

    # Prod: Change character removal count based on prod domain name
    customername = customer_details.customer_domain[:-16]
    # LetsEncrypt Cert Validity Check
    # Prod: Change Letsencrypt Docker Default path & Certificate Domain Name
    expiry_date = subprocess.check_output(["openssl", "x509", "-noout", "-dates", "-in", "/home/ubuntu/rasabot/letsencrypt-nginx-sidecar/sidecar/certs/" + customername + ".marvinaiapp.com/cert.pem"])
    # Trim result output
    expiry_date_split = str(expiry_date).split("notAfter=", 1)
    expiry_date_split = str(expiry_date_split[1]).split('GMT')
    expiry_date = str(expiry_date_split[0])
    #logging.debug(str(expiry_date))

    # Get Current Date in GMT
    current_date = pd.to_datetime("today")
    #logging.debug(current_date)

    # Calculate License expiry days left
    logging.debug(pd.to_datetime(expiry_date))
    date_diff = pd.to_datetime(expiry_date) - pd.to_datetime("today")
    #logging.debug(str(date_diff))
    days_left_temp = str(date_diff).split("days", 1)
    days_left = str(days_left_temp[0])
    logging.debug(days_left)

    # Define color code based on how many days left for license expiry
    color = ''
    if int(days_left) >= 30:
        color = 'green'
    elif int(days_left) < 30 and int(days_left) >= 7:
        color = 'yellow'
    elif int(days_left) < 7:
        color = 'red'

    context = { 'resellers' : resellers, 'customers' : customers, 'user':user, 'customer_details' : customer_details, 'date' : expiry_date, 'days_left' : days_left, 'color' : color }
    return render(request, 'main/dashboard/customer/license.html', context)


#****************************************************#
#      View Customer Bot Conversation as Inbox       #
#****************************************************#
@login_required(login_url='login')
def CustomerMessages(request, pk):
    ########################### Index logic #########################
    resellers = None
    customers = None
    res=None
    user=Profile.objects.get(user=request.user)
    if user.customer == True :
        customers=Customer.objects.get(user=request.user)

    if user.reseller == True:
        resellers=Reseller.objects.get(user=request.user).get_descendants(include_self=True)
    ########################### Index logic #########################

    customer_details = Customer.objects.get(id=pk)
    customername = customer_details.customer_domain[:-16]

    os.chdir("/home/ubuntu/rasabot/" + customername)
    # Ftech user id (unique user as per session) from conversation
    res_val = ''
    distinct_user_list = []
    res_val = os.popen("docker exec -i rasa_postgres_" + customername + " psql -t -Upostgres -a rasa_db -c 'SELECT DISTINCT sender_id FROM events;'").read()
    # convert string resultset into array

    def func(x):
        try:
            return int(x)
        except ValueError:
            return x

    session_id_list = [func(x) for x in re.sub(r'^.*?;', '', res_val).split()]

    for i in session_id_list:
        if not "SELECT" or "DISTINCT" or "sender_id" or "FROM" or "events;" in i:
            distinct_user_list.append(i)
        else:
            break

    context = { 'resellers' : resellers, 'customers' : customers, 'user':user, 'customer_details' : customer_details, 'user_list' : distinct_user_list, 'conv_thread_count' : len(distinct_user_list) }
    return render(request, 'main/dashboard/customer/messages.html', context)


#****************************************************#
# View Customer Bot Inbox - Each Conversation Thread #
#****************************************************#
@login_required(login_url='login')
@csrf_exempt
def ChatHistoryUpdate(request):
    conv_time = ''
    data = ""
    # Ajax call on button
    customername = ""
    if request.is_ajax and request.method == 'POST':
       dataset = json.loads(request.body)

    data = dataset["msgval"]
    customername = dataset["cust_name"][:-16]
     
    user_session_data = ''
    user_session_data = os.popen("docker exec -i rasa_postgres_" + customername + " psql -t -Upostgres -a rasa_db -c " + '''"select data from events where sender_id =''' + """'""" + data + """'""" + ''';''' + '''"''').read()
      
    timestamp = ''
    global datetime
    conv_dictionary = {}

    for i in re.split('[;]', user_session_data):


        if "event" in i and not "events" in i:
            for j in re.split('[{]', i):
                #print(j)
                #print(j[35:45].strip())
                if "session_started" in j:
                    #print(j[40:51].strip())
                    timestamp = j[40:51].strip()
                    datetime = str(timestamp)



                if "user" in j:
                    for k in re.split('[,]', j):
                        #print(k)
                        if "text" in k:
                            user_statement = k.split(':', 1)[1]
                            user_says = user_statement.replace('"', '')
                            #print(user_says)
                            if datetime:
                               conv_dictionary.setdefault(datetime, []).append({"user":user_says})



                if "template_name" in j:
                    #print(j)
                    for k in re.split('[,]', j):
                        if "text" in k:
                            #print(k)
                            bot_statement = k.split(':', 1)[1]
                            bot_says = bot_statement.replace('"', '')
                            #print(bot_says)
                            if datetime:
                               conv_dictionary.setdefault(datetime, []).append({"bot":bot_says})
                            



    return JsonResponse(json.dumps(conv_dictionary), safe=False)

