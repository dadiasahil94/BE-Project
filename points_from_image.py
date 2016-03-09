import cv2
import numpy as np
import helper_functions as hf
import matplotlib.pyplot as plt

""" Prints R	G    B  values of a selectedbox

    Useage :  python my_ginput.py >> outputfile.txt

"""



def GINPUT(image):
    '''INPUT:
       image =  where points are supposed to be selected

       OUTPUT:
       image image with modified values
    '''
    # image  = cv2.resize(image,(640,480))
    plt.figure(1)
    plt.imshow(image)
    plt.axis("off")
    plt.title("Select a rectangel OR press scrool button to exit", fontsize=20)
    pts = np.array(plt.ginput(n=2, timeout = 10))
    # print ("in")
    if(len(pts)!=0):
        c = int(pts[0][0])
        r = int(pts[0][1])
        c1 = int(pts[1][0])
        r1 = int(pts[1][1])
        cropped_image = image[r:r1,c:c1]
        # cv2.rectangle(image,(c,r),(c1,r1) , (0,0,200))
        return cropped_image , image, True
    else:
        return image , image, False

start = "./aerialroad/"
number = 1
end = ".jpg"
start1 = "./"
number1 = 1
end1 = "cropped.jpg"

vid = cv2.VideoCapture("./vid1.mp4")
ret , frame  = vid.read()
skip=1100
for i in range(0,skip):
	ret, frame = vid.read()
#skip_frames(skip)
while(frame!=None):

    status =  True
    frame = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)
    while(status):
 #       cv2.imshow("frame input" , frame)
#        out_name = str(start1+str(number1)+end1)
        cropped , image, status = GINPUT(frame)
        # print "out"
        # print cropped.shape
	if status ==True:
    #    image1 = cropped.reshape((cropped.shape[0]*cropped.shape[1],3))
     #   length = (image1.shape[0]*image1.shape[1])
		rows,cols ,colors = cropped.shape
		for row in range(rows):
			for col in range(cols):
				# print R, G, B values
				print(str(cropped[row][col][0]) +"\t"+ str(cropped[row][col][1]) + "\t" +str(cropped[row][col][2]))


        # if(status==True):
        #     cv2.imwrite(out_name, cropped)
        #     number1+=1
    # number+=1
    for i in range(25):
        ret , frame  = vid.read()
#    cv2.waitKey(0)
