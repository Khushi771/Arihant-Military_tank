import cv2 as cv
import numpy as np

cap=cv.VideoCapture(0)

cap.set(cv.CAP_PROP_FRAME_WIDTH, 720)       
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

KNOWN_DISTANCE = 76.2  # centimeter
KNOWN_WIDTH = 14.3  # centimeter

x=[]
y=[]
rad=[]
dist=[]

X=0
Y=0
Z=0
t=0


while True:

    _,img=cap.read()

    gray=cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    b,g,r=cv.split(img)
    gray = cv.subtract(r, gray)

    gray=cv.medianBlur(gray,5)

    rows=gray.shape[0]

    circles=cv.HoughCircles(gray,cv.HOUGH_GRADIENT,1,rows/8,param1=100,param2=20,minRadius=10,maxRadius=250)


    if circles is not None:
        circles=np.uint16(np.around(circles))
        for i in circles[0,:]:
            center=(i[0],i[1])
            x.append(center[0]*(0.0265))
            y.append(center[1]*(0.0265))
            cv.circle(gray,center,1,(255,255,0),3)
            radius=i[2]
            rad.append(radius*(0.0265))
            cv.circle(gray,center,radius,(255,255,0),3)           
            area = 3.142 * (rad[t]**2)
            t=t+1
            distance = 124 * (area)**(-0.502)
            dist.append(distance)
           
            if t==10:
                for i in range(10):
                    X+=x[i]
                    Y+=y[i]
                    Z+=dist[i]
                X=X/10
                Y=Y/10
                Z=Z/10
                print(X,", ",Y,", ",Z)
                x.clear()
                y.clear()
                rad.clear()
                dist.clear()
                t=0
                break


    cv.imwrite("save.jpg",gray)
    sv=cv.imread("save.jpg")
    cv.imshow("save",sv)

    
    if cv.waitKey(1500) & 0xFF==ord('q'):
        cap.release()
        cv.destroyAllWindows()
        break

