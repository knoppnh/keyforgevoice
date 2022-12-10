import cv2, os.path, csv, re, pyaudio, time, keyboard, threading, datetime
from pocketsphinx import LiveSpeech
from statistics import multimode
import tkinter as tk
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

Location="Cards/"
display=8 #adjust this number to change how long in seconds until the image closes
fullcardlist=[]
cardlist=[] #create an empty list for the cards
errata = []
sets=[]
AllSets=[]
CoTA = []
AoA = []
WC = []
MM = []
DT = []
WoE = []
#GM=[]


window_name="Keyforge Match" #name of the window that this script opens when it finds a match 
keyword=["play", 'fight', 'reap'] #change these values to add keywords for speech recognition. new words will need to be added to the dictionary
keystroke="`" #change this value to use a different keyboard key for speech recognition
feedback=""
matches=""
i=0
j=0
k=0

mic=[]
countmics=0
micindex=0

kill=threading.Event()
kill.set()

window=tk.Tk()
window.geometry('400x300')
#window.resizable(False, False)
window.title("Keyforge Voice Helper")

#nosearch words are not checked for matches - add or remove words as needed
nosearch=["the","a", "and", "to", "it", "in", "i", "you", "of", "with", "is", "for", "or", "find"]

with open(resource_path("Keyforge_Cards.csv"), encoding="cp1252") as f: #opens list of cards and add them to a list
    for row in csv.reader(f):
        if row[2] == "CoTA":
            CoTA.append(row[0])
        if row[3] == "AoA":
            AoA.append(row[0])
        if row[4] == "WC":
            WC.append(row[0])
        if row[5] == "MM":
            MM.append(row[0])
        if row[6] == "DT":
            DT.append(row[0])
        if row[7] == "WoE":
            WoE.append(row[0])
        #if row[8] == "GM":
        #    GM.append(row[0])
        fullcardlist.append(row[0])
        errata.append(row[1])

image=""  #sets .png name to blank
number=len(fullcardlist) #finds number of cards in the card list
# print("Ready to find matches for " + str(number) + " Keyforge cards. The " + recog_type +"(s) is/are: "+ str(recognition))
# if rec_type == 2:
#     print('Press the ' + recognition + ' key to advance')

def searching(selected):
    speech = LiveSpeech(
        sampling_rate=16000,
        audio_device = micindex,
        lm=resource_path('Keyforge.lm'), #this is the language model file
        dic=resource_path('Keyforge.dic') #this is the dictionary file
    )
    j=0
    i=0
    k=0
    keyword=["play", 'fight', 'reap'] #change these values to add keywords for speech recognition. new words will need to be added to the dictionary
    keystroke="`" #change this value to use a different keyboard key for speech recognition
    while k==0:
        thread=threading.Thread(target=close, args=[selected])
        thread.start()
        k=+1
    else:
        if selected == 1:
            print("Using CONTINUOUS recognition")
            recognition=keyword
        if selected == 2:
            print("Using KEYSTROKE recognition")
            recognition=keystroke
            keyword=""
        print("Ready to find matches for Keyforge cards.")
        if selected ==1:
            print("The keywords(s) is/are: "+ str(recognition))
        if selected == 2:
            print('Press the ' + recognition + ' key to advance')
        while kill.is_set()==True:
            for phrase in speech:            
                if kill.is_set()==False:
                    print("End")
                    break
                Card=str(phrase).lower()
                feedback=Card
                if feedback!="":
                    response.configure(text="Heard: " + feedback)
                print(str(Card)) #this prints what the microphone hears to the shell
                Card=Card.split() #splits input into individual words to check
                Card=list(dict.fromkeys(Card)) #removes duplicate words from list
                #need to put a check in here to find only sets of cards in the data base
                cardlist=[]
                if cota.get()==1:
                    for row in range(len(CoTA)):
                        cardlist.append(CoTA[row])
                if aoa.get()==1:
                    for row in range(len(AoA)):
                        cardlist.append(AoA[row])
                if wc.get()==1:
                    for row in range(len(WC)):
                        cardlist.append(WC[row])
                if mm.get()==1:
                    for row in range(len(MM)):
                        cardlist.append(MM[row])
                if dt.get()==1:
                    for row in range(len(DT)):
                        cardlist.append(DT[row])
                if woe.get()==1:
                    for row in range(len(WoE)):
                        cardlist.append(WoE[row])
