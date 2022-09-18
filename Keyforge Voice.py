import cv2, os.path, csv, re
from pocketsphinx import LiveSpeech
from collections import OrderedDict

Location="Cards/"
display=3500 #adjust this number to change how long until the image closes
cardlist=[]
j=0
#nosearch words are not checked for matches
nosearch=["the","a", "and", "to", "it", "in", "i", "twin"]

with open("Keyforge_Cards.csv") as f: #opens list of cards and add them to a list
    for row in csv.reader(f):
        cardlist.append(row[0])
image=""  #sets .png name to blank
number=len(cardlist)

for phrase in LiveSpeech():
    Card=str(phrase).split() #splits input into individual cardlist to check
    print(Card)
    Card=list(dict.fromkeys(Card)) #removes duplicate words from list
    #print(Card)
    match=[]
    for i in Card:
        while j < number: #search through each row for a match
            if re.search(r"\b"+i+r"\b",cardlist[j]) and i not in nosearch:            
                #print(cardlist[j])
                match.append(cardlist[j])
                #image=Location+cardlist[j].replace(" ","-")+".png"
                #while os.path.isfile(image):
                #    img=cv2.imread(image)
                #    cv2.imshow("Keyforge", img)
                #    cv2.waitKey(display)
                #    cv2.destroyAllWindows()
                #    #Card=""
                #    image=""
            j=j+1
            #print(j)
        j=0
    match=list(dict.fromkeys(match))
    for i in match:
        image=Location+i.replace(" ","-")+".png"
        while os.path.isfile(image):
            img=cv2.imread(image)
            cv2.imshow("Keyforge", img)
            cv2.waitKey(display)
            cv2.destroyAllWindows()
            image=""
    cardcheck=""
    pass