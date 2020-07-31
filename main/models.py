from django.db import models
import datetime
from bs4 import BeautifulSoup
import requests
from django.contrib.auth.models import User

#from .models import Crawler
#from . import Spider as spider


# Create your models here.
class Agent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    agent_name = models.CharField(max_length=200)
    agent_domain = models.CharField(max_length = 200)
    
    active = models.BooleanField()
    started_date = models.DateTimeField('date started')

    def __str__(self):
        return self.agent_name


    @classmethod
    def create(cls, auser, aname, adomain):
        agent = cls(user = auser, agent_name = aname, agent_domain = adomain, active = False,started_date = datetime.datetime.now())
        return agent


    


class Crawler(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE , related_name='crawler')
    crawler_url = models.CharField(max_length=200)
    manchete_class = models.CharField(max_length = 200)
    link_class = models.CharField(max_length = 200)
    titulo_class = models.CharField(max_length = 200)
    subtitulo_class = models.CharField(max_length = 200)
    content_class = models.CharField(max_length = 200)
    date_class = models.CharField(max_length = 200)
    autor_class = models.CharField(max_length = 200)
    started_date = models.DateTimeField('date started')

    @classmethod
    def create(cls, cagent, curl, cmanchete, clink, ctitulo, csub, ccontent, cdate, cauthor):
        crawler = cls(
            agent = cagent, 
            crawler_url = curl, 
            manchete_class = cmanchete,
            link_class = clink,
            titulo_class = ctitulo,
            subtitulo_class = csub,
            content_class = ccontent,
            date_class = cdate,
            autor_class = cauthor,
            started_date = datetime.datetime.now()
            )
        return crawler
   

    
    def parse(self): 
        data = {}        
        #spiders = Spider(aname = self.agent.name, curl = self.crawler_url, cmanchete = self.manchete_class, clink = self.link_class, ctitulo = self.titulo_class, csub = self.subtitulo_class, ccontent = self.content_class, cdate = self.date_class, cauthor = self.autor_class)
        
        #cr1 = Crawler.objects.get(id = id)
        data = self.parseNoticia()
        i = 0

        print(data)
        for item in data.items():

            try:
                aux = Noticia.objects.get(link_noticia = data[i]['link'])
            except Noticia.DoesNotExist as identifier:
                if len(str(data[i]['content']))>800:

                    noti = Noticia.create(
                        self, 
                        titulo=data[i]['title'], 
                        sub = data[i]['sub'], 
                        link=data[i]['link'], 
                        content=data[i]['content'], 
                        author='teste')
                    noti.save()
            """aux = Noticia.objects.get(link_noticia= item[0])
            if aux is None:
                noti = Noticia.create(
                    self, 
                    titulo=data[i]['title'], 
                    sub = data[i]['sub'], 
                    link=data[i]['link'], 
                    content=data[i]['content'], 
                    author='teste')
                noti.save()

            
            
                
                print(data[i]['link'])"""
            i+=1
        #for i in data.__len__():

            #try:
                #noticia = data[i]
                #noti = Noticia.create(self, titulo=noticia['title'], sub = noticia['sub'], link=noticia['link'], content=noticia['content'], author='teste')
                #noti.save()
                #print('foi') 

            #except Exception as identifier:
                #print(identifier)
          
        return 'ok criado'
    def parseNoticia(self):
        #cr = .objects.get(id = id)
        nlink = ''
        if self.crawler_url != '':
            request = requests.get(self.crawler_url)

            bf = BeautifulSoup(request.text, features='lxml')
            res = {}
            i = 0
            try:
                for item in bf.find_all('a', {'class':self.link_class}):
                    
                    if "http" not in str(item.get('href')):
                        agentid = Agent.objects.get(pk = self.agent.id)
                        nlink = "http://"+str(agentid.agent_domain)+str(item.get('href'))
                        if nlink == "http://www.infomoney.com.breletrobras/noticia/7776797":
                            nlink = "http://www.infomoney.com.br/eletrobras/noticia/7776797"    

                    
                    else:
                        
                        nlink = str(item.get('href'))
                    if 'noticia' in nlink or '/noticia/' in nlink or '/noticias/' in nlink or '/news' in nlink or '/artigo' in nlink or 'exame.abril.com.br/brasil/' in nlink:
                        print("OLHA O LINK AQUI: s"+nlink)
                        request2 = requests.get(nlink)
                        dat = request2.text
                        soup = BeautifulSoup(dat, features='lxml')
                        content  = ''
                        sub = ''
                        caux = ''
                        for cont in soup.findAll('p'):
                            content+=cont.text
                        try:
                            sub = soup.find('h2', {'class': self.subtitulo_class}).getText()                   

                        except Exception as id:
                            try:
                                sub = soup.find('h3', {'class': self.subtitulo_class}).getText()
                            except Exception as id2:
                                try:
                                    sub = soup.find('h4', {'class': self.subtitulo_class}).getText()
                                except Exception as id3:
                                    try:
                                        sub = soup.find('h5', {'class': self.subtitulo_class}).getText()
                                    
                                    except Exception as id4:
                                        try:
                                            sub = soup.find('h6', {'class': self.subtitulo_class}).getText()
                                        except Exception as id5:
                                            try:
                                                sub = soup.find('p', {'class': self.subtitulo_class}).getText()
                                            except Exception as id6:
                                                sub = ''

                        res[i] = {
                            'link':nlink,
                            'title': soup.find('title').getText(),
                            'sub': sub,
                            'content' : content,
                            

                            
                        }
                        print(res[i])
                        #parse()
                        i+=1
                print(res.__len__())
            except Exception as err:
                print("OS error: {0}".format(err))
            return res
        return {}






