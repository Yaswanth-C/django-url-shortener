import json
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .forms import UrlForm
from .models import TinyUrls
import re
# Create your views here.

def app_root_view(request):
    if request.method == 'POST':
        form = UrlForm(request.POST)
        if form.is_valid():
            k=form.save()
            db_data = TinyUrls.objects.get(entry_hash=k.entry_hash)
            return JsonResponse({'tiny_url':db_data.tiny_url},status=200)
        else:
            error1 = form.errors.get_json_data()
            error = list()
            try:
                try:
                    error.append(error1.get('full_url','')[0].get('message'))
                except IndexError:
                    pass
                try:
                    error.append(error1.get('tiny_url','')[0].get('message'))
                except IndexError:
                    pass
            except Exception:
                pass
            return JsonResponse({'error':error},status=400)
    else:
        obj = TinyUrls.objects.all().order_by('-clicks').filter(clicks__gt=0)[:5]
        return render(request,"index.html",{'data':obj})



# view which redirects to the original url
def url_redirect(request,keystring):
    key = keystring.replace('/','')
    s2=re.findall('^[a-zA-Z0-9,-]{5,10}$',key)   # regex to ensure the key given is valid. (some string and digits of 5 to 10 charecters).
    try:
        s=str(s2[0])
        if s.startswith('-') or s.endswith('-'):
            raise Exception()
    except:
        msg = 'Check the url you typed.'
        return render(request,"404.html",{'msg':msg})
    try:
        url_data = TinyUrls.objects.get(tiny_url = s2[0])
    except:
        msg = 'Whoa !!. not found !'
        return render(request,"404.html",{'msg':msg})
    else:
        url_data.clicked()  # call clicked() method of object to increment the clicked count
        return redirect(url_data.full_url)

"""
find me here > https://github.com/Yaswanth-C
"""