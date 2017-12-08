import matplotlib.pyplot as plt
import pickle
from scipy.interpolate import interp1d, griddata
import numpy as np
from scipy import misc, ndimage
import nibabel as nib
import dicom
import os
from rib_supp import rib_suppress
from rib_fitting import fit

def convert2NII_save(I, save_dir, file_name):
    # convert img to NII
    # save in current folder
    new_image = nib.Nifti1Image(I, affine=None)
    print ('saving to ' + save_dir + file_name)
    nib.save(new_image, save_dir + file_name)

def BSplineReg_save(filename_img_ref, filename_img_flo, filename_img_res):
    # input to PC for NIFTY registration
    # save in "filename_img_res" directory
    print ('ref=' + filename_img_ref + ' flo=' + filename_img_flo + ' --> Begin BSpline registration')
    reg_command = 'reg_f3d' + ' -ref ' + filename_img_ref + ' -flo ' + filename_img_flo + ' -res ' + filename_img_res \
                  + ' -sx ' + '1' + ' -sy ' + '1' + ' -sz ' + '1'
    os.system(reg_command)


## Specify Case Number
case_ind = '16'
data_dir = 'DECC_DATA/'

## Load DCM data and convert to NII
L_filename = data_dir + case_ind + '/IL.dcm'
L = dicom.read_file(L_filename)
IL = np.array(L.pixel_array, dtype='float32')
convert2NII_save(IL, data_dir + case_ind + '/', 'IL.nii')

H_filename = data_dir + case_ind + '/IH.dcm'
H = dicom.read_file(H_filename)
IH = np.array(H.pixel_array, dtype='float32')
convert2NII_save(IH, data_dir + case_ind + '/', 'IH.nii')

## Rib processing
# 1) Fit rib using AAM
path_to_train = './data'; path_to_test = './test/10.jpg'
center_x = 950; center_y = 1100; width = 1400;
pts = fit(path_to_train, path_to_test, center_x, center_y, width)

# 2) Suppress rib on IL & IH.
IL_supp = rib_suppress(IL, pts)
IH_supp = rib_suppress(IH, pts)

# 3) Save the suppressed data to NII.
# plt.figure(1)
# plt.imshow(IH_supp, cmap='gray')
# plt.figure(2)
# plt.imshow(IL_supp, cmap='gray')
# plt.figure(3)
# plt.imshow(IH, cmap='gray')
# plt.figure(4)
# plt.imshow(IL, cmap='gray')
# plt.show()

convert2NII_save(IL_supp, data_dir + case_ind + '/', 'IL_supp.nii')
convert2NII_save(IH_supp, data_dir + case_ind + '/', 'IH_supp.nii')

## Apply BSpline image registration
# 1) with rib suppression.
filename_img_ref = data_dir + case_ind + '/', 'IL_supp.nii'
filename_img_flo = data_dir + case_ind + '/', 'IH_supp.nii'
filename_img_res = data_dir + case_ind + '/', 'IH_supp_reg.nii'
BSplineReg_save(filename_img_ref, filename_img_flo, filename_img_res)

# 2) without rib suppression.
filename_img_ref = data_dir + case_ind + '/', 'IL.nii'
filename_img_flo = data_dir + case_ind + '/', 'IH.nii'
filename_img_res = data_dir + case_ind + '/', 'IH_reg.nii'
BSplineReg_save(filename_img_ref, filename_img_flo, filename_img_res)

## Generate dual energy image
fs = 0.1
beta = [0, 0, 0.686564, 0.794393, -0.122075, 0.252449, -0.154831, 9.986063]

# 1) IL & IH
IL_source = nib.load(data_dir + case_ind + '/', 'IL.nii'); IL = IL_source.get_data()
IH_source = nib.load(data_dir + case_ind + '/', 'IH.nii'); IH = IH_source.get_data()
IB = np.exp(beta[2]*np.log(IL) - beta[3]*np.log(IH) + beta[4]*(np.log(IL)**2) + beta[5]*(np.log(IL)*np.log(IH)) + beta[6]*(np.log(IH)**2) + beta[7])

# 2) IL & IH_reg
IL_source = nib.load(data_dir + case_ind + '/', 'IL.nii'); IL = IL_source.get_data()
IH_reg_source = nib.load(data_dir + case_ind + '/', 'IH_reg.nii'); IH_reg = IH_reg_source.get_data()
IB_reg = np.exp(beta[2]*np.log(IL) - beta[3]*np.log(IH_reg) + beta[4]*(np.log(IL)**2) + beta[5]*(np.log(IL)*np.log(IH_reg)) + beta[6]*(np.log(IH_reg)**2) + beta[7])

# 3) IL_supp & IH_supp
IL_supp_source = nib.load(data_dir + case_ind + '/', 'IL_supp.nii'); IL_supp = IL_supp_source.get_data()
IH_supp_reg_source = nib.load(data_dir + case_ind + '/', 'IH_supp_reg.nii'); IH_supp_reg = IH_supp_reg_source.get_data()
IB_reg = np.exp(beta[2]*np.log(IL_supp) - beta[3]*np.log(IH_supp_reg) + beta[4]*(np.log(IL_supp)**2) + beta[5]*(np.log(IL_supp)*np.log(IH_supp_reg)) + beta[6]*(np.log(IH_supp_reg)**2) + beta[7])
