import cv2

vid = cv2.VideoCapture(0)
frame_width = 640
frame_height = 480
vid.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
   
size = (frame_width, frame_height)

#video write object
# fourcc= cv2.CV_FOURCC('m', 'p', '4', 'v')
fourcc= cv2.VideoWriter_fourcc('m','p','4','v')
result = cv2.VideoWriter('drone_vid.avi',fourcc, 10, size,0)

while 1:
	_,fr = vid.read()

	
	fr = cv2.cvtColor(fr,cv2.COLOR_BGR2GRAY)
	cv2.imshow('ff', fr)
	result.write(fr)

	k = cv2.waitKey(10)&0xff
	if k == 27:
		result.release()
		vid.release()
		cv2.destroyAllWindows()
		break