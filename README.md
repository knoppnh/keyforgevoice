This python script will require the following dependancies to be installed:
pyaudio
opencv-python
pocketsphinx

The csv file and the Keyforge card image folder should be kept in the same folder as the python script.

Words can be added or removed to the "nosearch" variable to help protect against false-positives or from too many hits

In order to function correctly, each row in the csv file should match an image name in the folder. Custom names can be added to the csv and images to get better matches. The script will replace " " with "-" in the csv file.

I have removed the punctuation from the card names (. ? ! ).
