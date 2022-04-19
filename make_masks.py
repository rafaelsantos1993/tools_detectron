#Converts a polygon image annotations (created by VIA - VGG annotator)

#Required libraries 

import numpy as np
import os, json, cv2, random# enumerating the annotations (v) and image id (idx)
from skimage import transform
from skimage.draw import polygon
from scipy import ndimage 

#Takes as input the path where the images are located and the polygons
#It saves the results in '/img_dir/masks'

def make_masks(img_dir, annotations_path):
    
    #criates the path to 'img_dir/masks' to salve the masks 
    masks_dir=os.path.join(img_dir,'masks')
    try: 
        os.mkdir(os.path.join(masks_dir))
    
    except:
        print('Using existing mask folder')

    #list the files in the folder to make the transformations 
    imgs_list=[img for img in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir,img))]

    #reads the json file 
     
    with open(annotations_path) as f:  
        imgs_anns=json.load(f)
    
    # enumerating the annotations (v) and image id (idx)

    for idx,v in enumerate(imgs_anns.values()): 
        
        filename_path=os.path.join(img_dir,v['filename'])
        filename=v['filename']
        print(filename_path)   # show the made files
        height, width=cv2.imread(filename_path).shape[:2] 
        
        #makes a ditionary with the objcts ids, necessary for the masks identifications 
        annos={}
        annos_old=v['regions']
        obj_id=0
        mask=np.zeros([height,width], dtype=np.uint8)
        for i in annos_old:
          annos[str(obj_id)]=i
          obj_id+=1

        for _, anno in annos.items(): #gwts the pollylines with the coordinate pairs. 
            anno=anno["shape_attributes"]
            px=anno['all_points_x']
            py=anno['all_points_y']
            r,c=polygon(py,px)
            mask[r-1,c-1]=1 # due to polygon annotations compatibility with numpy indexes 

        #Saves the  work the directory. 
        root_filename=filename.split('.')
        root_filename=root_filename[0]
        cv2.imwrite(os.path.join(masks_dir,root_filename+'.png'), mask)