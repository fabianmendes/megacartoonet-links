import requests
from bs4 import BeautifulSoup
import html

import time

#web_url = input("Link 1º Ep. post, ")
web_url = "https://www.megacartoons.net/part-i-the-beginning/"

r = requests.get(web_url)
print(r.status_code)
soup = BeautifulSoup(r.content, "html.parser")

#main_nxt =  TODO: Poner aqui el main_nxt. CREATES A Class, SERIE, Episode.
# TODO Create a def Next web_page.


# example for try:
# <header class="dark-div">
main_in = soup.find("input", attrs={"type": "hidden"})  # TODO CURRENT POST
# <input type="hidden" name="main_video_url" value="https://www.megacartoons.net/video/Samurai-Jack-I-The-Beginning.mp4">

main_list=str(main_in).split(">")
#print(main_list)

main_input= main_list[0].split(" ")
del main_input[0] #deletes '<input'
#print(main_input)
# -------- Cleaning to Dictionary.
main_inputdict = {}
aux = []

# clean to..
for i in range(len(main_input)):
    aux = main_input[i].split("=")
    aux[1] = aux[1].replace('"', '')  # deletes "
    main_inputdict[aux[0]] = aux[1]
    # my_dict['name']='Nick'
# ..dictionary.


'''
def cleanLink(raw_list):
    #raw_ soup.find("
    
    raw_line = str(raw_list).split(">")

    desire_line = raw_line[0].split(" ")
    del desire_line[0]  # deletes "<dType"

    dict_line = createDict(desire_line)

    #       ".mp4" link <str>, next-post url <str>.
    return dict_line['value'], dict_line['href']
'''

#print(dict_line)
#print(dict_line['value'])
# Link del video (".mp4") ^ .
time.sleep(1)
#print(main_in)

main_nxt = soup.find("a", attrs={"class": "next"})  # TODO NEXT POST
#print(main_nxt)

#dict_nxt = cleanBeauty(main_nxt)
#print(dict_nxt)
#print(dict_nxt['href'])

#print(soup)

class Serie():

    def __init__(self):

        self.cartoon = ''  # <type str>
        self.ep_links= ()  # <type tuple of dicts>
        self.episodes= []  # <type set of objects>

    def addEpisode(self, yes):
        a = list(self.episodes).append(yes)
        # self.episodes = set(a)


    class Episode():

        def __init__(self, dictionary):

            self.name = dictionary['title']  # name of dictionary.
            #Serie.addEpisode(self.name)

            #self.vurl = dictionary['value']

            self.vurl, self.next = webLink(dictionary['href'])
            #       ".mp4" link <str>, next-post url <str>.
            #self.next = dictionary['href']


def clean4Dict(lista):
    #	creates dictionary:
    dict_line = {}
    aux = []

    for i in range(len(lista)):
        aux = lista[i].split('=')
        aux[1] = aux[1].replace('"', '')

        dict_line[aux[0]] = aux[1]
    return dict_line


def createDict(raw_list):
    '''raw_ soup.find("
    '''
    raw_line = str(raw_list).split(">")

    desire_line = raw_line[0].split(" ")
    del desire_line[0]  # deletes "<dType"

    dict_line = clean4Dict(desire_line)
    #print(dict_line)
    #       ".mp4" link <str>, next-post url <str>.

    # TODO method para hallar el next-post.
    #return dict_line['value'], dict_line['href']
    return dict_line  #dictionary


def webLink(web_link):
    r = requests.get(web_link)
    # print(r.status_code)
    soup = BeautifulSoup(r.content, "html.parser")
    main_in = soup.find("input", attrs={"type": "hidden"})

    nextpost = soup.find("a", attrs={"class": "next"})

    return createDict(main_in)["value"], createDict(nextpost)["href"]


def linkNext(post):


    return


# LIMPIEZA DE CAPITULOS con el mismo link del 1er capitulo.
chapters_raw = soup.find("ul", attrs={"class": "video-series-list list-inline"})
#print(chapters_raw)
chapters_rawlist= str(chapters_raw).split('<li><a ')
del chapters_rawlist[0]

