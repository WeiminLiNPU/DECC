import matplotlib.pyplot as plt
import pickle
from scipy.interpolate import interp1d, griddata
import numpy as np
from scipy import misc, ndimage
import dicom
import os

L = dicom.read_file('DECC_DATA/16/IL.dcm')
IL = np.log(np.array(L.pixel_array, dtype='float32'))
H = dicom.read_file('DECC_DATA/16/IH.dcm')
IH = np.log(np.array(H.pixel_array, dtype='float32'))

with open('fited-point.pkl', 'r') as f:
    pts = pickle.load(f)

labels = ['{0}'.format(i) for i in range(196)]

# for label,x,y in zip(labels,pts[:,1],pts[:,0]):
#     plt.annotate(label,xy=(x,y))
plt.plot(pts[:, 1], pts[:, 0], 'r.')

mid_points = np.zeros((14, 7, 2))
mid_point = np.zeros((7, 2))
for i in range(14):
    base = i * 14
    index = [0, 2, 3, 4, 5, 6, 1]
    for j in range(7):
        mid_point[j, 0] = (pts[base + index[j], 0] + pts[base + index[j] + 7, 0]) / 2
        mid_point[j, 1] = (pts[base + index[j], 1] + pts[base + index[j] + 7, 1]) / 2
    mid_points[i] = mid_point

# interpolation & extract rib fields
f = []
radius = 50
for i in range(14):

    f_ = interp1d(mid_points[i, :, 1], mid_points[i, :, 0], kind='cubic')
    f.append(f_)
    st = int(np.ceil(mid_points[i, 0, 1]))
    en = int(np.ceil(mid_points[i, 6, 1]))

    print st, en
    if i >= 7:
        st, en = en, st
    r_img = np.zeros([1 + radius * 2, en - st], dtype='float32')
    for k in range(st, en):
        c = int(f_(k))
        r_img[:, k - st] = IL[c - radius:c + radius + 1, k]

    # G_r_img_x, G_r_img_y = np.gradient(r_img)
    # G_r_img = (100*G_r_img_x)**2 + (100*G_r_img_y)**2
    # plt.imshow(r_img, cmap='gray', vmin=r_img.min(), vmax=r_img.max())
    # plt.imshow(G_r_img, cmap='gray', vmin=0, vmax=45)
    # plt.show()

    # interpolate the rib region
    r = r_img.shape[0]; c = r_img.shape[1]
    y = np.array(range(0, r) + [0]*c + range(0, r) + [r-1]*c)
    x = np.array([0]*r + range(0, c) + [c-1]*r + range(0, c))
    points = np.zeros([y.shape[0], 2])  # construct point = [x_vec, y_vec]
    points[:, 0] = x
    points[:, 1] = y

    z = np.array(np.ndarray.tolist(r_img[:, 0]) + np.ndarray.tolist(r_img[0, :]) + np.ndarray.tolist(r_img[:, c-1]) + np.ndarray.tolist(r_img[r-1, :]))
    values = np.zeros([z.shape[0], 1])   # construct values = [z_vec]
    values[:, 0] = z

    y_new = np.arange(0, r, 1)
    x_new = np.arange(0, c, 1)
    xx_new, yy_new = np.meshgrid(x_new, y_new)
    zz_new = griddata(points, values, (xx_new, yy_new), method='cubic')

    r_img_interp = zz_new[:, :, 0]

    plt.figure(1)
    plt.imshow(r_img, cmap='gray', vmin=r_img.min(), vmax=r_img.max())
    plt.figure(2)
    plt.imshow(r_img_interp, cmap='gray', vmin=r_img.min(), vmax=r_img.max())
    plt.show()

    a = 1


