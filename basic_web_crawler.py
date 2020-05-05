import urllib.request
import os
import sys
import platform
from bs4 import BeautifulSoup


#  TODO: cambiar script para usar otro user agent en vez del default porque lo detectan muchas paginas como bot

def text_desktop():
    user = os.getlogin()
    platf = str(platform.system())
    if platf == "Darwin":
        sys.stdout = open(f"/Users/{user}/reportCrawler.log", "w")
    elif platf == "Windows":
        sys.stdout = open(f"c:/users/{user}/reportCrawler.log", "w")
    else:
        sys.stdout = open(f"/home/{user}/reportCrawler.log", "w")


url = input("introduce url:")  # funcionan la gran mayoria de urls
print("un log se creara en la carpeta del usuario")
print(f"rastreando {url} y su nivel inferior...")
text_desktop()
html = urllib.request.urlopen(url)  # obtenemos pagina web haciendo peticion
soup = BeautifulSoup(html, "html.parser")  # lo transformamos a objeto BS para obtener etiquetas
tags = soup("a")  # extraemos las etiquetas del tipo indicado

print("ENLACES EN LA PAGINA PRINCIPLAL\r\n")
for tag in tags:
    if len(tag.get("href")) > 2:  # comprobamos que no sean enlaces vacios o erroneos
        print(tag.contents, tag.get("href"))  # texto de cada enlace y su url

        
print("\r\n\r\n ENLACES EN LAS PAGINAS SECUNDARIAS\r\n")
for tag in tags:
    newurl = tag.get("href")  # obtenemos los enlaces de dentro de la pag
    try:  # usamos bloque try-except para evitar enlaces caidos o de referencias relativas
        if newurl[0:4] == "http":  # comprobamos que la url comienze por http, lo que incluye https
            html2 = urllib.request.urlopen(newurl)
        else:
            html2 = urllib.request.urlopen(url + newurl)  # para casos de enlaces relativos (pag anterior+/....)
            soup2 = BeautifulSoup(html2, "html.parser")
            newtags = soup2("a")  # obtenemos nuevos tags
        if len(newtags) > 0:  # para comprobar que existen nuevos enlaces
            for newtag in newtags:
                if len(newtag.get("href")) > 2:
                    print(tag.contents, newtag.get("href"))
        else:
            print("no hay más enlaces")
    except:
        print("algo ha fallado")  # va a dar fallos porque habria que cambiar el agente usado

        
sys.stdout.close()
