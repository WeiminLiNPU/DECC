import os
import nibabel as nib
import numpy as np
from scipy.ndimage.filters import gaussian_filter
import dicom
import matplotlib.pyplot as plt


def convert2NII_save(filename_dcm):
    # convert img to NII
    # save in current folder
    H = dicom.read_file(filename_dcm)
    data = np.array(H.pixel_array)
    # data = np.flip(np.rot90(data), axis=0)
    new_image = nib.Nifti1Image(data, affine=None)

    print ('saving ' + filename_dcm + ' as ' + os.path.splitext(filename_dcm)[0] + '.nii')
    nib.save(new_image, os.path.splitext(filename_dcm)[0] + '.nii')


def BSplineReg_save(filename_img_ref, filename_img_flo, filename_img_res):
    # input to PC for NIFTY registration
    # save in "filename_img_res" directory
    print ('ref=' + filename_img_ref + ' flo=' + filename_img_flo + ' --> Begin BSpline registration')
    reg_command = 'reg_f3d' + ' -ref ' + filename_img_ref + ' -flo ' + filename_img_flo + ' -res ' + filename_img_res \
                  + ' -sx ' + '1' + ' -sy ' + '1' + ' -sz ' + '1'
    os.system(reg_command)


############### main ##################
# convert to NII
filename_dcm_L = 'DECC_DATA/08/IL.dcm'
filename_dcm_H = 'DECC_DATA/08/IH.dcm'
convert2NII_save(filename_dcm_L)
convert2NII_save(filename_dcm_H)

# H and L image registration
filename_img_ref = os.path.splitext(filename_dcm_L)[0] + '.nii'
filename_img_flo = os.path.splitext(filename_dcm_H)[0] + '.nii'
filename_img_res = os.path.splitext(filename_dcm_H)[0] + '_res.nii'
# BSplineReg_save(filename_img_ref, filename_img_flo, filename_img_res)

# generate dual energy image from IL + IH   or    IL + IH_reg
IL_source = nib.load(filename_img_ref)
IL = IL_source.get_data()

IH_source = nib.load(filename_img_flo)
IH = IH_source.get_data()

IH_reg_source = nib.load(filename_img_res)
IH_reg = IH_reg_source.get_data()

fs = 0.1
beta = [0, 0, 0.686564, 0.794393, -0.122075, 0.252449, -0.154831, 9.986063]
# IB = 1000 * np.exp(0.73 * np.log(IL) - gaussian_filter(np.log(IH), fs))
# IB_reg = 1000 * np.exp(0.73 * np.log(IL) - gaussian_filter(np.log(IH_reg), fs))

IB = np.exp(beta[2]*np.log(IL) - beta[3]*np.log(IH) + beta[4]*(np.log(IL)**2) + beta[5]*(np.log(IL)*np.log(IH)) + beta[6]*(np.log(IH)**2) + beta[7])
IB_reg = np.exp(beta[2]*np.log(IL) - beta[3]*np.log(IH_reg) + beta[4]*(np.log(IL)**2) + beta[5]*(np.log(IL)*np.log(IH_reg)) + beta[6]*(np.log(IH_reg)**2) + beta[7])

plt.figure(1)
plt.imshow(IB, cmap='gray', vmin=IB.min() - 200, vmax=IB.max() - 1600)

plt.figure(2)
plt.imshow(IB_reg, cmap='gray', vmin=IB.min() - 200, vmax=IB.max() - 1600)

plt.show()
