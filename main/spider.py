from bs4 import BeautifulSoup
import requests

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
                i+=1
            return res
                
                

                
                    

        except Exception:
            pass
    
        
        