from fileinput import filename
from django.shortcuts import render
from .models import *
import os

import time
from datetime import datetime
import aes
import post.rsa as rsa
import pandas as pd


from post.forms import FileUploadForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage


# Create your views here.
def result(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('post/drone_list')

    else:
        form = FileUploadForm()

    return render(request, 'post/drone_list.html', {'form': form})


# Create your views here.
def signup(request):   
    if request.method == 'POST':
        if request.POST['password'] == request.POST['confirm']:
            user = User.objects.create_user(
                username=request.POST['username'], password=request.POST['password']
            )
            auth.login(request, user)
            return redirect('/')
        return render(request, 'post/signup.html')
    return render(request, 'post/signup.html')
        
        

def login(request):    
    # login으로 POST 요청이 들어왔을 때, 로그인 절차를 밟는다.
    if request.method == 'POST':
        # login.html에서 넘어온 username과 password를 각 변수에 저장한다.
        username = request.POST['username']
        password = request.POST['password']
                                

        # 해당 username과 password와 일치하는 user 객체를 가져온다.
        user = auth.authenticate(request, username=username, password=password)
        
        # 해당 user 객체가 존재한다면
        if user is not None:
            # 로그인 한다
            auth.login(request, user)
            return redirect('/')
        # 존재하지 않는다면
        else:
            # 딕셔너리에 에러메세지를 전달하고 다시 login.html 화면으로 돌아간다.
            return render(request, 'post/login.html', {'error' : 'username or password is incorrect.'})
    # login으로 GET 요청이 들어왔을때, 로그인 화면을 띄워준다.
    else:
        return render(request, 'post/login.html')

# 로그 아웃
def logout(request):
    auth.logout(request)
    return redirect('/')


def decrypt_field(Cipher, array):
    new_array = [0 for x in range(len(array))]
    for i, v in enumerate(array):
        new_array[i] = Cipher.dec(v).decode()
    return new_array


# Create your views here.
def show_post(request):
    if request.method == 'POST':     
        div = 30
        file = request.FILES['priv_key']
        fs = FileSystemStorage(location='media/keys', base_url='media/keys')
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.url(filename)
        
        def varify_rsa(file):
            drone = Drone.objects.filter(sn=1).values()
            for d in drone: enc_data = d['encryptedkey']
            varify = rsa.rsa_dec2(enc_data, file)
            if not varify: return False
            else: return varify

        kr = varify_rsa(uploaded_file_url)
        if not kr: pass
        else:
            drones = Drone.objects.all().values()
            keyText, iv = kr.decode().split('~')
            data = pd.DataFrame(drones)

            Cipher = aes.myAES(keyText, iv)
            
            data_list = data

            encrypt_temperature = list(data_list['temperature'])
            encrypt_pressure = list(data_list['pressure'])
            encrypt_altitude = list(data_list['altitude'])
            encrypt_rangeheight = list(data_list['rangeheight'])

            # decrypt
            decrypt_temperature = decrypt_field(Cipher, encrypt_temperature)
            decrypt_pressure = decrypt_field(Cipher, encrypt_pressure)
            decrypt_altitude = decrypt_field(Cipher, encrypt_altitude)
            decrypt_rangeheight = decrypt_field(Cipher ,encrypt_rangeheight)

            data_list['temperature'] = decrypt_temperature
            data_list['pressure'] = decrypt_pressure
            data_list['altitude'] = decrypt_altitude
            data_list['rangeheight'] = decrypt_rangeheight
            data_list.drop(['encryptedkey'], axis=1, inplace=True)

            t_list = list(data_list['temperature'])[-div:]
            p_list = list(data_list['pressure'])[-div:]
            a_list = list(data_list['altitude'])[-div:]
            r_list = list(data_list['rangeheight'])[-div:]

            tem_list = list(map(float, t_list))
            pem_list = list(map(float, p_list))
            aem_list = list(map(float, a_list))
            rem_list = list(map(float, r_list))
            
            context = {
                'temperature': tem_list,
                'pressure': pem_list,
                'altitude': aem_list,
                'rangeheight': rem_list,
            }
            return render(request, 'post/result.html', context)

def show_main_page(request):
    return render(
        request,
        'post/index.html',
    )
    
def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                                            username=request.POST['username'],
                                            password=request.POST['password1'],)
            auth.login(request, user)
            return redirect('/')
        return render(request, 'post/signup.html')
    return render(request, 'post/signup.html')

# def form_action(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = NameForm(request.POST)

#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return HttpResponseRedirect('/post/index.html/')

#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = NameForm()

#     return render(request, 'myform/name.html', {'form': form})
