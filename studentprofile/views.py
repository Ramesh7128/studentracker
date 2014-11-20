# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from oautherise.forms import Userform
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime
import urllib2
import json
from studentprofile.forms import profileform
from studentprofile.models import profile

def index(request):
    context = RequestContext(request)
    context_dict = {}
    return render_to_response('studentracker/base.html', context_dict, context)

def addlinks(request):
    context = RequestContext(request)
    context_dict = {}
    if request.method == 'GET':
        form = profileform()
    else:
        form = profileform(request.POST)
        if form.is_valid():
            profiles = form.save(commit=False)

            try:
                users = User.objects.get(username=request.user)
                profiles.users = users
                profiles.save()
                return HttpResponseRedirect('/')
            except:
                pass
        else:
            print form.errors

    context_dict['forms'] = form

    return render_to_response('studentracker/addlinks.html', context_dict, context)

def userprofile(request, userprofname):
    context = RequestContext(request)
    context_dict = {}
    dicts = []
    lang = []
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

    ########### Git hub ##########
    users = User.objects.get(username=request.user)
    user_url = profile.objects.get(users=users)
    user_url = str(user_url.github)
    list_url = user_url.split('/')
    url = "https://api.github.com/users/"+list_url[-1]+"/repos?client_id=30e9b9ede28e81a28760&client_secret=26308f9622371b86cb0a6f3f55468d4b9ab3e49d"
    req = urllib2.Request(url, headers=hdr)
    repos = urllib2.urlopen(req)
    data = json.load(repos)
    for li in data:
        if li['fork']==False:
            b = {'name':li['name']}
# url to get the languages used in the repo
            url_lang="https://api.github.com/repos/"+list_url[-1]+"/"+li['name']+"/languages?client_id=30e9b9ede28e81a28760&client_secret=26308f9622371b86cb0a6f3f55468d4b9ab3e49d"
            req = urllib2.Request(url_lang,headers=hdr)
            languages = urllib2.urlopen(req)
            datalang = json.load(languages)
            c = dict(b.items()+ datalang.items())
            dicts.append(c)
    points = len(dicts)
    userprof = profile.objects.get(users=request.user)
    context_dict['userprof'] = userprof
    context_dict['data'] = dicts
    context_dict['points'] = points
    ######## end of github ##########


    return render_to_response('studentracker/userprofile.html', context_dict, context)


