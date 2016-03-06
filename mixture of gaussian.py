import sys
import cv2
import numpy as np
from sklearn import mixture
import helper_functions as hf
import re


def PRINT_PARAMETERS(g, no_sources, Feature_matrix):
    print "no of sources for road  : ", no_sources
    print "AIC : ", g.aic(Feature_matrix), "BIC : ", g.bic(Feature_matrix)
    print "means"
    print g.means_
    print "weights"
    print g.weights_
    print "covars matrix"
    print g.covars_
    print


def SKIP_FRAMES(video_obj, n_frames):
    for i in range(n_frames):
        ret, frame = video_obj.read()


def main():

    # get feature matrix
    file_name = (sys.argv[1])
    Feature_matrix = hf.FEATURE_MATRIX_FROM_FILE(file_name)

    # initialise video file and skip a couple of frames
    video_name = sys.argv[2]
    vid = cv2.VideoCapture(video_name)
    for i in range(1500):
        ret, frame = vid.read()

    # output video
    fourcc = cv2.cv.FOURCC(*'XVID')
    out = cv2.VideoWriter('/home/sahil/Desktop/test.avi',
                          fourcc, 30, (640, 480))

    # create GMM
    no_sources = 8
    while no_sources <= 10:

        print "-------------------------------------------------------------------------------------"
        # random colors
        colors = np.arange(0, 255, int(255 / no_sources))
        colors1 = np.array([[0, 0, 0], [0, 221, 255], [0, 255, 0], [0, 0, 255], [255, 255, 255], [147, 20, 255], [255, 0, 0], [212,255,127],[0,165,255]  ])


        # initialise mixtures
        g = mixture.GMM(n_components=no_sources, covariance_type='tied')
        g.fit(Feature_matrix)
        PRINT_PARAMETERS(g, no_sources, Feature_matrix)

        print "black    yellow      greeen      red     white       pink        blue        aqua        orange"
        print colors1


        # run for each frame
        ret, frame = vid.read()
        while (frame != None):

            # prepreocessing
            frame = hf.RESIZE_IMAGE(frame, 0.5, 0.5)
            # frame = cv2.GaussianBlur(frame, (5, 5), 0, 0)
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rows, cols, _ = frame.shape
            draw_frame = frame.copy()
            test_image = np.reshape(
                frame, (frame.shape[0] * frame.shape[1], 3))

            # do prediction here
            image_classed = hf.TRANSPOSE_1DMATRIX(g.predict(test_image))
            image_classed = np.reshape(image_classed, (rows, cols))

            # map the colors
            np.unique(image_classed)
            for row in range(rows):
                for col in range(cols):
                    draw_frame[row][col] = colors1[image_classed[row][col]]
                    # image_classed[row][col] = colors[image_classed[row][col]]
            # image_classed_disp = (image_classed*1.0/255) #--- for display
            # purpose

            cv2.imshow("classed color", draw_frame)
            cv2.imshow("original", frame)
            cv2.waitKey(20)
            ret, frame = vid.read()

            for i in range(15):
                ret, frame = vid.read()

        # update the gaussian numbers
        vid = cv2.VideoCapture(video_name)
        no_sources += 1


if __name__ == '__main__':
    main()
