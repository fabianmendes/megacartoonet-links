import requests
from bs4 import BeautifulSoup
import html

import time

#web_url = input("Link 1º Ep. post, ")
web_url = "https://www.megacartoons.net/part-i-the-beginning/"

r = requests.get(web_url)
print(r.status_code)
soup = BeautifulSoup(r.content, "html.parser")


class Serie:

    def __init__(self):

        self.cartoon = ''  # <type str>
        self.ep_links= ()  # <type tuple of dicts>
        self.episodes= []  # <type set of objects>
        # save cartoon as "<album>"
        # TODO also, search for year&artist

    class Episode:

        def __init__(self, dictionary):

            self.name = dictionary['title']  # name of dictionary.

            #Serie.addEpisode(self.name)
            # save EPISODE name into "<title>"
            #  save number of chapter as well.
            # (is it possible save the Ep.Nº?)
            #  extract the brief→comment/note
            # and add the Ep's image!

            self.vurl, self.next = webLink(dictionary['href'])
        # ".mp4" link <str>, next-post url <str>.

            ic, bf = extractCoverbrief(dictionary['href'])
            self.img_cover = ic  # cover image!
            self.brief_snp = bf  # sinopsis ep.

            #self.chap_nums = dictionary["num"]
            # <trackNum>1</trackNum> <annotation>


def clean4Dict(lista):
    #	creates dictionary:
    dict_line = {}
    aux = []

    for i in range(len(lista)):

        aux = lista[i].split('=')
        aux[1] = aux[1].replace('"', '')

        dict_line[aux[0]] = aux[1]
    return dict_line


def createDict(raw_list, num = None):
    '''raw_ soup.find("
    '''
    raw_line = str(raw_list).split(">")

    desire_line = raw_line[0].split(" ")
    del desire_line[0]  # deletes "<dType"

    dict_line = clean4Dict(desire_line)
    #print(dict_line)
    #       ".mp4" link <str>, next-post url <str>.

    #return dict_line['value'], dict_line['href']
    return dict_line  #dictionary


def webLink(web_link):
    r = requests.get(web_link)
    # print(r.status_code)
    soup = BeautifulSoup(r.content, "html.parser")
    main_in = soup.find("input", attrs={"type": "hidden"})

    nextpost = soup.find("a", attrs={"class": "next"})

    return createDict(main_in)["value"], createDict(nextpost)["href"]


def extractCoverbrief(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, "html.parser")
    img_line = soup.find("img", attrs={"class": "fp-splash"})
    img_path = createDict(img_line)["src"]
    sinopsis = soup.find("div", attrs={"class": "item-content toggled"}).text

    return img_path, sinopsis


# LIMPIEZA DE CAPITULOS con el mismo link del 1er capitulo.
chapters_raw = soup.find("ul", attrs={"class": "video-series-list list-inline"})
#print(chapters_raw)
chapters_rawlist= str(chapters_raw).split('<li><a ')
del chapters_rawlist[0]

#numbers_chapter = chapters_raw.text
#numbers_chapter = numbers_chapter.split(" ")

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


for z in range(len(aa)-1):
    del aa[z][0]
    dict_aux = {}

    dict_aux[aa[z][0][0]] = aa[z][0][1]  # href = url (link post)
    dict_aux[aa[z][1][0]] = aa[z][1][1]  # title= name (chapter)
    #dict_aux["num"] = numbers_chapter[z] # chapter number. TODO?
    chapters_list.append(dict_aux)

#print(aa[z])
#print(chapters_list)

ver = Serie()
ver.cartoon = "Samurai Jack" + "-copy"
ver.ep_links= tuple(chapters_list)
#print(ver.ep_links)

vurls, cname, nextp = [], [], []

for i in range(len(ver.ep_links)):
    ex_dato = ver.ep_links[i]

    ver.episodes.append(ver.Episode(ex_dato))
    a = ver.episodes

    #print(a[-1])
    #print(a[-1].vurl + "\t" + a[-1].name + " " + a[-1].next)

    vurls.append(a[-1].vurl)
    cname.append(a[-1].name)
    nextp.append(a[-1].next)

    #time.sleep(0.5)

#import pandas
# PANDAS: -----------------------------------------
#Domain = ["IT", "DATA_SCIENCE", "NEYWORKING"]

domain_dict = {'Mp4 URLs': vurls, 'Episode': cname, 'Next C.': nextp}
#print(domain_dict)
#data_frame = pandas.DataFrame(domain_dict)
#data_frame.to_csv(ver.cartoon + '.csv')
#--------------------------------------------------
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
# def vlcPlaylist(convert):
#               ↓ (convert.episodes)
for i in range(len(ver.episodes) -1):
    inputLink = ver.episodes[i].vurl
    pista = subele(play_list, 'track')  # TRACK
    lugar = subele(pista, 'location')
    lugar.text = inputLink  #TODO def parameter.

    title = subele(pista, 'title')
    title.text = ver.episodes[i].name
    album = subele(pista, 'album')
    album.text = ver.cartoon

    track_num = subele(pista, 'trackNum')
    track_num.text = str(i +1)
    #track_num.text = ver.episodes[i].chap_nums
    comment = subele(pista, 'annotation')
    comment.text = ver.episodes[i].brief_snp
    cover = subele(pista, "image")
    cover.text = ver.episodes[i].img_cover

    ext_app = "http://www.videolan.org/vlc/playlist/0"
    extensionapp = subele(pista, 'extension')
    extensionapp.set('application', ext_app)

    vlc_id = subele(extensionapp, 'vlc:id')
    vlc_id.text = str(i)  # IMPORTANT, Nro track!!
    # TODO ^  position of the list!!
    vlc_opt = subele(extensionapp, 'vlc:option')
    vlc_opt.text = 'network-caching=1000'

# --- extension (o)ut o(f) trackLis(t): ~~~|
extensionapp_oft = subele(playlist, 'extension')
ext_app = "http://www.videolan.org/vlc/playlist/0"
extensionapp_oft.set('application', ext_app)
# items:
# <vlc:item tid="nro_idex_list_inputLink"/>
# for...
for trackid in range(len(ver.episodes) -1):
#trackid = 'None'
#TODO trackid = position.
    inside_i = 'vlc:item tid="' + str(trackid) + '"'
    vlc_item = subele(extensionapp_oft, inside_i)

print(playlist)  # print prittify(playlist)
# create a new XML file with the results: ↓

#tree = ET.ElementTree(vehicles)
#tree.write("vehicle_file.xml", xml_declaration=True, encoding='utf-8', method="xml")
# ^ code from https://norwied.wordpress.com/2013/08/27/307/
mydata = xee.ElementTree(playlist)
mydata.write(ver.cartoon + ".xspf",  # nameSerie
             xml_declaration=True,
             encoding='utf-8', method="xml")
#print(mydata)  # it prints xeEtEt object...