#                 if gm.get()==1:
#                     for row in range(len(GM)):
#                         cardlist.append(GM[row])



                cardlist = sorted(set(cardlist))
                number=len(cardlist) #finds number of cards in the card list


                match=[] #creates a list to add card matches
                duplicate=[] #creates a list to filter for multiple matches of the same card
                for i in Card:
                    if kill.is_set()==False:
                        print("End")
                        break
                    while j < number: #search through each row of the csv file for a match
                        if (re.search(r"\b"+i.lower()+r"\b",cardlist[j]) and i.lower() not in nosearch) and ([ele for ele in keyword if(ele in str(Card))] or keyword == ""): #looks for direct word matches and filters out words from nosearch
                            match.append(cardlist[j]) #adds card to list if it is a match
                            duplicate.append(j) #adds the row number to a list to determine how many matches a card gets
                        j=j+1
                    j=0
                    #match=list(dict.fromkeys(match)) #remove duplicate card matches
                for i in multimode(duplicate): #finds the mode of the matches
                    if len(multimode(duplicate)) <5: #limits the number of cards to less than 5 at a time
                        image=resource_path(Location+cardlist[i].replace(" ","-"))#+".png")
                        #Looks for extension and sets the image name
                        if os.path.isfile(image+".png") == True:
                            image=image+".png"
                        if os.path.isfile(image+".jpg") == True:
                            image=image+".jpg"
                        if os.path.isfile(image+".jpeg") == True:
                            image=image+".jpeg"
                        
                        matches=("FOUND " + str(len(multimode(duplicate)))+ " CARD MATCH(ES): " + cardlist[i])
                        found.configure(text=matches)
                        if errata[i] != "1":
                            print("Errata found: " + str(errata[i]))
                        if os.path.isfile(image) is True:
                            img=cv2.imread(image)
                            if errata[i] != "1":
                                 cv2.putText(img, "Errata'd" , (30, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_8)
                            img=cv2.resize(img,(300,420)) #this resizes the images
                            cv2.namedWindow(window_name, flags=cv2.WND_PROP_TOPMOST)
                            cv2.imshow(window_name, img)
                            if selected == 2:
                                cv2.waitKey(display*1000) 
                                #keyboard.wait(keystroke)
                            else:
                                cv2.waitKey(display*1000)
                            cv2.destroyAllWindows()
                            time.sleep(0.1)
                            image=""
                        else:
                            print("Could not find file " + cardlist[i])
                            with open("failedcards.txt", "a") as log:
                                log.write(str(datetime.datetime.now()) + " Could not find file " + cardlist[i])
                                log.write('\n')
                                log.close()
                            image=""
                if kill.is_set()==False:
                    print("End")
                    break
                if selected == 2:
                    keyboard.wait(keystroke)
                    time.sleep(0.1)
                if kill.is_set()==False:
                    print("End")
                    break
                pass

def changeset(change):
    change.get()
    if allsets.get()==1:
            cota.set(1)
            aoa.set(1)
            wc.set(1)
            mm.set(1)
            dt.set(1)
            woe.set(1)
            #gm.set(1)

def close(selected): #this window runs the searching script
    global close, response, found, matches
    close=tk.Tk()
    close.title("Keyforge Voice Helper")
    close.geometry('400x400')
    if selected == 1:
         Label=tk.Label(text="Using CONTINUOUS recognition")
         Label1= tk.Label(text='Say these words: ' +str(keyword) + " to recognize a card")
    if selected == 2:
         Label=tk.Label(text="Using KEYSTROKE recognition")
         Label1=tk.Label(text='Use this key: ' + str(keystroke) + " (you will need to hit this key to close the image window)")
    Button = tk.Button(close, text="Close Script", command = lambda: escape(selected))
    #Need to add check boxes here to allow you to pick which sets to pull from
    global allsets, cota, aoa, wc, mm, dt, woe#, gm
    allsets = tk.IntVar()
    cota = tk.IntVar()
    aoa = tk.IntVar()
    wc = tk.IntVar()
    mm = tk.IntVar()
    dt = tk.IntVar()
    woe = tk.IntVar()
    #gm=tk.IntVar()
    allsetsbox=tk.Checkbutton(close,text="All Sets", variable = allsets, command=lambda: changeset(allsets))
    cotabox=tk.Checkbutton(close,text="Call of the Archons", variable = cota, command=lambda: changeset(cota))
    aoabox=tk.Checkbutton(close,text="Age of Ascension", variable = aoa, command=lambda: changeset(aoa))
    wcbox=tk.Checkbutton(close,text="World's Collide", variable = wc, command=lambda: changeset(wc)) 
    mmbox=tk.Checkbutton(close,text="Mass Mutation", variable = mm, command=lambda: changeset(mm))
    dtbox=tk.Checkbutton(close,text="Dark Tidings", variable = dt, command=lambda: changeset(dt))
    woebox=tk.Checkbutton(close,text="Winds of Exchange", variable = woe, command=lambda: changeset(woe))
    #gmbox=tk.Checkbutton(close,text="GM", variable = gm, command=lambda: changeset(gm))
    
    allsets.set(1)
    changeset(allsets)
    allsets.set(0)
    
    response=tk.Label(close,textvariable=feedback) #this label outputs what the program 'heard'
    found=tk.Label(close,textvariable=matches) #this label outputs what the program finds
    Label.pack(side='top', anchor = 'w')
    Label1.pack(anchor='w')
    allsetsbox.pack(anchor='w')
    cotabox.pack(anchor='w')
    aoabox.pack(anchor='w')
    wcbox.pack(anchor='w')
    mmbox.pack(anchor='w')
    dtbox.pack(anchor='w')
    woebox.pack(anchor='w')
    #gmbox.pack(anchor='w')
        
    Button.pack(pady=20, anchor='center')
    response.pack(anchor='w')
    found.pack(anchor='w')
    close.mainloop()

def escape(selected):
    kill.clear()
    if selected ==2:
        keyboard.write(keystroke)
    close.destroy()

def selection(): #this selects the microphone inputs from the radio buttons
    global display
    selected = radio.get()
    display = delay.get()
    display=int(display)
    #print(deviceindex.get())
    for i in range(0,countmics):
        if mics[i]==deviceindex.get():
            micindex=int(mic[i])
    #print(mic)
    #print(micindex)
    window.destroy()
    searching(selected)

p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
mics=[]
#print(numdevices)

for i in range(0, numdevices): #this searches for connect mics and adds their names in a list
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        mics.append((p.get_device_info_by_host_api_device_index(0, i).get('name')))
        mic.append(p.get_device_info_by_host_api_device_index(0, i).get('index'))
        countmics=countmics+1
        #print(mic)
        #print(mics)


#This is the first window
deviceindex=tk.StringVar(value=mics[0])
drop=tk.OptionMenu(window, deviceindex, *mics)
radio = tk.IntVar()
Label= tk.Label(text="Choose a recognition type:")
r1= tk.Radiobutton(window, text="Always Listening", value=1, variable = radio)
r2= tk.Radiobutton(window, text="Keystroke  " + keystroke, value=2, variable = radio)
Button = tk.Button(window, text="Begin Voice Recognition", command = selection)
r2.select() #starts with keystroke recognition selected
delaylbl=tk.Label(text="Time for card window to display in seconds")
delay= tk.Entry(window)
delay.insert(0,8)

Label.pack(anchor = 'w')
r1.pack(anchor = 'w')
r2.pack(anchor ='w')
delaylbl.pack(anchor='w')
delay.pack()
miclabel=tk.Label(text="Choose a microphone:").pack(anchor='w')
drop.pack()
Button.pack(pady=40)
window.mainloop()