import cv2
 
width = 1280
height = 720

cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

paddleWidth = int(width / 10)
paddleHeight = int(paddleWidth / 5)
paddleColor = (0, 0, 255)


class mpHands:
    import mediapipe as mp
    def __init__(self,maxHands=2,tol1=.5,tol2=.5):
        self.hands=self.mp.solutions.hands.Hands(False,maxHands,tol1,tol2)

    def Marks(self,frame):
        myHands=[]

        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

        results=self.hands.process(frameRGB)

        if results.multi_hand_landmarks != None:
            for handLandMarks in results.multi_hand_landmarks:
                myHand=[]

                for landMark in handLandMarks.landmark:
                    myHand.append((int(landMark.x*width),int(landMark.y*height)))

                myHands.append(myHand)

        return myHands

findHands = mpHands(2)
lives = 3

xPos = int(width/2)
yPos = int(height/2)
radius = 20
circleColor = (255, 0, 0)

deltaX = 4
deltaY = 6

xSpeedIncrement = 2
ySpeedIncrement = 2

xPosHand = 0


while True:
    ignore,  frame = cam.read()

    handData = findHands.Marks(frame)
    
    for hand in handData:
        cv2.rectangle(frame, (int(hand[8][0] - paddleWidth/2), 10), (int(hand[8][0] + paddleWidth/2), 10 + paddleHeight), paddleColor, -1)
        xPosHand = hand[8][0]

    if xPos + radius >= width or xPos - radius <= 0:
        deltaX = -deltaX
    
    if yPos + radius >= height:
        deltaY = -deltaY
    
    if yPos - radius <= 0:
        xPos = int(width/2)
        yPos = int(height/2)

        lives -= 1
      
    cv2.putText(frame, "Lives: " + str(lives), (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    if yPos - radius <= 10 + paddleHeight:
        if xPos >= int(xPosHand - paddleWidth/2) and xPos <= int(xPosHand + paddleWidth/2):
            deltaY = -deltaY
            if deltaX < 0:
                deltaX -= xSpeedIncrement
            else:
                deltaX += xSpeedIncrement
            if deltaY < 0:
                deltaY -= ySpeedIncrement
            else:
                deltaY += ySpeedIncrement

    if lives <= 0:
        break

    xPos += deltaX
    yPos += deltaY

    cv2.circle(frame, (xPos, yPos), radius, circleColor, -1)

    cv2.imshow('my WEBcam', frame)

    cv2.moveWindow('my WEBcam',0,0)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
