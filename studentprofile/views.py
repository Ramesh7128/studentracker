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
from studentprofile.models import profile, stacklistmodel, Githubmodel, TeamTreeHousemodel, CodeCademymodel, Codewarsmodel, UserProfile
from bs4 import BeautifulSoup
from django.db.models import Q




stackcolors = {"python":"#FF0000", "javascript":"#00FF00", "jquery":"#00FF00", "ruby":"#0000FF", "php":"#00FFFF", "css":"#C0C0C0", "html":"#C0C0C0",}
def index(request):
    context = RequestContext(request)
    context_dict = {}
    try:
        profile_list = UserProfile.objects.filter(~Q(user=request.user))
    except:
        profile_list = UserProfile.objects.all()
    context_dict['profile_list'] = profile_list

    return render_to_response('studentracker/index.html', context_dict, context)


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


def colorsfunction(colorvalue):
    colorvalue = colorvalue.lower()
    try:
        color = stackcolors[colorvalue]
    except:
            color = "#000000"
    return color


def codewars(context_dict, request, jsonstacklist, users):

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive',
       'Authorization': 'C-RRG9-N3JTTRjS5px1i',
       }

    dictlan = {}
    users = User.objects.get(username=request.user)
    user_url = profile.objects.get(users=users)
    user_git = str(user_url.codewars)
    list_url = user_git.split('/')
    url = "https://www.codewars.com/users/"+list_url[-1]+".json"
    req = urllib2.Request(url, headers=hdr)
    source = urllib2.urlopen(req)
    data = json.load(source)

    for key, value in data.items():
        if key == "ranks":
            dictlan = value['languages']
        if key == "honor":
            honor = int(value)
        if key == "completed":
            completed = int(len(value))

    for k, val in dictlan.items():
        jsonlength = len(jsonstacklist) + 1
        l = str(k.strip())
        colors = colorsfunction(l)
        Codewarsmodel.objects.create(users=users, honors=honor, language=k, rank=dictlan[k]['name'],completedchallenges=completed)
        stacklistmodel.objects.create(users=users, stack=k,parentid=4,value=(int(dictlan[k]['score'])),colors=colors)

    userprof = profile.objects.get(users=request.user)
    context_dict['userprof'] = userprof
    return context_dict, jsonstacklist




def github(context_dict, request, jsonstacklist, users):

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

    dicts = []
    lang = []
    github_lang = []
    github_stackpoints = {}

    users = User.objects.get(username=request.user)
    user_url = profile.objects.get(users=users)
    user_git = str(user_url.github)
    list_url = user_git.split('/')
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

            for key, value in datalang.items():
                if key not in github_lang:
                    github_lang.append(str(key))
            github_stackpoints = dict.fromkeys(github_lang,0)


            c = dict(b.items()+ datalang.items()) #to join two dict
            dicts.append(c)
    for dic in dicts:
        for lis, mis in dic.items():
            lis = str(lis)
            # mis = int(mis)
            if lis != "CSS":
                if lis in github_stackpoints.keys():
                    github_stackpoints[lis] += mis
            elif lis == 'CSS' and mis > 500000:
                if lis in github_stackpoints.keys():
                    github_stackpoints[lis] += (mis-500000)
            else:
                if lis in github_stackpoints.keys():
                    github_stackpoints[lis] += mis

    ###database entry###############
    for d in dicts:
      for i,j in d.items():
          name = d['name']
          if (i != "name"):
            Githubmodel.objects.create(users=users, reponame=name, stack=i, bytes=int(j))
    ######end of database entry######

    ########## for changing the bytes github to points#######
    for key, value in github_stackpoints.items():
        github_stackpoints[key] = value/10000.0
        ###########################

    ####### treemap-json for github ###########
    for key, value in github_stackpoints.items():
            jsonlength = len(jsonstacklist) + 1
            l = str(key.strip())
            colors = colorsfunction(l)
            stacklistmodel.objects.create(users=users, stack=str(key),parentid=1,value=int(value),colors=colors)
    ############################################

    points_github = len(dicts)

    return context_dict, jsonstacklist


