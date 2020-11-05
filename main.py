import sys
import urllib.request
from bs4 import BeautifulSoup
import genanki
import random
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
        if (Text[i].text == "." or Text[i].text == " " or Text[i].text == ""):
            continue

        obj = {}
        obj['Header'] = Header[i].text
        obj['Text'] = Text[i].text
        Inhalt.append(obj)
    
    return Titel, Inhalt


# Anki Karten erstellen
def createKard(Name, Inhalt):
    my_model = genanki.Model(
        random.randrange(1 << 30, 1 << 31),
        'PythonAutomatedCards',
        fields=[
            {'name': 'Definition'},
            {'name': 'Answer'},
        ],
        templates=[
            {
            'name': 'Card 1',
            'qfmt': '{{Question}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
    ])
    my_deck = genanki.Deck(random.randrange(1 << 30, 1 << 31), Name)

    for i in Inhalt:
        Header = i['Header']
        Text = i['Text']
        # print(Header + " --> " + Text)

        my_note = genanki.Note(
            model=my_model,
            fields=[Header, Text]
        )
        my_deck.add_note(my_note)

    genanki.Package(my_deck).write_to_file(Name + '.apkg')
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
    
    for o in HTML:
        Titel, Inhalt = Crawler(o)
        createKard(Titel, Inhalt)
        
    
    Error("Finished!")