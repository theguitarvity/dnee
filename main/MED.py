"""
MED - Motor de Extração Dinâmica


"""
from bs4 import BeautifulSoup
import requests
from main.models import Agent, Crawler
from django.contrib.auth.models import User
#from django.db.models import Q
from djongo.models import Q


class Engine():
    #nlink = 'https://news.google.com/topics/CAAqJQgKIh9DQkFTRVFvSUwyMHZNREUxWm5JU0JYQjBMVUpTS0FBUAE?hl=pt-BR&gl=BR&ceid=BR%3Apt-419'
    nlink = 'https://www.bing.com/news?cc=br'
    def start(self, user):
        req = requests.get(self.nlink)
        print('iniciado')
        curl = ''
        users = User.objects.all()
        dat = req.text
        soup = BeautifulSoup(dat, features='lxml')
        for s in soup.find_all('a'):
            
            #if 'http' in str(s.get('href')) and 'google' not in str(s.get('href')) and 'youtube' not in str(s.get('href')) and 'itunes' not in str(s.get('href')) and 'blogger' not in str(s.get('href')):
            if (len(str(s.get('href')).split('/'))-1) > 5: 
                print(s.get('href'))
                engine_domain = str(s.get('href')).split('/')[2]
                engine_name = str(s.get('href')).split('.')[1]
                for user in users:
                    try:
                        agent = Agent.objects.get(
                            Q(user= user),
                            Q(agent_domain = engine_domain)
                        )
                    except Agent.DoesNotExist as identifier:
                        ag = Agent.create(
                            auser = user,
                            aname = engine_name,
                            adomain = engine_domain,
                        )
                        ag.save()
                        try:
                            r1 = requests.get(str(s.get('href')))
                            dat1  = r1.text
                            bf = BeautifulSoup(dat1, features='lxml')
                            for s2 in bf.find_all('a'):
                                if s2.get('href') is not None and 'http' in s2.get('href'):
                                    r2 = requests.get(str(s2.get('href')))
                                    dat2 = r2.text
                                    bf2 = BeautifulSoup(dat2, features='lxml')
                                    for h1 in bf2.find_all('title'):
                                        try:
                                            cr = Crawler.objects.get(agent = ag)
                                        except Crawler.DoesNotExist as identifier:
                                            try:
                                                crawler = Crawler.create(
                                                    cagent = ag,
                                                    curl = str(s.get('href')),
                                                    cmanchete = '',
                                                    clink = '',
                                                    ctitulo = '',
                                                    csub = '',
                                                    ccontent = '',
                                                    cdate = '',
                                                    cauthor = '',
                                                )
                                                crawler.save()
                                                crawler.parse()
                                            except Exception as identifier:
                                                ag.delete()
                                            
                                               


                        except Exception as id:
                            print(id.value)