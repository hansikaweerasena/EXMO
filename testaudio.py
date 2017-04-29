import pyttsx
from pygame import mixer

def speak(a):
    engine = pyttsx.init()
    engine.setProperty('rate', 150)
    engine.setProperty('voice', 1)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
    engine.say(a)
    engine.runAndWait()


def speak2(file):
    mixer.init()
    mixer.sound.load('g:/EXMO/Tic tac toe/speak/'+ file)
    mixer.sound.play()
    print ("Playing audio"+ file)


def speak3(file):
    p = vlc.MediaPlayer("file:///g:/EXMO/Tic tac toe/speak/thank.mp3")
    p.play()
    
speak('Thank you for your time')


