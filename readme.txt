This python script will require the following dependancies to be installed:
pyaudio
opencv-python
pocketsphinx
keyboard


The script will let you pick which input to use for a microphone.

The Keyforge_Cards.csv, failedcards.txt, DarkTidings.dic, DarkTidings.lm and the Cards folder should be kept in the same folder as the Keyforge Voice.py python script.

If the script fails to match a card from the csv with a file, it will record it in failedcards.txt. To fix this, update the cardname in the folder to match the csv. The data in this txt file can be deleted as needed.

Words can be added or removed to the "nosearch" variable to help protect against false-positives or to prevent too many hits on common words

In order to function correctly, each row in the csv file should match an image name in the folder. Custom names can be added to the csv and images to get better matches. The script will replace " " with "-" in the csv file.

I have removed the punctuation from the card names (. ? ! ).

New cards can be added to the image folder and the names to the csv file to expand. A new dictionary will need to be created for new cards.

Tools for creating a custom dictionary (add words or new cards to the Keyforge Corpus txt file): 
	http://www.speech.cs.cmu.edu/tools/lmtool-new.html
	http://ghatage.com/tech/2012/12/13/Make-Pocketsphinx-recognize-new-words/

To Do:
-Add feedback from the microphone to the GUI
-Create an input panel on the GUI to select a keystroke
-Script currently waits for one final keypress when quitting after running in Keystroke mode. Find way to stop script
