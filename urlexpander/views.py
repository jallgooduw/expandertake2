from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import URLExp
from .forms import SubmitForm
from bs4 import BeautifulSoup 
import requests 

# Create your views here.

def url_list(request):
	urls = URLExp.objects.all()
	return render(request, 'urlexpander/url_list.html', {'urls': urls})

def url_detail(request, pk):
	url = get_object_or_404(URLExp, pk=pk)
	return render(request, 'urlexpander/url_detail.html', {'url': url})

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
