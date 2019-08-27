import requests

class HtmlDownloader():
    def download(self,url,text):
        if url is None:
            return None
        user_agent =  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"  
        headers={"User-Agent":user_agent}
        r = requests.get(url,headers=headers)
        if r.status_code==200:         
            if text:               
                return r.text
            else:
                return r.content
        return None

