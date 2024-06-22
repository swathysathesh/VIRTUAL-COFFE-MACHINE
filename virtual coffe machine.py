#>>>>importing libraries
import cv2
import os                          #for define file path
import HandTrackingModule as htm   #for detecting hands

#>>>>setting the webcam
cap=cv2.VideoCapture(0)
cap.set(3,640) #(propid,width)
cap.set(4,480) #(propid,height)

#>>>>print background image
img_background=cv2.imread('/home/swathy/Downloads/python/opencv/project/Resources/Background.png')

#>>>>import all modes as a list
folder_pathmodes='/home/swathy/Downloads/python/opencv/project/Resources/Modes'
lst_image_modespath=os.listdir(folder_pathmodes)
lst_image_modespath=sorted(lst_image_modespath)  #1 png,2 png,3 png,4 png
lst_image_modes=[]
for i in lst_image_modespath:
    lst_image_modes.append(cv2.imread(os.path.join(folder_pathmodes,i)))
print(lst_image_modes)

#>>>>importing all icons as a list
folder_pathicons='/home/swathy/Downloads/python/opencv/project/Resources/Icons'
lst_image_iconpath=os.listdir(folder_pathicons)
lst_image_iconpath=sorted(lst_image_iconpath)
lst_image_icon=[]
for i in lst_image_iconpath:
    lst_image_icon.append(cv2.imread(os.path.join(folder_pathicons,i)))
print(lst_image_icon)

#>>>> For changing selection mode
mode_type=0   

selection=-1
counter=0
selectiospeed=10
modepositions=[(1135,196),(1002,382),(1137,597)]
counterpause=0
selectionlst=[-1,-1,-1]
detector =htm.handDetector()

while True:
    success,img=cap.read()

#>>>>overlaying the webcam feed on the background image
                #[height:lower part of height+image height,width]
    img_background[139:139+480,50:50+640]=img 

#>>>>overlaying the modes on the background image
                #[starting point:height,width]
    img_background[0:720,847:1280]=lst_image_modes[mode_type]

#>>>>find hand and its landmark
    find_hands=detector.findHands(img)
    lm_list=detector.findPosition(img)
    #print(lm_list)
    
#>>>>check finger is up
    if len(lm_list)!=0 and counterpause==0 and mode_type<3:
        fingers=detector.fingersUp()
        print(fingers)

        #index finger is up
        if fingers==[0,1,0,0,0]:
            if selection!=1:
                counter=1
            selection=1
        #index & middle
        elif fingers==[0,1,1,0,0]:
            if selection!=2:
                counter=1
            selection=2
        #index, middle & ring finger
        elif fingers==[0,1,1,1,0]:
            if selection!=3:
                counter=1
            selection=3
        

        else:
            selection=-1
            counter=0
        if counter>0:
            counter+=1
            print(counter)

            #draw ellipse 
            cv2.ellipse(img_background,modepositions[selection-1],(103,103),0,0,counter*selectiospeed,(0,255,0),20)
            if counter*selectiospeed>360:
                selectionlst[mode_type]=selection
                mode_type+=1
                counter=0
                selection=-1
                counterpause=1
    #to pause after each selection made          
    if counterpause>0:
        counterpause+=1
        if counterpause>60:
            counterpause=0
    #add selection icon  at the bottom
    if selectionlst[0]!=-1:
        img_background[636:636+65,133:133+65]=lst_image_icon[selectionlst[0]-1]
    if selectionlst[1]!=-1:
        img_background[636:636+65,340:340+65]=lst_image_icon[2+selectionlst[1]]
    if selectionlst[2]!=-1:
        img_background[636:636+65,542:542+65]=lst_image_icon[5+selectionlst[2]]
    



#displaying
    #cv2.imshow("image",img)
    #cv2.imshow("background",img_background)
    
    cv2.namedWindow('background',cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow('background',1000,500)
    cv2.imshow('background',img_background)
    if cv2.waitKey(1) & 0xFF==27:
        break
cap.release()
cv2.destroyAllWindows()


