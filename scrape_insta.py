
from PIL import Image
import pyautogui
import time
import os
import tkinter

### To get Clipboard:
import ctypes

OpenClipboard = ctypes.windll.user32.OpenClipboard
EmptyClipboard = ctypes.windll.user32.EmptyClipboard
GetClipboardData = ctypes.windll.user32.GetClipboardData
SetClipboardData = ctypes.windll.user32.SetClipboardData
CloseClipboard = ctypes.windll.user32.CloseClipboard
CF_UNICODETEXT = 13
GlobalAlloc = ctypes.windll.kernel32.GlobalAlloc
GlobalLock = ctypes.windll.kernel32.GlobalLock
GlobalUnlock = ctypes.windll.kernel32.GlobalUnlock
GlobalSize = ctypes.windll.kernel32.GlobalSize
GMEM_MOVEABLE = 0x0002
GMEM_ZEROINIT = 0x0040

unicode_type = type(u'')

def cb_get():
    text = None
    OpenClipboard(None)
    handle = GetClipboardData(CF_UNICODETEXT)
    pcontents = GlobalLock(handle)
    size = GlobalSize(handle)
    if pcontents and size:
        raw_data = ctypes.create_string_buffer(size)
        ctypes.memmove(raw_data, pcontents, size)
        text = raw_data.raw.decode('utf-16le').rstrip(u'\0')
    GlobalUnlock(handle)
    CloseClipboard()
    return text

print(os.getcwd())

## IKMZ
#pytesseract.pytesseract.tesseract_cmd = r"C:\Users\mawett\AppData\Local\Tesseract-OCR\tesseract"

## Laptop
#pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract"

#testfile = "Posting_011.png"
#print(pytesseract.image_to_string(Image.open(testfile)))

def bereinigen(text):
    text = text.replace('\n','  ')
    outtext = ''
    for c in text:
        if c.upper() == c.lower():
            outtext += ' '
        else:
            outtext += c.lower()

    while '  ' in outtext:
        outtext = outtext.replace('  ', ' ')
    return outtext

def trial1():
    ## get current screensize

    ss = pyautogui.size()
    print(ss)
    print(type(ss))

    print('Breite:',ss[0])
    print('Hoehe:',ss[1])

def trial2():
    ## get current mouse position

    mp = pyautogui.position()
    print(mp)
    print(type(mp))

def trial3():
    ## move mouse 100 pixels southwest

    mp = pyautogui.position()
    newx = mp[0]-100
    newy = mp[1]+100

    pyautogui.moveTo(newx,newy, duration=4)

    # Alternatively use relative movement
    pyautogui.moveRel(-100,100,duration=4)

def trial4():
    ## Drag mouse (select text in the region dragged over)
    ## This will select part of the script after clicking on 'Run'
    pyautogui.moveRel(-100,-20,duration=0)
    pyautogui.dragRel(0,200,duration=.5)


def trial5():
    ## Get multiple mouse locations with 3 sec intervals to plan a clickpath
    for i in range(5):
        print(pyautogui.position())
        time.sleep(3)

def trial6():
    ## Use the coordinates to click on 'Save' (have to click on the 'R' of Run
    pyautogui.moveRel(-120,-61,duration=2)
    pyautogui.click()
    pyautogui.moveRel(0,147,duration=2)
    pyautogui.click()

def trial7():
    ## Use scrolling on this script
    pyautogui.moveRel(0,100,duration=0)
    pyautogui.scroll(1)
    time.sleep(1)
    pyautogui.scroll(1)
    time.sleep(1)
    pyautogui.scroll(-1)

def trial8():
    ## go to the bottom of this page and write something.

    pyautogui.moveRel(0,580,duration=1)
    pyautogui.click()
    pyautogui.typewrite("Hello World\nI am a Ghost\n\n## BOOOH", interval=.1)

    pyautogui.typewrite(['enter','enter','h','e','l','l','o','space',
                         'w','r','o','l','d','backspace',
                         'backspace','backspace','backspace',
                         'o','r','l','d'],interval=.5)


def trial9():
    ## Copy and Paste from the script to the bottom of the page.
    pyautogui.moveRel(-100,-20,duration=0)
    pyautogui.dragRel(0,200,duration=.5)

    pyautogui.hotkey('ctrl','c')

    pyautogui.moveRel(0,400,duration=1)
    pyautogui.click()

    pyautogui.hotkey('ctrl','v')
    

def trial10():
    ## User Prompts
    pyautogui.alert("Gugguseli",button="Dada")
    a = pyautogui.confirm("Wollen Sie wirklich weiter machen?",buttons=("Ja","Nein"))
    print(a)
    b = pyautogui.prompt("Geben Sie einen Text ein:",default="Nein")
    print(b)


def trial11():
    ## Take a screenshot
    pyautogui.alert("Please go to the view you need, then click OK")

    time.sleep(1)
    pyautogui.screenshot("Testscreen.png")

    time.sleep(2)
    pyautogui.screenshot("Testscreen2.png")


def trial14():
    ## OCR eines Screenshots machen
    pyautogui.alert("Please go to the view you need, then click OK")

    time.sleep(1)
    bild = pyautogui.screenshot("Testscreen.png")

    contents = pytesseract.image_to_string(bild)

    print(contents)


def instagrab():
    pyautogui.alert("Ensure that the first post of the instagram page is opened and the 'next'-Arrow is visible.\nConfirm with 'OK' and move the mouse on this arrow within 5 seconds.")
    time.sleep(5)

    x1 = 540    ## Bildausschnitt, der abfotografiert wird
    x2 = 1030-x1
    y1 = 150
    y2 = 1050-y1
    capturebox = (x1,y1,x2,y2)

    for i in range(10000): ## Nummerier die Bilder von 0 bis 10'000
        try:
            fname = "c:/temp/Picture_{0:06}.png".format(i)
            bild = pyautogui.screenshot(fname,region=capturebox)  ## Screenshot

            pyautogui.hotkey('ctrl','a')  ## Inhalt kopieren
            time.sleep(0.5)
            pyautogui.hotkey('ctrl','c')

            contents = cb_get()

            fname = "Caption_{0:06}.txt".format(i)
            outf = open(fname,"w",encoding="utf-8")
            try:
                outf.write(contents)
            except:
                outf.write("ERROR: Not able to read text as UTF-8")
            outf.close()
        except:
            print("There was an Error on Posting #"+str(i))

        pyautogui.click() ## Weiter-Pfeil klicken
        time.sleep(3)  ## 3 Sekunden warten, bis Inhalte gelesen werden (Ladezeit).


instagrab()




