from mitmproxy import ctx
import requests

class Counter():
    def __init__(self):
        self.num = 0
    
    def request(self,flow):        
        if "v6-dy.ixigua.com" in flow.request.url:
            filename = "douyin/"+str(self.num)+".mp4"
            res = requests.get(flow.request.url)
            print("开始下载:{0}".format(filename))
            with open(filename,"wb") as f:
                f.write(res.content)
                print("下载完成:{0}".format(filename))
                self.num = self.num + 1

addons = {
    Counter()
}