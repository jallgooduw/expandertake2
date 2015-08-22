from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import URLExp
from .forms import SubmitForm
from bs4 import BeautifulSoup
import requests
from django.contrib.auth import views as auth_views
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import URLExp
from .serializers import URLSerializer
from selenium import webdriver
from ratelimit.decorators import ratelimit
import os, sys
from rest_framework import permissions
from mysite.settings import STATIC_URL, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME
import boto
from boto.s3.key import Key
from boto.s3.connection import S3Connection

# Create your views here.
@ratelimit(key='ip', rate ='10/m', block=True)
@login_required(login_url='accounts/login/')
def url_list(request):
    urls = URLExp.objects.all()
    return render(request, 'urlexpander/url_list.html', {'urls': urls})

@ratelimit(key='ip', rate ='10/m', block=True)
@login_required
def url_detail(request, pk):
    url = get_object_or_404(URLExp, pk=pk)
    return render(request, 'urlexpander/url_detail.html', {'url': url})

@ratelimit(key='ip', rate ='10/m', block=True)
@login_required
def url_new(request):
    if request.method == "POST":
        form = SubmitForm(request.POST)
        if form.is_valid():
            url = form.save(commit=False)
            r = requests.get(url)
            destpage = r.text
            soup = BeautifulSoup(destpage, "html.parser")
            url.finaldestination = r.url
            url.pagetitle = soup.title.string.encode('utf-8')
            url.httpstat = r.status_code  # httpstatus
            #driver = webdriver.PhantomJS(service_log_path='/tmp/ghostdriver.log')
            #driver.set_window_size(1024, 768)
            #driver.get(r.url)
            #url.save()
            #pk = url.pk
            imgsave(url, 'update')
            url.save()
        return redirect('urlexpander.views.url_detail', pk=url.pk)
    else:
        form = SubmitForm()
    return render(request, 'urlexpander/url_edit.html', {'form': form})

def imgsave(url, status):  #I had a lot of help on this!
    scon = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    getname = scon.get_bucket(AWS_STORAGE_BUCKET_NAME)
    passkey = Key(getname)
    if status == 'update':
        r = requests.get(url)
        driver = webdriver.PhantomJS(service_log_path=os.path.devnull)
        driver.set_window_size(1024, 768)
        driver.get(r.url)
        url.save()
        pk=url.pk
        filename = str(pk) + '.png'
        passkey.key = 'imagecaps/' + filename
        driver.save_screenshot('/tmp/'+filename)
        passkey.set_contents_from_filename('/tmp/' + filename)
        passkey.make_public()
        driver.service.process.kill()
        os.remove('/tmp/' + filename)
        url.imagecap = STATIC_URL + "imagecaps/" + filename
    else:
        getname.delete_key(path)


@ratelimit(key='ip', rate ='10/m', block=True)
@login_required
def url_remove(request, pk):
    url = get_object_or_404(URLExp, pk=pk)
    url.delete()
    return redirect('urlexpander.views.url_list')

@ratelimit(key='ip', rate ='10/m', block=True)
@api_view(['GET', 'POST'])
@login_required(login_url='accounts/login/')
def url_apilist(request, format=None):
    if request.method == 'GET':
        urls = URLExp.objects.all()
        serializer = URLSerializer(urls, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = URLSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@ratelimit(key='ip', rate ='10/m', block=True)
@api_view(['GET', 'PUT', 'DELETE'])
@login_required(login_url='accounts/login/')
def url_apidetail(request, pk, format=None):
    try:
        url = URLExp.objects.get(pk=pk)
    except URLExp.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = URLSerializer(url)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = URLSerializer(url, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        url.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)