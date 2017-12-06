import os
import nibabel as nib
import numpy as np
import dicom
import matplotlib.pyplot as plt

## convert img1 to nii
H = dicom.read_file('H.dcm')
data = np.array(H.pixel_array)
data = np.flip(np.rot90(data), axis=0)
new_image = nib.Nifti1Image(data, affine=None)
nib.save(new_image, 'H.nii')

## convert img2 to nii
L = dicom.read_file('L.dcm')
data = np.array(L.pixel_array)
data = np.flip(np.rot90(data), axis=0)
new_image = nib.Nifti1Image(data, affine=None)
nib.save(new_image, 'L.nii')


## img registration
img_ref = 'L.nii'
img_flo = 'H.nii'
img_res = 'H_res.nii'

reg_command = 'reg_f3d' + ' -ref ' + img_ref + ' -flo ' + img_flo + ' -res ' + img_res

os.system(reg_command)
