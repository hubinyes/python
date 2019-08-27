import requests
from bs4 import BeautifulSoup
import re
import os
import time
import concurrent.futures
import threading
import multiprocessing
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB

url = "http://music.taihe.com/top"
url_songtype = "http://play.taihe.com/data/music/box/top"    
url_info = "http://play.taihe.com/data/music/songinfo"
url_link = "http://play.taihe.com/data/music/songlink"

user_agent =  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"  
headers={
    "User-Agent":user_agent
}

def main1():    
    songTypeKeys = []
    songTypeNames = []

    r = requests.get(url,headers=headers)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text,"lxml")
    for module in soup.select(".module"):
        name = module.find(class_="title").string
        if name is None:
            continue
        key = module['monkey'].split('-')[1]        
        songTypeKeys.append(key)
        songTypeNames.append(name)
    
    print("千千音乐下载\n")
    print("请选择需下载的音乐类型：")    
    for t in range(0,len(songTypeNames)):        
        print(songTypeNames[t]+"--------"+str(t))

    while True:
        songtype = input("请输入类型对应的数字:")
        try:        
            typeIndex = int(songtype)
            if typeIndex < 0 or typeIndex >= len(songTypeKeys):
                print("索引不在范围内")
                continue
            break
        except:
            print("输入不合法")

    params = {
        "topId":songTypeKeys[typeIndex]
    }

    r = requests.get(url_songtype,headers=headers,params=params)
    songIdList = r.json()['data']["songIdList"]

    localPath = "music/"+songTypeNames[typeIndex]+"/"
    if not os.path.exists(localPath):
        os.mkdir(localPath)

    print("开始下载")
    print("共计%d首" % len(songIdList))
 
    #startime = time.time()
    downLoadMusic(songIdList,localPath)
    #endtime = time.time()
    #print("totaltime",endtime-startime)   
    print("下载完成")

#传入mp3、jpg的本地路径以及其他字符串
def setSongInfo(songfilepath, songtitle, songartist, songalbum, picdata):
    audio = ID3(songfilepath) 
    #img = open(songpicpath,'rb')
    audio.update_to_v23() #把可能存在的旧版本升级为2.3
    audio['APIC'] = APIC( #插入专辑图片
                    encoding=3,
                    mime='image/jpeg',
                    type=3, 
                    desc=u'Cover',
                    data=picdata
                )
    audio['TIT2'] = TIT2( #插入歌名
                    encoding=3,
                    text=[songtitle]
                )
    audio['TPE1'] = TPE1( #插入第一演奏家、歌手、等
                    encoding=3,
                    text=[songartist]
                )
    audio['TALB'] = TALB( #插入专辑名称
                    encoding=3,
                    text=[songalbum]
                )
    audio.save() #记得要保存
    # img.close()

def download(songId,localPath):

    playload={"songIds":songId}

    r = requests.post(url_info,playload,headers=headers)    
    songInfo = r.json()['data']["songList"][0]    

    r = requests.post(url_link,playload,headers=headers)    
    songLink = r.json()['data']["songList"][0]   
    
    name = songInfo["songName"]
    artistName = songInfo["artistName"]
    albumName = songInfo["albumName"]
    
    # songPicBig = songInfo["songPicBig"]        
    # songPicSmall = songInfo["songPicSmall"]
    songPicRadio = songInfo["songPicRadio"]
    
    lrcLink = songLink["lrcLink"]
    songLink = songLink["songLink"]

    print("正在下载：{0}\n".format(name))
    #print("当前线程：{0}".format(threading.current_thread().name))
    try:     
        songPath = localPath + name +"/"
        if not os.path.exists(songPath):
            os.mkdir(songPath)

        lrcName = songPath + name +".lrc"
        if not os.path.exists(lrcName):
            r = requests.get(lrcLink,headers=headers)
            with open(lrcName,'wb') as f:
                f.write(r.content)
                
        mp3Name = songPath + name +".mp3"
        if not os.path.exists(mp3Name):
            r = requests.get(songLink,headers=headers)
            with open(mp3Name,'wb') as f:
                f.write(r.content)        

            r = requests.get(songPicRadio,headers=headers)
            # picName = songPath +songid+".jpg"
            # with open(picName,'wb') as f:
            #     f.write(r.content)        
            try:                  
                setSongInfo(mp3Name,name,artistName,albumName,r.content)
            except:
                pass
    except:
        print("下载出错")

def downLoadMusic(songIdList,localPath):
    works = 2*multiprocessing.cpu_count()+1
    print("cpu_Count:{}".format(multiprocessing.cpu_count()))
    with concurrent.futures.ThreadPoolExecutor(max_workers= works) as exector:
        for songId in songIdList:
            exector.submit(download,songId,localPath)
            
main1()