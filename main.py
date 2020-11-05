import sys
import urllib.request



#--------------------------------------



# Webpage laden und Inhalt zurück geben
def WepRipper(Link):
    uf = urllib.request.urlopen(Link)
    html = uf.read()
    
    return html

# Überschriften und Inhalt rippen und als Array ausgeben + Titel der Seite als Überschrift
def Crawler(HTML):
    pass


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
    print(len(Links) + " -> Links gefunden")
    if (len(Links)==0):
        Error("Keine Links gefunden!")

    HTML = []
    for i in Links:
        HTML.append(WepRipper(i))
    print(len(HTML) + " -> webpages geladen")
    if(len(Links)==0):
        Error("Webpages konnten nicht geladen werden!")
    
    Inhalt = []
    for o in HTML:
        Inhalt.append(Crawler(o))
    
    for t in Inhalt:
        createKard(t[0], t[1:])
    
    Error("Finished!")