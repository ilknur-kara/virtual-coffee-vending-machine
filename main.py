import os

import cv2
from cvzone.HandTrackingModule import HandDetector


class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (225, 225, 225), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                      (50, 50, 50), 3)
        cv2.putText(img, self.value, (self.pos[0] + 2, self.pos[1] + 50), cv2.FONT_HERSHEY_PLAIN,
                    2, (50, 50, 50), 2)

    def checkClick(self, x, y): # clikc fonksiyonu burası. Belirlenen mesafe 50 iki parmak arası 50 uzunluğu altındaysa ilk if kısmına giriyor
        if self.pos[0] < x < self.pos[0] + self.width and \
                self.pos[1] < y < self.pos[1] + self.height:
            cv2.rectangle(img, (self.pos[0] + 3, self.pos[1] + 3),
                          (self.pos[0] + self.width - 3, self.pos[1] + self.height - 3),
                          (255, 255, 255), cv2.FILLED)
            cv2.putText(img, self.value, (self.pos[0] + 25, self.pos[1] + 80), cv2.FONT_HERSHEY_PLAIN,
                        5, (0, 0, 0), 5)
            return True
        else:
            return False

#WebCam
cap = cv2.VideoCapture(0) #0 is for laptop webcam, 1 is for external webcam
cap.set(3, 1288) #width
cap.set(4, 720) #height
detector = HandDetector(detectionCon=0.8, maxHands=1)

#Create Button
buttonListValues = [['Filter Coffee', 'Americano'],
                    ['Latte', 'Mocha'],
                    ['Ristretto', 'Frappe'],
                    ['Espresso', 'Cappuccino'],
                    ['Continue', 'Pay it']]
buttonList = []
for x in range(2):
    for y in range(5):
        xpos = x * 280 + 350
        ypos = y * 80 + 200

        buttonList.append(Button((xpos, ypos), 300, 80, buttonListValues[y][x]))

#Variables
myChoice = ''
delayCounter = 0 #çoklu tıklamayı önlemek için sayaç oluşturduk

isContinue = False

imageFolderPath = "/Users/black/PycharmProjects/VirtualVendingMachine/resources"
imageList = os.listdir(imageFolderPath)
overlayList = []
for imagePath in imageList:
    image = cv2.imread(f'{imageFolderPath}/{imagePath}')
    print(f'{imageFolderPath}/{imagePath}')
    overlayList.append(image)

#Loop
while True:
    #Get image from webcam
    success, img = cap.read()
    img = cv2.flip(img, 1) #kamerayı döndürüyor.

    #Detection hand
    hands, img = detector.findHands(img, flipType=False)

    for button in buttonList:
        button.draw(img)

    #Finger Click
    if hands:
        lmList = hands[0]['lmList']
        length, _, img = detector.findDistance(lmList[8], lmList[12], img)
        print(length)
        x, y = lmList[8]
        if length < 50 and delayCounter == 0:
            for i, button in enumerate(buttonList):
                if button.checkClick(x, y):
                    myValue = buttonListValues[int(i % 5)][int(i / 5)]  # get correct number
                    if myValue == 'Filter Coffee':
                        myChoice = myValue + ' is chosen.'
                    elif myValue == 'Americano':
                        myChoice = myValue + ' is chosen.'
                    elif myValue == 'Latte':
                        myChoice = myValue + ' is chosen.'
                    elif myValue == 'Mocha':
                        myChoice = myValue + ' is chosen.'
                    elif myValue == 'Ristretto':
                        myChoice = myValue + ' is chosen.'
                    elif myValue == 'Frappe':
                        myChoice = myValue + ' is chosen.'
                    elif myValue == 'Espresso':
                        myChoice = myValue + ' is chosen.'
                    elif myValue == 'Cappuccino':
                        myChoice = myValue + ' is chosen.'
                    elif (myValue == 'Continue') & ((myChoice == 'Filter Coffee is chosen.') | (myChoice == 'Americano is chosen.') | (myChoice == 'Latte is chosen.') | (myChoice == 'Mocha is chosen.') | (myChoice == 'Ristretto is chosen.') | (myChoice == 'Frappe is chosen.') | (myChoice == 'Espresso is chosen.') | (myChoice == 'Cappuccino is chosen.')):
                        isContinue = True
                        myChoice = 'To continue, press pay it button.'
                    elif (myValue == 'Pay it') & isContinue:
                        myChoice = 'Your payment is done. Coffee is getting ready...'
                        isContinue = False #After payment is done, turn it to isContinue false to prevent to press payment directly.
                    else:
                        myChoice = '' #To prevent writing something to screen among clicks.

                    delayCounter = 1

    #Multi-click prevention
    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0

    #Display the Result
    cv2.putText(img, myChoice, (345, 110), cv2.FONT_HERSHEY_PLAIN,
                2, (225, 10, 10), 3)

    #Display Image
    key = cv2.waitKey(1)
    cv2.imshow("Virtual Coffee Vending Machine", img)
    #cv2.waitKey(1)
    if key == ord('c'): #burada klavyede c tuşuna basınca ekran sıfırlanıyor
        myChoice = ''



