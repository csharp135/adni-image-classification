import sys
import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np

#form seg_file,dest_dir,image_id
def execute(dest_dir, image_id, image, slc, axis):
    plt.imshow(np.take(image.get_fdata(), slc, axis=axis), cmap='gray')
    plt.axis('off')
    plt.savefig(dest_dir + image_id +'_'+str(slc)+'_'+str(axis)+ '.png')


if __name__ == "__main__":
    seg_file = sys.argv[1]
    image_id = sys.argv[2]
    dest_dir = sys.argv[3]
    image = nib.load(seg_file)

    #coronal
    for slc in range(100, 109):
        execute(dest_dir, image_id, image, slc, 1)

    #axial
    for slc in range(60, 71):
        execute(dest_dir, image_id, image, slc, 2)

    for slc in range(90, 101):
        execute(dest_dir, image_id, image, slc, 2)

    sys.exit(0)