class Noticia(models.Model):

    crawler = models.ForeignKey(Crawler, on_delete=models.CASCADE, related_name="noticias")
    titulo_noticia = models.CharField(max_length = 1000)
    subtitulo_noticia = models.CharField(max_length = 1000)
    link_noticia = models.CharField(max_length = 1000)
    content_noticia = models.TextField()
    date_noticia = models.DateField()
    autor_noticia = models.CharField(max_length = 1000)

    data = {}

    @classmethod
    def create(cls, crawler, titulo, sub, link, content, author):
        noticia = cls(
            crawler = crawler, 
            titulo_noticia = titulo, 
            subtitulo_noticia = sub, 
            link_noticia = link, 
            content_noticia = content,
            date_noticia = datetime.datetime.now(),
            autor_noticia = author)
        return noticia

    def __str__(self):
        return self.titulo_noticia
    def getLink(self):
        return self.link_noticia






    
class Spider:
    name = ''
    url = ''
    alink = ''
    request = ''
    ctitle = ''
    bf = ''
    cmanchete = ''
    csub = ''
    ccont = ''
    cauthor = ''
    cdate = ''
    
    @classmethod
    def __init__(self, aname, curl, cmanchete, clink, ctitulo, csub, ccontent, cdate, cauthor):
        self.name = aname
        self.url = curl
        self.request = requests.get(self.url)
        self.ctitle = ctitulo
        self.bf = BeautifulSoup(self.request.text, features='lxml')
        self.alink = clink
        self.cauthor = cauthor
        self.cmanchete = cmanchete
        self.csub = csub
        self.cdate = cdate

    def parseNoticia(self):
        nlink = ''
        res = {}
        i = 0
        try:
            for item in self.bf.find_all('a', {'class':self.alink}):
                nlink = str(item.get('href'))
                request = requests.get(str(self.alink))
                dat = request.text
                soup = BeautifulSoup(dat, features='lxml')
                content  = ''
                for cont in soup.findAll('p'):
                    content+=cont.text

                res[i] = {
                    'link':nlink,
                    'title': soup.find('h1', {'class':self.ctitle}).getText(),
                    'sub': soup.find('h2', {'class': self.csub}). getText(),
                    'content' : content,
                    

                    
                }
                print(res[i])
                i+=1
        except Exception as err:
            print("OS error: {0}".format(err))
        return res
                
                
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name_user = models.CharField(max_length = 200)

    def __str__(self):
        return self.name_user



        
    