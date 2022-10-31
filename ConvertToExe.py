import PyInstaller.__main__

PyInstaller.__main__.run([
    'KeyforgeVoice_0_3.py',
    '--add-data=Cards/;.',
    #'--add-data=en-us/;.',
    '--add-data=Keyforge_Cards.csv;.',
    '--add-data=Keyforge.lm;.',
    '--add-data=Keyforge.dic;.',
    '--add-data=failedcards.txt;.',
    #'--hidden-import=cv2,os.path,csv,re,pyaudio,time,keyboard,threading,pocketsphinx,numpy,multimode,multiprocessing,tkinter',
    #'-d=imports',
    '--onefile'#,
    #'--windowed'
])