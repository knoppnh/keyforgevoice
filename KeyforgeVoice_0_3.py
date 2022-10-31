import cv2, os.path, csv, re, pyaudio, time, keyboard, threading
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
cardlist=[] #create an empty list for the cards
errata = []
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
window.geometry('300x225')
window.resizable(False, False)
window.title("Keyforge Voice Helper")

#nosearch words are not checked for matches - add or remove words as needed
nosearch=["the","a", "and", "to", "it", "in", "i", "you", "of", "with", "is", "for", "or", "find"]

with open(resource_path("Keyforge_Cards.csv"), encoding="cp1252") as f: #opens list of cards and add them to a list
    for row in csv.reader(f):
        cardlist.append(row[0])
        errata.append(row[1])
image=""  #sets .png name to blank
number=len(cardlist) #finds number of cards in the card list
# print("Ready to find matches for " + str(number) + " Keyforge cards. The " + recog_type +"(s) is/are: "+ str(recognition))
# if rec_type == 2:
#     print('Press the ' + recognition + ' key to advance')

def searching(selected):
    speech = LiveSpeech(
        sampling_rate=16000,
        audio_device = micindex,
        lm=resource_path('Keyforge.lm'), #this is the language model file
        dic=resource_path('Keyforge.dic') #this is the dictionary file
        #hmm=resource_path('en-us/')
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
        print("Ready to find matches for " + str(number) + " Keyforge cards.")
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
                #res.pack(anchor = "w")
                print(str(Card)) #this prints what the microphone hears to the shell
                Card=Card.split() #splits input into individual words to check
                Card=list(dict.fromkeys(Card)) #removes duplicate words from list
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
                for i in multimode(duplicate): #finds the mode 
                    if len(multimode(duplicate)) <5: #limits the number of cards to less than 5 at a time
                        image=resource_path(Location+cardlist[i].replace(" ","-")+".png")
                        matches=("FOUND " + str(len(multimode(duplicate)))+ " CARD MATCH(ES): " + cardlist[i])
                        found.configure(text=matches)
                        if errata[i] != "1":
                            print("Errata found: " + str(errata[i]))
                        if os.path.isfile(image) is True:
                            img=cv2.imread(image)
                            if errata[i] != "1":
                                 cv2.putText(img, "Errata'd" , (30, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_8)
                            img=cv2.resize(img,(300,420))
                            cv2.imshow(window_name, img)
                            if selected == 2:
                                cv2.waitKey(display*1000+4000) 
                                #keyboard.wait(keystroke)
                            else:
                                cv2.waitKey(display*1000)
                                #time.sleep(display)
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
            
def close(selected): #this window runs the searching script
    global close, response, found, matches
    close=tk.Tk()
    close.title("Keyforge Voice Helper")
    close.geometry('400x150')
    if selected == 1:
         Label=tk.Label(text="Using CONTINUOUS recognition")
         Label1= tk.Label(text='Say these words: ' +str(keyword) + " to recognize a card")
    if selected == 2:
         Label=tk.Label(text="Using KEYSTROKE recognition")
         Label1=tk.Label(text='Use this key: ' + str(keystroke) + " (you will need to hit this key to close the image window)")
    Button = tk.Button(close, text="Close Script", command = lambda: escape(selected))
    response=tk.Label(close,textvariable=feedback) #this label outputs what the program 'heard'
    found=tk.Label(close,textvariable=matches) #this label outputs what the program finds
    Label.pack(side='top', anchor = 'w')
    Label1.pack(anchor='w')
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
    selected = radio.get()
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

deviceindex=tk.StringVar(value=mics[0])
drop=tk.OptionMenu(window, deviceindex, *mics)
radio = tk.IntVar()
Label= tk.Label(text="Choose a recognition type:")
r1= tk.Radiobutton(window, text="Always Listening", value=1, variable = radio)
r2= tk.Radiobutton(window, text="Keystroke  " + keystroke, value=2, variable = radio)
Button = tk.Button(window, text="Begin Voice Recognition", command = selection)
r1.select()

Label.pack(anchor = 'w')
r1.pack(anchor = 'w')
r2.pack(anchor ='w')
miclabel=tk.Label(text="Choose a microphone:").pack(anchor='w')
drop.pack()
Button.pack(pady=40)
window.mainloop()

