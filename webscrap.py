from threading import Thread
import requests
from tkinter import *
import time
from bs4 import BeautifulSoup
qs=""
def transition2():
    global img1
    global flag
    global flag2
    global frames
    global canvas
    local_flag = False
    for k in range(0,5000):
        for frame in frames:
            if flag == False:
                canvas.create_image(0, 0, image=img1, anchor=NW)
                canvas.update()
                flag = True
                return
            else:
                canvas.create_image(0, 0, image=frame, anchor=NW)
                canvas.update()
                time.sleep(0.1)
def web_scraping(qs):
    global flag2
    global loading
    URL = 'https://www.google.com/search?q=' + qs
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    
    links = soup.findAll("a")
    all_links = []
    for link in links:
       link_href = link.get('href')
       if "url?q=" in link_href and not "webcache" in link_href:
           all_links.append((link.get('href').split("?q=")[1].split("&sa=U")[0]))
           

    flag= False
    print(all_links)
    for link in all_links:
        if 'https://en.wikipedia.org/wiki/' in link:
            wiki = link
            flag = True
            break
    div0 = soup.find_all('div',class_="kvKEAb")
    div1 = soup.find_all("div", class_="Ap5OSd")
    div2 = soup.find_all("div", class_="nGphre")
    div3  = soup.find_all("div", class_="BNeawe iBp4i AP7Wnd")

    if len(div0)!=0:
        answer = div0[0].text
    elif len(div1) != 0:
       answer = div1[0].text+"\n"+div1[0].find_next_sibling("div").text
    elif len(div2) != 0:
       answer = div2[0].find_next("span").text+"\n"+div2[0].find_next("div",class_="kCrYT").text
    elif len(div3)!=0:
        answer = div3[1].text
    elif flag==True:
       page2 = requests.get(wiki)
       soup = BeautifulSoup(page2.text, 'html.parser')
       title = soup.select("#firstHeading")[0].text
       
       paragraphs = soup.select("p")
       for para in paragraphs:
           if bool(para.text.strip()):
               answer = title + ":" + para.text
               break
    else:
        answer = ""
    #canvas2.create_text(10, 225, anchor=NW, text=answer, font=('Candara Light', -25,'bold italic'),fill="white", width=350)
    #flag2 = False
    #loading.destroy()

    #p1=Thread(target=qs,args=(answer,))
    #p1.start()
    #p2 = Thread(target=transition2)
    #p2.start()
    print(answer+wiki)
    return answer+wiki

