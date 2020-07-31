from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, JsonResponse
from reportlab.pdfgen import canvas
from django.template import loader
from .models import Agent as Agents
from .models import Noticia as Noticias
from .models import Crawler
from main.forms import UserForm, UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse
import threading
import time
import io
from django.http import  FileResponse
from reportlab.pdfgen import canvas
from main.MED import Engine
from django.core import serializers
from django.views.generic import View
import datetime
from .render import Render
from django.template.loader import get_template
from django.db.models import Q
import json
class Pdf(View):
    def get(self, request, agent_id):
        agent = Agents.objects.get(pk=agent_id)
        crawler1 = Crawler.objects.get(agent = agent)
        last_news_list = Noticias.objects.filter(crawler = crawler1.id).order_by('-date_noticia')
        params = {
            'agente': agent,
            'crawler': crawler,
            'noticias': len(last_news_list)
        }
        return Render.render('main/relatorio.html', params)

def autocompleteModel(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    
    if search_text is not '':
        news  = Noticias.objects.filter(titulo_noticia__contains = search_text)
    else:
        return render(request,'main/ajax/ajax_search.html', {}) 
    context = {
        'news':news
    }
    return render(request,'main/ajax/ajax_search.html', context) 
    

@login_required
def index(request):
    agent_per_user = Agents.objects.filter(
        Q(user = request.user)
    )
    news_list = []
    for agent in agent_per_user:
        try:
            craw = Crawler.objects.get(agent = agent)
            for n in Noticias.objects.filter(Q(crawler = craw)):
                news_list.append(n)
        except Exception as identifier:
            pass

    agent_list = Agents.objects.filter(Q(user = request.user))
    crawlers_list = Crawler.objects.all()
    chart = []
    datas = {}
    chart_name = list(chart)
    chart_data = list(datas)
    
    i = 2
    j = 0
    for agent in agent_list:
        try:
            c = Crawler.objects.get(agent = agent)
            noti = Noticias.objects.filter(crawler = c.id)
            chart.append(len(noti))
            

        except Exception as identifier:
            pass
        
    
    
    context = {
        'allnews': news_list,
        'allagents':agent_list,
        'allcrawlers': crawlers_list,
        'chartnames': chart_name,
        'data':chart,

        
    }
    #crawlers_list = Crawler.objects.all()
    t = threading.Thread(target=worker, args=(request, crawlers_list,), kwargs={})
    t.daemon= True
    t.start()
    return render(request, 'main/home.html', context)
def newhome(request):
    context = {}
    return render(request, 'main/newhome.html', context)
def updateHome(request):
    if request.is_ajax():
        news_list = Noticias.objects.all()
    agent_list = Agents.objects.filter(user = request.user)
    crawlers_list = Crawler.objects.all()
    chart = []
    datas = {}
    chart_name = list(chart)
    chart_data = list(datas)
    
    i = 2
    j = 0
    for agent in agent_list:
        try:
            c = Crawler.objects.get(agent = agent)
            noti = Noticias.objects.filter(crawler = c.id)
            chart.append(len(noti))
            

        except Exception as identifier:
            pass
        
    
    
    context = {
        'allnews': list(news_list),
        'allagents':list(agent_list),
        'allcrawlers': list(crawlers_list),
        'chartnames': list(chart_name),
        'data':list(chart),

        
    }
    json = serializers.serialize('json', context)
    return JsonResponse(json, content_type = 'application/json')
    

def news(request):
    news_list = Noticias.objects.all()
    agent_list = Agents.objects.all()
    crawlers_list = Crawler.objects.all()
    context = {
        'allnews': news_list,
        'allagents':agent_list,
        'allcrawlers': crawlers_list,
        
    }
    t = threading.Thread(target=worker, args=(crawlers_list,), kwargs={})
    t.daemon= True
    t.start()
    return render(request, 'main/noticias.html', context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, 'main/login.html', {'message':'Conta inativa'})
        else:
            print('erro 2')
            return render(request, 'main/login.html', {'message':'username ou senha inválido'})

    else:
        return render(request, 'main/login.html', {})
        


def register(request):
    registered = False

    if request.method == 'POST':
        user_form  = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True

        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    context = {
        'user_form':user_form,
        'profile_form':profile_form,
        'registered':registered
    }
    return render(request, 'main/registration.html', context)


def worker(request, crawlers_list):
    eng = Engine()
    while True:
        
        for item in crawlers_list:
            item.parse()
        eng.start(user = request.user)
        
        time.sleep(120)

def remove(request, agent_id):
    agent = Agents.objects.get(pk=agent_id)
    agent.delete()
    return redirect('index')


def gerarRelatorio(request, agent_id):
    agent = Agents.objects.get(pk=agent_id)
    data = datetime.datetime.today().strftime('%d/%m/%y')
    crawler1 = Crawler.objects.get(agent = agent)
    last_news_list = Noticias.objects.filter(crawler = crawler1.id).order_by('-date_noticia')
    params = {
        'agente': agent,
        'crawler': crawler,
        'noticias': len(last_news_list),
        'data': data
    }
    return Render.render('main/relatorio.html', params)    
def gerarRelatorioGlobal(request):
    agentes = Agents.objects.filter(Q(
        user_id = request.user.id
    ))
    news_list = {}
    data = datetime.datetime.today().strftime('%d/%m/%y')
    
    for agent in agentes:
        
        try:
            i = 0
            craw = Crawler.objects.get(agent = agent)
            noti = Noticias.objects.filter(Q(crawler = craw))

            #news_list[agent.agent_domain] = len(noti)
            listn = [
                noti.link_noticia
                for noti in crawler.noticias.all()
            ]                
        except Exception as identifier:
            pass
    params = {
        'agentes_rel': agentes,
        'noticias': news_list,
        'data': data
    }
    return Render.render('main/relatorio.html', params)
   

    




def agente(request, agent_id):
    last_news_list = {}
    try:
        agent = Agents.objects.get(pk=agent_id)
        crawler1 = Crawler.objects.get(agent = agent)
        last_news_list = Noticias.objects.filter(crawler = crawler1.id).order_by('-date_noticia')
    except Agents.DoesNotExist:
        raise Http404("O agente solicitado não existe!")
    except Noticias.DoesNotExist:
        pass
    return render(request, 'main/agentes.html', {'agent':agent, 'last_news_list':last_news_list})
def crawler(request, crawler_id):
    try:

        crawler = Crawler.objects.get(agent = crawler_id)
        crawler.parse()
    except Exception as ex:
        print("OS error: {0}".format(ex))
    url = str('/agentes/')+str(crawler_id)
    return HttpResponseRedirect(url)    

def play(request):
    crawlers_list = Crawler.objects.all()
    t = threading.Thread(target=worker, args=(crawlers_list,))
    t.start()
    while t.isAlive():
        print("Aguardando thread")
        time.sleep(30)
        
    print("Thread morreu")
    print("Finalinzando o crawler")
    return HttpResponseRedirect("/")
    

    




def newagent(request):
    try:
        user = request.user
        ag = Agents.create(
            auser = user, 
            aname = request.POST['agent_name'], 
            adomain = request.POST['agent_domain']
        )
        ag.save()
        
        #agent = Agents.objects.get(agent_domain = str(request.POST['agent_domain']))
        curl = "http://".join(str(request.POST['agent_domain']))
        crawler = Crawler.create(
            cagent = ag,
            curl = curl,
            cmanchete = '',
            clink = '',
            ctitulo = '',
            csub = '',
            ccontent = '',
            cdate = '',
            cauthor = '',
        )
        crawler.save()
    except KeyError as ex:
        print (ex.value) 
        
    return HttpResponseRedirect(reverse('index'))

    
    
def info(request):
    return render(request, 'main/info.html', {})