import cv2


cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)   # Create a video capture object which is helpful to capture videos to webcam
cam.set(3, 640)  # Set video FrameWidth
cam.set(4, 480)  # Set video FrameHeight


detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')   # Haar cascade clasifier is an effective object detection apporach

face_id = input("Enter a numeric user Id here:  ")   # Use integer id for every new face (0,1,2,3,4,5,6,7,8,9......)

print("Taking samples, look at camera......")
count = 0   # Initializing sampling page count


while True:

    ret, img = cam.read()  # Read the frame using the above created object
    converted_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # The functions converts an input image from one color space to another
    faces = detector.detectMultiScale(converted_image, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)  # Use to draw a rectangle on any image
        count += 1

        cv2.imwrite("Samples/faces." + str(face_id) + '.' + str(count) + ".jpg", converted_image[y:y+h,x:x+w])  # To capture & save images into the datasets folder

        cv2.imshow('image', img)  # Used to display an image in a window

    k = cv2.waitKey(100) & 0xff   # Wait for a pressed key
    if k == 27:   # Press 'ESC' to stop
        break
    elif count >= 10:    # Take 50 samples (More sample --> More accuracy)
        break


print("Sample taken now closing the program...")
cam.release()
cv2.destroyAllWindows()