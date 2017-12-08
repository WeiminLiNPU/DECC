import matplotlib.pyplot as plt
import pickle
from scipy.interpolate import interp1d
import numpy as np
import pylab
import cancelation as cc
import dicom

def rib_suppress(img,pts):

    labels = ['{0}'.format(i) for i in range(196)]


    # for label,x,y in zip(labels,pts[:,1],pts[:,0]):
    #     plt.annotate(label,xy=(x,y))
    plt.plot(pts[:,1],pts[:,0],'r.')

    mid_points = np.zeros((14, 7, 2))
    mid_point = np.zeros((7, 2))
    for i in range(14):
        base = i * 14
        index=[0,2,3,4,5,6,1]
        for j in range(7):
            mid_point[j, 0] = (pts[base + index[j], 0] + pts[base + index[j] + 7, 0]) / 2
            mid_point[j, 1] = (pts[base + index[j], 1] + pts[base + index[j] + 7, 1]) / 2
        mid_points[i] = mid_point

    #interpolation & extract rib fields
    f=[]
    radius=50
    for i in range(14):

        f_=interp1d(mid_points[i,:, 1], mid_points[i,:, 0], kind='linear')
        f.append(f_)
        st=int(np.ceil(mid_points[i, 0, 1]))
        en=int(np.ceil(mid_points[i, 6, 1]))

        if i>=7 :
            st,en=en,st
        r_img = np.zeros([1 + radius * 2, en - st + 1], dtype=np.uint8)
        for k in range(st,en):
            c=f_(k)
            r_img[:,k-st]=img[c-radius:c+radius+1,k]
        r_cancelled=cc.cancelation(r_img)
        for k in range(st, en):
            c = f_(k)
            img[c - radius:c + radius + 1, k]=r_cancelled[:, k - st]
        #misc.imsave(os.path.join('./result/',str(i)+'.png'),r_img)
        return img

if __name__ == "__main__":
    img = dicom.read_file('test/IL10.dcm').pixel_array

    with open('fited-point.pkl', 'r') as f:
        pts = pickle.load(f)
    r_img=rib_suppress(img,pts)
    pylab.imshow(img,cmap=pylab.cm.bone)
    pylab.show()





