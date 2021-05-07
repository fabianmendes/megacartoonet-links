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

	''''
    def addEpisode(self, yes):
        a = list(self.episodes).append(yes)
        # self.episodes = set(a)
	''''

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
    r = requests.get(web_url)
    # print(r.status_code)
    soup = BeautifulSoup(r.content, "html.parser")
    main_in = soup.find("input", attrs={"type": "hidden"})

    nextpost=  soup.find("a", attrs={"class": "next"})  # TODO NEXT POST)

    return createDict(main_in)["value"], createDict(nextpost)["href"]


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
for i in range(len(ver.ep_links)):
    ex_dato = ver.ep_links[i]

    ver.episodes.append(ver.Episode(ex_dato))
    a = ver.episodes
    
	#print(a[-1])  # Class storage Obj.
    print(a[-1].vurl + "\t" + a[-1].name + '\n')
    #ver.ep_links[i][1] = ver.episodes[i][1]  # clean dict.

    #time.sleep(0.5)
