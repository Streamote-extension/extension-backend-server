import numpy as np
import cv2
from keras.preprocessing import image
from WebCam import WebcamVideoStream

#-----------------------------
#opencv initialization

detection_model_path = 'haarcascade_frontalface_default.xml'
emotion_model_path = 'facial_expression_model_weights.h5'

vs = WebcamVideoStream(src=0).start()
#-----------------------------
#face expression recognizer initialization
from keras.models import model_from_json
model = model_from_json(open("facial_expression_model_structure.json", "r").read())
model.load_weights('facial_expression_model_weights.h5') #loading preprepped weights

#-----------------------------

streamotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')

while(True):
	ret, img = vs.read()
	
	grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	face = stream_Cascade.detectMultiScale(grey, 1.3, 5)

	#print(face) displays the location of faces

	
	for (x,y,w,h) in face:
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2) #rectangle box for the "image"
		
		detected_face = img[int(y):int(y+h), int(x):int(x+w)] #crop detected face from "image"
		detected_face = cv2.cvtColor(detected_face, cv2.COLOR_BGR2GRAY) #transform to gray scale
		detected_face = cv2.resize(detected_face, (48, 48)) #resize to 48x48
		
		img_pixels = image.img_to_array(detected_face) #grabs pixels
		img_pixels = np.expand_dims(img_pixels, axis = 0) 
		
		img_pixels /= 255 #pixels are in scale of [0, 255]. normalize all pixels in scale of [0, 1]
		
		predictions = model.predict(img_pixels) #store probabilities of 7 expressions
		
		#find max indexed array 0: angry, 1:disgust, 2:fear, 3:happy, 4:sad, 5:surprise, 6:neutral
		max_index = np.argmax(predictions[0])
		
		emotion = streamotions[max_index]
		
		#write emotion text above rectangle
		cv2.putText(img, emotion, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
		
		#process on detected face end
		#-------------------------

	cv2.imshow('img',img)

	if cv2.waitKey(1) & 0xFF == ord('q'): #press q to exit progream
		break

#kill open cv things		
vs.release()
cv2.destroyAllWindows()