def teamtreehouse(context_dict, request, jsonstacklist, users):

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

    dicts = []
    points_teamtreehouse = 0

    #users = User.objects.get(username=request.user)
    user_url = profile.objects.get(users=users)
    user_git = str(user_url.teamtreehouse)
    list_url = user_git.split('/')
    url = "https://teamtreehouse.com/"+list_url[-1]
    req = urllib2.Request(url, headers=hdr)
    stackpoints = urllib2.urlopen(req)
    soup = BeautifulSoup(stackpoints)

    sourcehtmltag = soup.findAll('canvas',{ "class" : "chart featurette " })
    data =  json.loads(sourcehtmltag[0].get('data-points'))
    treehousepointsover0 = {}

    for key, value in data.items():
        if value > 0:
            treehousepointsover0[key] = value
            points_teamtreehouse = int(value) + points_teamtreehouse
            TeamTreeHousemodel.objects.create(users=users, coursename=key, points= int(value))


    for key, value in treehousepointsover0.items():
        jsonlength = len(jsonstacklist) + 1
        l = str(key.strip())
        colors = colorsfunction(l)
        stacklistmodel.objects.create(users=users, stack=str(key),parentid=3,value=(value/100.0),colors=colors)
    userprof = profile.objects.get(users=request.user)


    return context_dict, jsonstacklist


def codecademy(context_dict, request, jsonstacklist, users):

    codecademy = []

    #users = User.objects.get(username=request.user)
    user_url = profile.objects.get(users=users)

    user_codecademy = str(user_url.codecademy)
    source = urllib2.urlopen(user_codecademy)
    soup = BeautifulSoup(source)

    links = soup.findAll('h5',{ "class" : "text--ellipsis" })

    for link in links:
        codecademy.append(link.contents[0])

    points_codecademy = len(codecademy)
    for l in codecademy:
        jsonlength = len(jsonstacklist) + 1
        l = str(l.strip())

        colors = colorsfunction(l)

        CodeCademymodel.objects.create(users=users, coursename=l)
        stacklistmodel.objects.create(users=users, stack=l,parentid=2,value=10,colors=colors)
    return context_dict, jsonstacklist

def treemapsforallprofile(jsonstacklist,request, users):
    #userskey = User.objects.get(username=request.user)
    stackobjects = stacklistmodel.objects.filter(users=users)
    for stack in stackobjects:
        jsonstacklist.append({
            "id": stack.id+4,
            "text": stack.stack,
            "parentid": stack.parentid,
            "value": stack.value,
            "color": stack.colors,
        }
        )
    return jsonstacklist


def userprofile(request, userid):
    context = RequestContext(request)
    context_dict = {}
    jsonstacklist = []
    jsonstacklist.append({
                "id": "1",
                "text": "Github",
                "parentid": "-1"
                })
    jsonstacklist.append({
                "id": "2",
                "text": "Codecademy",
                "parentid": "-1"
            })
    jsonstacklist.append({
                "id": "3",
                "text": "TeamTreeHouse",
                "parentid": "-1"
            })
    jsonstacklist.append({
                "id": "4",
                "text": "Codewars",
                "parentid": "-1"
            })

    users = User.objects.get(id=userid)
    prof = stacklistmodel.objects.filter(users=users)

    if not prof:
        context_dict, jsonstacklist = github(context_dict,request, jsonstacklist, users)
        context_dict, jsonstacklist = codecademy(context_dict,request, jsonstacklist, users)
        context_dict, jsonstacklist = teamtreehouse(context_dict,request, jsonstacklist, users)
        context_dict, jsonstacklist = codewars(context_dict,request, jsonstacklist, users)

    jsonstacklist = treemapsforallprofile(jsonstacklist,request, users)
    jsonstacklist = json.dumps(jsonstacklist)
    context_dict['jsonstacklist'] = jsonstacklist


    try:
        githublist = Githubmodel.objects.filter(users=users)
        codecademylist = CodeCademymodel.objects.filter(users=users)
        treehouselist = TeamTreeHousemodel.objects.filter(users=users)
        codewarslist = Codewarsmodel.objects.filter(users=users)
        context_dict['githublist'] = githublist
        context_dict['codecademylist'] = codecademylist
        context_dict['treehouselist'] = treehouselist
        context_dict['codewarslist'] = codewarslist
    except:
        pass

    return render_to_response('studentracker/userprofile.html', context_dict, context)


