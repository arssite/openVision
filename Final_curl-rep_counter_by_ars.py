#without tracking curl-rep counter by ars
import cv2
import mediapipe as mp
import numpy as np

#calculate angles
def calculateangle(a,b,c):
    a=np.array(a)
    b=np.array(b)
    c=np.array(c)
    radians=np.arctan2(c[1]-b[1],c[0]-b[0])-np.arctan2(a[1]-b[1],a[0]-b[0])
    angle=np.abs(radians*180.0/np.pi)

    if angle>180.0:#change angle value by your resolution
        angle=360-angle
    return angle

#curl and reps counter
reps=0 #for left
state=None
reps1=0 #for right
state1=None

#to draw
mpd=mp.solutions.drawing_utils
mpp=mp.solutions.pose
#for camera
cap=cv2.VideoCapture(0)#change value depend on your system camera if external use 1
with mpp.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    ret,frame=cap.read()
    #recolor image
    image=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    image.flags.writeable=False
    #make detections
    r=pose.process(image)

    image.flags.writeable=True
    image=cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
    print(r)
    
    
    try:
      landmarks=r.pose_landmarks.landmark
       #coordinates
      shoulder=[landmarks[mpp.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mpp.PoseLandmark.LEFT_SHOULDER.value].y]
      elbow=[landmarks[mpp.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mpp.PoseLandmark.LEFT_ELBOW.value].y]
      wrist=[landmarks[mpp.PoseLandmark.LEFT_WRIST.value].x,landmarks[mpp.PoseLandmark.LEFT_WRIST.value].y]
      angle=calculateangle(shoulder,elbow,wrist)
      shoulder1=[landmarks[mpp.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mpp.PoseLandmark.RIGHT_SHOULDER.value].y]
      elbow1=[landmarks[mpp.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mpp.PoseLandmark.RIGHT_ELBOW.value].y]
      wrist1=[landmarks[mpp.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mpp.PoseLandmark.RIGHT_WRIST.value].y]
      angle1=calculateangle(shoulder1,elbow1,wrist1)
  
     
    #angle logic for right nd left
      if angle>140:
        state="down"
      if angle<40 and state=="down":
        state="up"
        reps=reps+1
        print(reps)
      if angle1>140:
        state1="down"
      if angle1<40 and state1=="down":
        state1="up"
        reps1=reps1+1
        print(reps1)
    
    except:
      pass

    #displaydata
    # cv2.putText(image, text, org, font, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])
    
    cv2.putText(image,'Right',(20,90),
                  cv2.FONT_HERSHEY_PLAIN , 3, (254,120,69) , 2 , cv2.LINE_AA)
    cv2.putText(image,str(reps1),(30,155),
                  cv2.FONT_HERSHEY_PLAIN , 5, (254,120,69) , 5 , cv2.LINE_AA)
    cv2.putText(image,'Left',(490,90),#aage,height
                  cv2.FONT_HERSHEY_PLAIN , 3, (254,120,69) , 2 , cv2.LINE_AA)
    cv2.putText(image,str(reps),(500,155),
                  cv2.FONT_HERSHEY_PLAIN , 5, (254,120,69) , 5 , cv2.LINE_AA)
    cv2.putText(image,state1,(25,200),
                  cv2.FONT_HERSHEY_SIMPLEX , 1, (255,255,255) , 1 , cv2.LINE_AA)
    cv2.putText(image,state,(495,200),
                  cv2.FONT_HERSHEY_SIMPLEX , 1, (255,255,255) , 1 , cv2.LINE_AA)
  
   #promotion 
    cv2.putText(image,'curl or reps counter by ARS',(220,450),
                  cv2.FONT_HERSHEY_SIMPLEX , 0.5, (0,0,0) , 1 , cv2.LINE_AA)
    #message to stop
    cv2.putText(image,'press <q> to quit',(5,12),
                  cv2.FONT_HERSHEY_SIMPLEX , 0.5, (0,0,0) , 1 , cv2.LINE_AA)

    cv2.imshow("curl-reps counter by ARS",image)
    if cv2.waitKey(10) & 0xff==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
