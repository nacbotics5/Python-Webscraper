import requests,re
from bs4 import BeautifulSoup
 
class WebCrawler(object):
    def __init__(self):
        self.browser = requests.session()
        self.user_agent = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'}
    
    def open_url(self,url):
        html = self.browser.get(url,headers = self.user_agent,allow_redirects=False).content
        return(html)
    
    def gather_text(self,url):
        html = self.open_url(url)
        soup = BeautifulSoup(html, features="html.parser")
        for tags in soup(["script", "style","head"]):
            tags.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return(text)
 
    def get_image(self,url):
        html = self.open_url(url)
        BS = BeautifulSoup(html, "html.parser")
        for image in BS.findAll('img'):
            print(image.get('src'))
    
    def Login(self, username, password):
        html = self.open_url(self.url)
        login_data = {"username": username,"password": password}
        self.browser.post(self.url,login_data)
        return(self.browser.status)
    
    def download(self,url,id):
        with open("%i.jpg"%id,'wb') as filem:
            data = self.browser.get(url,stream=True,headers = self.user_agent,allow_redirects=False)
            chunks =  int(data.headers['Content-length'])
            filesize = round(chunks/10**6,2)
            print("FILENAME: %i.jpg"%id)
            print("FILESIZE : %f"%filesize)
            try:
                for chunk in data.iter_content(chunk_size = chunks):filem.write(chunk)
                return("Done downloading!")
            except Exception as e:
                return("sorry couldn't download file because %s"%str(e))

    def crawl_link(self,url,pattern=""):
        pages = []
        html = self.open_url(url)
        BS = BeautifulSoup(html, "html.parser")
        for link in BS.findAll("a",href=re.compile("(.*?)")):
            if "href" in link.attrs:
                try:
                    file_link = link.attrs['href']
                    pages.append(file_link)
                except Exception as e:print(str(e))
        return(pages)



