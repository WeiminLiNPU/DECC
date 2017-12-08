
## Visualize data

from matplotlib import pyplot as plt
import pickle
import menpo.io as mio
from menpo.visualize import print_progress
import menpo.io as mio
from menpofit.aam import HolisticAAM
from menpo.feature import fast_dsift
from menpofit.aam import LucasKanadeAAMFitter, WibergInverseCompositional
import numpy as np
from menpo.shape import PointDirectedGraph

def fit(path_to_images, path_to_test , c,r,w):
    training_images = []
    for img in print_progress(mio.import_images(path_to_images, verbose=True)):
        # convert to greyscale
        if img.n_channels == 3:
            img = img.as_greyscale()
        # crop to landmarks bounding box with an extra 20% padding
        img = img.crop_to_landmarks_proportion(0.2)
        # rescale image if its diagonal is bigger than 400 pixels
        d = img.diagonal()
        if d > 1000:
            img = img.rescale(1000.0 / d)
        # define a TriMesh which will be useful for Piecewise Affine Warp of HolisticAAM
       # labeller(img, 'PTS', face_ibug_68_to_face_ibug_68_trimesh)
        # append to list
        training_images.append(img)


    # ## Training ribcage - Patch
    # from menpofit.aam import PatchAAM
    # from menpo.feature import fast_dsift
    #
    # patch_aam = PatchAAM(training_images, group='PTS', patch_shape=[(15, 15), (23, 23)],
    #                      diagonal=500, scales=(0.5, 1.0), holistic_features=fast_dsift,
    #                      max_shape_components=20, max_appearance_components=150,
    #                      verbose=True)

    ## Training ribcage - Holistic


    patch_aam = HolisticAAM(training_images, group='PTS', diagonal=500,
                         scales=(0.5, 1.0), holistic_features=fast_dsift, verbose=True,
                         max_shape_components=20, max_appearance_components=150)


    ## Prediction


    fitter = LucasKanadeAAMFitter(patch_aam, lk_algorithm_cls=WibergInverseCompositional,
                                  n_shape=[5, 20], n_appearance=[30, 150])




    image = mio.import_image(path_to_test)



    #initialize box

    adjacency_matrix = np.array([[0, 1, 0, 0],
                                 [0, 0, 1, 0],
                                 [0, 0, 0, 1],
                                 [1, 0, 0, 0],])
    # points = np.array([[0,0], [0,2020], [2020, 2020], [2020, 0]])
    points = np.array([[r-w/2,c-w/2], [r-w/2,c+w/2], [r+w/2,c+w/2], [r+w/2,c-w/2]])
    graph = PointDirectedGraph(points, adjacency_matrix)
    box=graph.bounding_box()

    # initial bbox
    initial_bbox = box

    # fit image
    result = fitter.fit_from_bb(image, initial_bbox, max_iters=[15, 5])

    pts=result.final_shape.points
    return pts

if __name__ == "__main__":
    path_to_train = './data'
    path_to_test = './test/10.jpg'
    center_x=950
    center_y=1100
    width = 1400
    pts=fit(path_to_train, path_to_test, center_x, center_y, width)
    with open('fited-point.pkl','w') as f:
        pickle.dump(pts,f)


