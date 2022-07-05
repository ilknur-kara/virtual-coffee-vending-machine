import cv2
from cvzone.HandTrackingModule import HandDetector
import time


class Button:
    # Constructor of the Button class
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

    def checkClick(self, x, y):
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


# Photo identification
imgBackground = cv2.imread("/Users/black/PycharmProjects/VirtualVendingMachine/resources/background.png")
imgEspBg = cv2.imread("/Users/black/PycharmProjects/VirtualVendingMachine/resources/espressobg.png")
imgAmeBg = cv2.imread("/Users/black/PycharmProjects/VirtualVendingMachine/resources/americanobg.png")
imgCapBg = cv2.imread("/Users/black/PycharmProjects/VirtualVendingMachine/resources/cappuccinobg.png")
imgContBg = cv2.imread("/Users/black/PycharmProjects/VirtualVendingMachine/resources/continiuebg.png")
imgFilterBg = cv2.imread("/Users/black/PycharmProjects/VirtualVendingMachine/resources/filterbg.png")
imgFrappeBg = cv2.imread("/Users/black/PycharmProjects/VirtualVendingMachine/resources/frappebg.png")
imgLatteBg = cv2.imread("/Users/black/PycharmProjects/VirtualVendingMachine/resources/lattebg.png")
imgMochaBg = cv2.imread("/Users/black/PycharmProjects/VirtualVendingMachine/resources/mochabg.png")
imgPayBg = cv2.imread("/Users/black/PycharmProjects/VirtualVendingMachine/resources/paybg.png")
imgPayBg2 = cv2.imread("/Users/black/PycharmProjects/VirtualVendingMachine/resources/pay2.jpeg")
imgRisseBg = cv2.imread("/Users/black/PycharmProjects/VirtualVendingMachine/resources/ristrettobg.png")

# WebCam
cap = cv2.VideoCapture(0)  # 0 is for laptop webcam, 1 is for external webcam
cap.set(3, 1288)  # Width
cap.set(4, 720)  # Height
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Create Button
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

        if y == 4:
            ypos = ypos + 50

        buttonList.append(Button((xpos, ypos), 300, 80, buttonListValues[y][x]))

# Variables
myChoice = ''
delayCounter = 0
counter = 0
isContinue = False

myChoiceImg = imgBackground


# Loop
def chosen_value(chosen):
    return chosen + " is chosen."


while counter < 2:
    # Get image from webcam
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Detection hand
    hands, img = detector.findHands(img, flipType=False)

    # # Display Image
    # key = cv2.waitKey(1)
    # # cv2.imshow("Virtual Coffee Vending Machine", img)
    #
    # if key == ord('c'):
    #     img = cv2.addWeighted(img, 0.2, myChoiceImg, 0.8, 0)
    #     for button in buttonList:
    #         button.draw(img)

    # Overlaying the background image
    if counter < 1:
        img = cv2.addWeighted(img, 0.2, myChoiceImg, 0.8, 0)
        for button in buttonList:
            button.draw(img)
    else:
        time.sleep(1)
        img = cv2.flip(img, 1)
        myChoiceImg = imgPayBg2
        img = cv2.addWeighted(img, 0.2, myChoiceImg, 0.8, 0)
        myChoice = ''
        myChoiceImg = imgBackground

    # Finger Click
    if hands:
        lmList = hands[0]['lmList']
        length, _, img = detector.findDistance(lmList[8], lmList[12], img)
        print(length)
        x, y = lmList[8]
        if length < 50 and delayCounter == 0:
            for i, button in enumerate(buttonList):
                if button.checkClick(x, y):
                    myValue = buttonListValues[int(i % 5)][int(i / 5)]  # Get correct number
                    if myValue == 'Filter Coffee':
                        myChoice = chosen_value(myValue)
                        myChoiceImg = imgFilterBg
                    elif myValue == 'Americano':
                        myChoice = chosen_value(myValue)
                        myChoiceImg = imgAmeBg
                    elif myValue == 'Latte':
                        myChoice = chosen_value(myValue)
                        myChoiceImg = imgLatteBg
                    elif myValue == 'Mocha':
                        myChoice = chosen_value(myValue)
                        myChoiceImg = imgMochaBg
                    elif myValue == 'Ristretto':
                        myChoice = chosen_value(myValue)
                        myChoiceImg = imgRisseBg
                    elif myValue == 'Frappe':
                        myChoice = chosen_value(myValue)
                        myChoiceImg = imgFrappeBg
                    elif myValue == 'Espresso':
                        myChoice = chosen_value(myValue)
                        myChoiceImg = imgEspBg
                    elif myValue == 'Cappuccino':
                        myChoice = chosen_value(myValue)
                        myChoiceImg = imgCapBg
                    elif (myValue == 'Continue') & ((myChoice == 'Filter Coffee is chosen.') | (myChoice == 'Americano is chosen.') | (myChoice == 'Latte is chosen.') | (myChoice == 'Mocha is chosen.') | (myChoice == 'Ristretto is chosen.') | (myChoice == 'Frappe is chosen.') | (myChoice == 'Espresso is chosen.') | (myChoice == 'Cappuccino is chosen.')):
                        isContinue = True
                        myChoice = 'To continue, press pay it button.'
                        myChoiceImg = imgContBg
                    elif (myValue == 'Pay it') & isContinue:
                        myChoice = 'Your payment is done. Coffee is getting ready...'
                        # After payment is done, turn it to isContinue false to prevent to press payment directly.
                        isContinue = False
                        myChoiceImg = imgPayBg
                        counter = counter + 1
                    else:
                        # To prevent writing something to screen among clicks.
                        myChoice = ''

                    delayCounter = 1

    # Multi-click prevention
    if delayCounter != 0:
        delayCounter += 5
        if delayCounter > 50:
            delayCounter = 0

    # Display the Result
    cv2.putText(img, myChoice, (270, 120), cv2.FONT_HERSHEY_PLAIN,
                2, (225, 10, 10), 3)

    # Display Image
    key = cv2.waitKey(1)
    cv2.imshow("Virtual Coffee Vending Machine", img)

    if key == ord('c'):
        myChoice = ''



