import numpy as np
import cv2
from matplotlib import pyplot as plt

def myMatch(img1, img2):

    img1 = cv2.imread(img1,0)          # queryImage
    img2 = cv2.imread(img2,0) # trainImage
    
    # Initiate SIFT detector
    orb = cv2.ORB()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = orb.detectAndCompute(img1,None)
    kp2, des2 = orb.detectAndCompute(img2,None)

    # create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match descriptors.
    matches = bf.match(des1,des2)

    # Sort them in the order of their distance.
    matches = sorted(matches, key = lambda x:x.distance)
    d = 0
    for i in range(15):
        d += matches[i].distance
    return -d/15.0
        

    '''for i in range(len(matches)):
        if matches[i].distance > 65:
            return i
            #return ((len(matches) - i) / float(len(matches)) * 100)
    return len(matches)'''



def myMatch2(img1, img2):
    MIN_MATCH_COUNT = 10

    img1 = cv2.imread(img1,0)          # queryImage
    img2 = cv2.imread(img2,0) # trainImage


    # Initiate SIFT detector
    sift = cv2.SIFT()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1,des2,k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)
            
    return len(good)
