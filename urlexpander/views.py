from django.shortcuts import render

# Create your views here.
def url_list(request):
return render(request, 'urlexpander/url_list.html', {})
