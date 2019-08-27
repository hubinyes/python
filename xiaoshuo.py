from HtmlDownloader import HtmlDownloader
from bs4 import BeautifulSoup
import re

url = "http://www.jjwxc.net/onebook.php?novelid=2140380"

downLoader = HtmlDownloader()
html = downLoader.download(url,0)
soup = BeautifulSoup(html,"lxml")

chapters = []
for tr in soup.select("tr[itemprop]"):
    if len(tr.select("a"))>0:
        try:
            data = {
                    "title":tr.select("a")[0].text,
                    "link":tr.select("a")[0]["href"]
            }
            chapters.append(data)
            print(data)
        except:
            pass 

with open("xiaoshuo.txt","w",encoding="utf-8") as f:
    for item in chapters:    
        # f.write(item["title"])
        # f.write('\n')
        html = downLoader.download(item["link"],0)
        soup = BeautifulSoup(html, "lxml")
        novel = soup.select(".noveltext")[0].text       
        pat =r'\u3000\u3000([\u4e00-\u9fa5][^0-9a-z\s]*)'
        st = ""
        for s in re.findall(pat, novel):
            st = st + s + "\n"        
 
        f.write(st)
        f.write('\n')
        

