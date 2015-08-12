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

# Create your views here.

@login_required(login_url='accounts/login/')
def url_list(request):
	urls = URLExp.objects.all()
	return render(request, 'urlexpander/url_list.html', {'urls': urls})

@login_required
def url_detail(request, pk):
	url = get_object_or_404(URLExp, pk=pk)
	return render(request, 'urlexpander/url_detail.html', {'url': url})

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
			url.pagetitle = soup.title.string
			url.httpstat = r.status_code  #httpstatus 
			url.save() #should post original url and results to db
		return redirect('urlexpander.views.url_detail', pk=url.pk)
        else:
                form = SubmitForm()
        return render(request, 'urlexpander/url_edit.html', {'form': form})

@login_required
def url_remove(request, pk):
	url = get_object_or_404(URLExp, pk=pk)
	url.delete()
	return redirect('urlexpander.views.url_list')
