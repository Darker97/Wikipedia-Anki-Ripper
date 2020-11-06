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

    # Titel des Decks und der Datei
    Titel = soup.title.string
    
    Inhalt = []

    Chapters = soup.find_all("dl")
    # print("Chapters: " + str(len(Chapters)))

    for ch in Chapters:
        notes = ch.find_all("dt")
        # print("Notes: " + str(len(notes)))

        for no in notes:
            obj = {}
            obj['Header'] = no.text
            obj['Text'] = ""
            pointer = no
            # print(pointer.next_sibling.next_sibling)
            while (pointer.next_sibling.next_sibling.name == "dd"):
                obj['Text'] = obj['Text'] + pointer.text
                pointer = pointer.next_sibling.next_sibling
                if pointer.next_sibling.next_sibling == None:
                    break

            if (obj['Text'] == "." or obj['Text'] == " " or obj['Text'] == ""):
                continue    
            Inhalt.append(obj)

    # print(len(Inhalt))

    if (len(Inhalt) == 0):
        return Titel, []
    
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
    print("Deck: " + Name + " -> " + str(len(Inhalt)) + " Karten erstellt")
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
        if len(Inhalt) == 0:
            print(Titel + " Konnte nicht geladen werden")
            continue
        createKard(Titel, Inhalt)
        
    
    Error("Finished!")