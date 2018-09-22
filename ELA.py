import requests
from tkinter import Tk
import time
from bs4 import BeautifulSoup
import random
import webbrowser
import os

#u = 'https://www.merriam-webster.com/dictionary/'




def getsyl(key):
  url = 'https://www.howmanysyllables.com/words/%s'%key   #a online service provide the function which can seperate word pieces by syllables
  s = requests.Session()                                  #form a new session
  res = s.get(url)                                        #use GET method to send requests to server
  soup = BeautifulSoup(res.text, 'html.parser')           #use bs4 to help us get sth we want in response web page
  #f = soup.find('span', class_='word-syllables')
  f = soup.find_all('span', class_='Answer_Red')          #find all <span> tags that include in '.Answer_Red' class beacause piecies of word are in this class
  #print(url)
  if len(f) != 0:       #if we find sth
    try:
      f = f[1]                                              #we want the second <span> tag in '.Answer_Red' class
      return f.text.replace(' ', '').replace('\n', '').split('-')  #drop all ' ' and '\n' char and split pieces by '-' and return
    except:
      return None
  else:
    return None                                           #'WRONG : CAN\'T NOT FIND THE WORD "%s"'%key

    
def getpics(key):
  url = 'https://www.google.com/search?q=%s&tbm=isch'%key  #google pictures url. if we want search some keyword on it we need to put our keyword in q argument
  
  #randomly choose 5 pics from the results of google picture
  n = [0]     #and we want the first pic
  box = list(range(1,20))
  random.shuffle(box)
  n += box[:4]
  #n = list(range(19))   
  s = requests.Session()
  s.headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'})#to imitate the real browser(firefox)
  res = s.get(url)
  soup = BeautifulSoup(res.text, 'html.parser')
  #imgs = soup.find_all('img', class_='rg_ic rg_i', src=True)      #find all <img> tags
  imgs = soup.find_all('script', nonce=True)                       #find all <script> tags with nonce 
  #print(n)
  pics = []
  for i in imgs:
    if len(str(i)) > 100000 and 'data:image/' in str(i):
      urls = str(i).split('"')
      #print(i)
      #print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

  #print(len(urls))
  
  pics = [u for u in urls if 'data:image/' in u]                   #we want the results included 'data:image/' because the string is a picture's singnal
  pics = [pics[i].replace('\\u003d', '=') for i in n]                                      #pick up the randomly 5  pics we want from 20 pics
  #print(pics)
  #print(len(pics))
  
  return pics
  

#to form a html page for vocabulary
def html(key, pics, syl, audio, data):

  fname = '%s\\%s.html'%(path, key)
  f = open(fname, 'w')
  
  css = '''
  <style>
  
  img{
      border-radius: 10px;
  }
  c{
      font-size: 150pt;
      //color: aqua;
      
  }
  .gre{
      font-family: "Comic Sans MS";
      color: #008744;
  }
  .blu{
      font-family: "Comic Sans MS";
      color: #0057e7;
  }
  .re{
      font-family: "Comic Sans MS";
      color: #d62d20;
  }
  .yel{
      font-family: "Comic Sans MS";
      color: #ffa700;
  }
  li{
      width: 90%;
      font-family: "Comic Sans MS";
  }
  .sen{
      font-size: 20pt;
      width: 100%;
      padding-left: 50pt;
      padding-right: 50pt;
  }
  .exp{
      font-size: 28pt;
      color: red;
      font-weight: bold;
      font-family: "Comic Sans MS";
  }
  
  </style>
  '''
  brk = '<br>'
  colors = ['gre', 'blu', 're', 'yel']
  pickup = chooseColor(colors)
  f.write(css)
  f.write('<div width="100%" align="center">')
  for p in pics[:5]:
    f.write('<img src="%s">\n'%p)
  f.write('</div>')
  f.write('%s\n'%(brk*5))
  f.write('<div width="100%" align="center">')
  for s in range(len(syl)):
    f.write('<c class="%s">%s</c>'%(pickup[s], syl[s]))
  f.write('</div>%s\n'%(brk*5))
  f.write('<div style="align:center;width:100%;"><br>\n')
  f.write('<div style="background-color:#FFAFFE;width:80%;margin:0 auto;padding-left:20pt;border-radius: 30px;">\n\n')
  for d in data:
    #print(d)
    for i in range(len(d)):
      if i == 0:
        try:
          sth = d[i].text
        except:
          sth = key
        f.write('<a class="exp"><br>> %s<br></a><br>\n<div class="sen">\n<br>\n'%sth)
      else:
        f.write('<li>%s<br><br></li>\n'%d[i])
    f.write('%s\n</div>\n'%(brk*2))  ######'%s\n</div>'%brk*2  ====>  'brk\n</div>'*2   correct: '%s\n</div>'%(brk*2)  =====>  'brk\n</div>'  XDDDDDDDDDDDDDDDDD
    #f.write('\n</div>\n')
  f.write('</div></div>')
  
  f.write('<audio src="https://dictionary.cambridge.org%s" autoplay loop>'%audio)
  f.close()
  
  return fname
  
  
