import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
scores = [0, 0]  # Robot, Player
imgAI = None     # ✅ FIX 1

while True:
    imgBG = cv2.imread("Resources/BG.png")
    success, img = cap.read()

    if not success:
        print("Camera not detected")
        break

    imgScaled = cv2.resize(img, (0, 0), None, 0.993, 1.016)
    imgScaled = imgScaled[:, 53:473]

    # Find Hands safely ✅ FIX 2
    hands, img = detector.findHands(imgScaled, draw=True)

    if startGame:
        if not stateResult:
            timer = time.time() - initialTime
            cv2.putText(
                imgBG, str(int(timer)), (605, 435),
                cv2.FONT_HERSHEY_PLAIN, 6, (75, 33, 15), 9
            )

            if timer > 3:
                stateResult = True
                timer = 0

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)

                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1   # Rock
                    elif fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2   # Paper
                    elif fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3   # Scissors

                    if playerMove:
                        randomNumber = random.randint(1, 3)
                        imgAI = cv2.imread(
                            f'Resources/{randomNumber}.png',
                            cv2.IMREAD_UNCHANGED
                        )
                        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

                        # Player wins
                        if (playerMove == 1 and randomNumber == 3) or \
                           (playerMove == 2 and randomNumber == 1) or \
                           (playerMove == 3 and randomNumber == 2):
                            scores[1] += 1

                        # AI wins
                        elif (playerMove == 3 and randomNumber == 1) or \
                             (playerMove == 1 and randomNumber == 2) or \
                             (playerMove == 2 and randomNumber == 3):
                            scores[0] += 1

    imgBG[207:695, 800:1220] = imgScaled

    # ✅ FIX 3
    if stateResult and imgAI is not None:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

    cv2.putText(imgBG, str(scores[0]), (369, 190),
                cv2.FONT_HERSHEY_PLAIN, 4, (75, 33, 15), 6)
    cv2.putText(imgBG, str(scores[1]), (1115, 190),
                cv2.FONT_HERSHEY_PLAIN, 4, (75, 33, 15), 6)

    cv2.imshow("BG", imgBG)

    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False
        imgAI = None

    elif key == ord('q'):   # ✅ EXIT KEY
        break

cap.release()
cv2.destroyAllWindows()
