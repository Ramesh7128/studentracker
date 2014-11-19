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
    dict = []

    ########### Git hub ##########
    users = User.objects.get(username=request.user)
    user_url = profile.objects.get(users=users)
    user_url = str(user_url.github)
    list_url = user_url.split('/')
    url = "https://api.github.com/users/"+list_url[-1]+"/repos"
    repos = urllib2.urlopen(url)
    data = json.load(repos)
    for li in data:
        if li['fork']==False:
            dict.append(li['name'])
    points = len(dict)
    userprof = profile.objects.get(users=request.user)
    context_dict['userprof'] = userprof
    context_dict['data'] = dict
    context_dict['points'] = points
    ######## end of githb ##########


    return render_to_response('studentracker/userprofile.html', context_dict, context)


