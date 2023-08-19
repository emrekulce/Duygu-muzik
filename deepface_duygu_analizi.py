from deepface import DeepFace
import cv2
from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import time
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

def analiz_et():
    global duygu_global
    analiz1 = DeepFace.analyze("ben.jpg")
    duygu = analiz1[0]
    print("Duygu:",duygu["dominant_emotion"],"\nYaş",duygu["age"],"\nCinsiyet:",duygu["gender"],"\nMilliyet:",duygu["dominant_race"],"\n\n",duygu)
    duygu_global = duygu["dominant_emotion"]

def konusma(text):
    tts = gTTS(text,lang='tr')
    tts.save('mesaj.mp3')
    time.sleep(5)
    song = AudioSegment.from_mp3("mesaj.mp3")
    play(song)

def foto_cek():
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    cap.set(3,640) # set Width
    cap.set(4,480) # set Height

    durum = False
    while True:
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray,scaleFactor=1.2,minNeighbors=5,minSize=(20, 20))

        for (x,y,w,h) in faces:
            print("Yüz Algılandı")
            time.sleep(5)
            cv2.imwrite('ben.jpg',img)
            durum = True
            break

        cv2.imshow('video',img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
        if durum == True:
            break
    cap.release()
    cv2.destroyAllWindows()


def muzik_ac():
    time.sleep(1)
    browser = webdriver.Chrome()
    browser.get(f"https://www.youtube.com/results?search_query={duygu_global}+piano+songs+no+ads")
    videolar = browser.find_elements(By.CLASS_NAME,"ytd-item-section-renderer")
    print(f"{len(videolar)} tane video var")
    time.sleep(1)
    video_sec = random.randint(0,len(videolar)-1)
    videolar[video_sec].click()
    time.sleep(1)
    kac_dakika = browser.find_element(By.CLASS_NAME,"ytp-time-duration").text
    kac_dakika = kac_dakika.replace(':','0')
    print(kac_dakika)
    time.sleep(1)
    browser.minimize_window()
    time.sleep(int(kac_dakika))

def duygu_tr_ceviri():
    duygular = {'angry','disgust','fear','happy','sad','surprise','neutral'}
    global duygu_global_tr

    if duygu_global == 'angry':
        duygu_global_tr = 'kızgın'
    elif duygu_global == 'distust':
        duygu_global_tr = 'iğrenmiş'
    elif duygu_global == 'fear':
        duygu_global_tr = 'korkmuş'
    elif duygu_global == 'happy':
        duygu_global_tr = 'mutlu'
    elif duygu_global == 'sad':
        duygu_global_tr = 'üzgün'
    elif duygu_global == 'suprise':
        duygu_global_tr = 'şaşırmış'
    elif duygu_global == 'neutral':
        duygu_global_tr = 'normal'
    else:
        pass

if __name__ == "__main__":
    foto_cek()
    analiz_et()
    duygu_tr_ceviri()
    konusma(f"bugün biraz {duygu_global_tr} görünüyorsunuz efendim. size için modunuza uygun bir müzik açıyorum.")
    muzik_ac()
