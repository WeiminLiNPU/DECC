import cv2
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from scipy import interpolate


# Function: suppress the intensity of bones given a single bone images

def global_adjustment(img_supp, img_orig):
    diff = img_orig - img_supp

    r = diff.shape[0]; c = diff.shape[1]
    ## four sides
    y = np.array(range(0, r) + [0]*c + range(0, r) + [r-1]*c)
    x = np.array([0]*r + range(0, c) + [c-1]*r + range(0, c))
    points = np.zeros([y.shape[0], 2])  # construct point = [x_vec, y_vec]
    points[:, 0] = x
    points[:, 1] = y

    z = np.array(np.ndarray.tolist(diff[:, 0]) + np.ndarray.tolist(diff[0, :]) + np.ndarray.tolist(diff[:, c-1]) + np.ndarray.tolist(diff[r-1, :]))
    values = np.zeros([z.shape[0], 1])   # construct values = [z_vec]
    values[:, 0] = z

    ## two sides
    # y = np.array([0]*c + [r-1]*c)
    # x = np.array(range(0, c) + range(0, c))
    # points = np.zeros([y.shape[0], 2])  # construct point = [x_vec, y_vec]
    # points[:, 0] = x
    # points[:, 1] = y
    #
    # z = np.array(np.ndarray.tolist(diff[0, :]) + np.ndarray.tolist(diff[r-1, :]))
    # values = np.zeros([z.shape[0], 1])   # construct values = [z_vec]
    # values[:, 0] = z


    y_new = np.arange(0, r, 1)
    x_new = np.arange(0, c, 1)
    xx_new, yy_new = np.meshgrid(x_new, y_new)
    zz_new = griddata(points, values, (xx_new, yy_new), method='cubic')

    img_supp_adj = img_supp + zz_new[:, :, 0]
    return img_supp_adj


def cancelation(img):
    img = img.astype(int)

    # compute high frequency HF
    kernel = np.ones((1, 60), np.float32) / 60.0
    LF = cv2.filter2D(img, -1, kernel)
    HF = img - LF

    # compute regional low frequency
    kernel = np.ones((60, 60), np.float32) / (80*80)
    region_imap = cv2.filter2D(img, -1, kernel)

    res = HF + region_imap

    # plt.figure(1)
    # plt.imshow(LF, cmap='gray')
    # plt.figure(2)
    # plt.imshow(HF, cmap='gray')
    # plt.figure(3)
    # plt.imshow(region_imap, cmap='gray')
    # plt.figure(4)
    # plt.imshow(res, cmap='gray')
    # plt.figure(5)
    # plt.imshow(img, cmap='gray')
    # plt.show()

    # fit the result back to the original image smoothly
    res_adj = global_adjustment(res, img)

    return res_adj.astype(np.float32)


if __name__ == "__main__":
    img = cv2.imread('result/8.png', 0)

    img = cancelation(img)
    img = np.maximum(img, 0)

    cv2.imshow('test', img)
    cv2.waitKey(0)
