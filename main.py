import sys
import urllib.request
from bs4 import BeautifulSoup
import genanki as anki
#--------------------------------------



# Webpage laden und Inhalt zuruck geben
def WepRipper(Link):
    uf = urllib.request.urlopen(Link)
    html = uf.read()

    return html

# uberschriften und Inhalt rippen und als Array ausgeben + Titel der Seite als Uberschrift
def Crawler(HTML):
    soup = BeautifulSoup(HTML)
    Titel = soup.title.string
    
    #dt ist die Uberschrift
    Header = soup.find_all("dt")
    #dd der Text
    Text = soup.find_all("dd")


    print(len(Header))
    print(len(Text))

    Inhalt = []
    for i in range(0,len(Header)-1):
        if (Text[i] == "."):
            continue

        obj = {}
        obj['Header'] = Header[i]
        obj['Text'] = Text[i]
        Inhalt.append(obj)
    
    return Titel, Inhalt


# Anki Karten erstellen
def createKard(Name, Inhalt):
    pass

def Error(Nachricht):
    print(Nachricht)
    sys.exit(0)


#--------------------------------------
# Main
if __name__ == "__main__":
    Links = sys.argv[1:]
    print(str(len(Links)) + " -> Links gefunden")
    if (len(Links)==0):
        Error("Keine Links gefunden!")

    HTML = []
    for i in Links:
        HTML.append(WepRipper(i))
    print(str(len(HTML)) + " -> webpages geladen")
    if(len(Links)==0):
        Error("Webpages konnten nicht geladen werden!")
    
    Inhalt = []
    for o in HTML:
        Inhalt.append(Crawler(o))
    
    for t in Inhalt:
        createKard(t[0], t[1:])
    
    Error("Finished!")