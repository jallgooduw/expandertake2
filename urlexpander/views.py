from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import URLExp

# Create your views here.

def url_list(request):
	urls = URLExp.objects.all()
	return render(request, 'urlexpander/url_list.html', {'urls': urls})

def url_detail(request, pk):
	url = get_object_or_404(URLExp, pk=pk)
	return render(request, 'urlexpander/url_detail.html', {'url': url})
