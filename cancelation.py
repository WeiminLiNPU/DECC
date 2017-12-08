import cv2
import numpy as np
from scipy import interpolate

# Function: suppress the intensity of bones given a single bone images

def cancelation(img):

    img=img.astype(int)

    # compute high frequency HF
    kernel = np.ones((1,60),np.float32)/60.0
    LF = cv2.filter2D(img,-1,kernel)
    HF = img-LF

    #compute regional low frequency
    kernel = np.ones((60,60),np.float32)/3600
    region_imap= cv2.filter2D(img, -1, kernel)

    res=HF+region_imap

    # fit the result back to the original image smoothly
    diff=img-res
    [h,w]=img.shape
    p1=np.vstack((np.arange(0,w), np.zeros(w)))
    p2=np.vstack((np.arange(0,w), (h-1)*np.ones(w)))
    p=np.concatenate((p1.transpose(), p2.transpose()), axis=0)
    # value=np.concatenate((diff[0][1:w],diff[h-1][1:w]),axis=0)
    x, y=np.mgrid[0:w,0:h]

    interp=interpolate.griddata(p, np.hstack((diff[0][0:w],diff[h-1][0:w])).transpose(), (x,y),method='linear')
    # cv2.imshow('t',interp)
    # cv2.waitKey(0)
    res=res+interp.transpose()

    # underflow correction
    res=np.maximum(res,0)

    return res.astype(np.uint8)

if __name__=="__main__":
    img=cv2.imread('result/8.png',0)

    img=cancelation(img)
    img=np.maximum(img,0)

    cv2.imshow('test',img)
    cv2.waitKey(0)