def chooseColor(colors):
  random.shuffle(colors)
  return colors*3


def get_sth_from_cambridge(key):

  url = 'https://dictionary.cambridge.org/zht/詞典/英語/%s'%key
  s = requests.Session()
  s.headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'})#to imitate the real browser(firefox)
  res = s.get(url)
  soup = BeautifulSoup(res.text, 'html.parser')
  audio = soup.find('span', class_='circle circle-btn sound audio_play_button', title='%s: listen to British English pronunciation'%key)['data-src-mp3']
  div = soup.find_all('div', class_='def-block pad-indent')
  
  data = []
  for d in div:
    soup = BeautifulSoup(str(d), 'html.parser')
    exp = soup.find('b', class_='def')
    sen = soup.find_all('span', class_='eg')
    data.append([exp] + sen)
    
  
  return audio, data

copy = Tk()
copy.withdraw()            #not show the windows
#try to get text from clipboard and put it into tmp
#if there's nothing in clipboard put '' into tmp
try:
  tmp = copy.clipboard_get()
except:
  tmp = ''
print(tmp)
  
path = 'Vocs'
os.system('mkdir %s'%path)
  
while True:
  time.sleep(1)                 #waiting for a second
  now = copy.clipboard_get()    #get text from clipboard
  if tmp != now:                #if tmp != sth in clipboard now means user copys new string and we want it
    tmp = now
    print('\nORIGIN : %s'%now)
    key = now.lower().replace(' ', '')   #convert all the aphabets into lower type because that is a easier way to Manipulate string
                                         #to drop all space(' ') in the copied string because we only want the vocabulary
   
    #check if sth we copied is not a legal vocabulary
    wrong = False
    for i in key:
      if not (ord(i) >= 97 and ord(i) <= 122):     #check if some char is not in the range of 'a-z'
        wrong = True
        print('WRONG : %s'%key)
    if wrong == True:                              #if this is illegal vocabulary finish this round
      continue
      
    syl = getsyl(key)  #seperate the vocbulary by syllables
    if syl == None:    #if this can not find this word's syllables maybe it's not legal english word , so we drop it
      continue
    
    pics = getpics(key)    #crawl 5 pictures from google randomly 
    audio, data = get_sth_from_cambridge(key)
    fname = html(key, pics, syl, audio, data)
    #print(pics)
    print(syl)
    print('OK : %s'%key)
    webbrowser.open(fname)
  
  
  
  
  
  
  
  
  '''
  key = copy.clipboard_get().lower().replace(' ', '')
  wrong = False
  for i in key:
    if not (ord(i) >= 97 and ord(i) <= 122):
      wrong = True
  if wrong != False and tmp != key:
  ''' 