aux_crl = []
for i in range(len(chapters_rawlist)):
    aux_crl.append(chapters_rawlist[i].split('" '))
    aux_crl[-1][2] = aux_crl[-1][2].split('><i ')
    aux_crl[-1][2] = aux_crl[-1][2][0]

#print(aux_crl)
aa = []
for i in range(len(aux_crl)):
    aaa = []
    for j in range(len(aux_crl[i])):
        aux_crl[i][j] = aux_crl[i][j].split("=")
        if j >= 1:
            aux_crl[i][j][1] = aux_crl[i][j][1].replace('"', '')
        aaa.append(aux_crl[i][j])
    aa.append(aaa)
chapters_list = []
print("Nro de Capitulos:", len(aa))


for z in range(len(aa) -1):
    del aa[z][0]
    dict_aux = {}

    dict_aux[aa[z][0][0]] = aa[z][0][1]  # href = url (link post)
    dict_aux[aa[z][1][0]] = aa[z][1][1]  # title= name (chapter)
    chapters_list.append(dict_aux)

#print(aa)
#print(chapters_list)

ver = Serie()
ver.cartoon = "Samurai Jack"
ver.ep_links= tuple(chapters_list)
#print(ver.ep_links)
vurls, cname, nextp = [], [], []
for i in range(len(ver.ep_links)):
    ex_dato = ver.ep_links[i]

    ver.episodes.append(ver.Episode(ex_dato))
    a = ver.episodes
    print(a[-1])
    print(a[-1].vurl + "\t" + a[-1].name + " " + a[-1].next)

    vurls.append(a[-1].vurl)
    cname.append(a[-1].name)
    nextp.append(a[-1].next)

    #time.sleep(0.5)

#import pandas

#Domain = ["IT", "DATA_SCIENCE", "NEYWORKING"]

domain_dict = {'Mp4 URLs': vurls, 'Episode': cname, 'Next C.': nextp}
#print(domain_dict)

#data_frame = pandas.DataFrame(domain_dict)

#data_frame.to_csv(ver.cartoon + '.csv')

from xml.etree.ElementTree import Element as ele, SubElement as subele
import xml.etree.ElementTree as xee

inputLink = '.mp4'  # It's parameter of funct.
#top = 'playlist'
playlist = ele('playlist')  # (top)
playlist.set('xmlns', "http://xspf.org/ns/0/")
playlist.set('xmlns:vlc', "http://www.videolan.org/vlc/playlist/ns/0/")
playlist.set('version', "1")
list_rep = subele(playlist, 'title')
list_rep.text = "Lista de reproducción"

play_list = subele(playlist, 'trackList')
# repetir desde aqui ----- \/ , iterations.
pista = subele(play_list, 'track')  # TRACK
lugar = subele(pista, 'location')
lugar.text = inputLink  #TODO def parameter.
ext_app = "http://www.videolan.org/vlc/playlist/0"
extensionapp = subele(pista, 'extension')
extensionapp.set('application', ext_app)

vlc_id = subele(extensionapp, 'vlc:id')
vlc_id.text = '0'  # IMPORTANT, Nro track!!
# TODO ^  position of the list!!
vlc_opt = subele(extensionapp, 'vlc:option')
vlc_opt.text = 'network-caching=1000'

# --- extension (o)ut o(f) trackLis(t): ~~~|
extensionapp_oft = subele(playlist, 'extension')
extensionapp_oft.set('application', ext_app)
# items:
# <vlc:item tid="nro_idex_list_inputLink"/>
# for...
trackid = 'None'
#TODO trackid = position.
inside_i = 'vlc:item tid="' + trackid + '"'
vlc_item = subele(extensionapp_oft, inside_i)

print(playlist)  # print prittify(playlist)

#print(etree.tostring(playlist, encoding='unicode', pretty_print=True))
# create a new XML file with the results
mydata = xee.tostring(playlist, encoding='utf8', method='xml')
#thanks to "Martijn Pieters♦" at https://stackoverflow.com/questions/15304229/convert-python-elementtree-to-string/15304351#15304351
print(mydata)
myfile = open("megatry.xml", "w")
myfile.write(mydata)