import cv2
import glob
import numpy as np

def vwHist(img):
    name = img.split('.')[0]
    img = cv2.imread(img, 0)
    img = img.astype(np.uint8)
    
    orb = cv2.ORB()
    kp, des = orb.detectAndCompute(img, None)
    
    hist = [0.0] * 90
    for k in kp:
        hist[int(k.angle/4.0)] += float(k.response)
        #print(hist[int(k.angle)])

    op = open(name+".txt", 'w')
    for x in hist:
        op.write('%f ' % x)
        op.write('\n')
    op.close()
    return hist

for f in glob.glob("*.pgm"):
    print(f)
    vwHist(f)

'''def storeDes(img):
    name = img.split('.')[0]
    img = cv2.imread(img, 0)
    img = img.astype(np.uint8)
    
    orb = cv2.ORB()
    kp, des = orb.detectAndCompute(img, None)

    op = open(name+".txt", 'w')
    hist = [0.0] * 180
    if des is None:
        return
    for dd in des:
        #print(dd)
        for d in dd:
            op.write('%i ' % d)
    
for f in glob.glob("*.pgm"):
    print(f)
    storeDes(f)'''
