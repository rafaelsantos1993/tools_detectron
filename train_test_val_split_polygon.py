#Script to split a dataset's masks annotions in the poligon/json format
#made by VIA-VGG 

#library to work with json and images 

import json 
import os
import random 
from math import floor
from shutil import move


#train_test_val_split_polygon can work in two diferents ways 
#By reciving the images names for the test and val folders 
# or by receing a percetage of imagens  to be allocated in the train test folders.
#In the end, both images and created annotations files ("datasetName.json - that might be train, test or val") are
#allocated to a new made subdir ("/train test or val") where the images' folder are oginally located 

def train_test_val_split_polygon (annotations_path,images_path, test_names=[], val_names=[], \\
                                    test_proportion=0.15, val_proportion=0.05, seed=None):
  
  with open(annotations_path) as f: 
    imgs_anns=json.load(f)

  #dictionary to save the annotations of each dataset 
  test_annos={} 
  val_annos={}
  train_annos={}

  #get the image keys from the json  
  images_keys=list(imgs_anns.keys())

  #if the image names are used to split the datasets 

  if (test_names or val_names):
    #if the image keys are in the list of train or val, they are allocated to val or test, otherwise, they are send to the train dataset 
    for image_name in images_keys:
      img_dict=imgs_anns[image_name]
      if img_dict['filename'] in test_names:
        test_annos[image_name]=imgs_anns[image_name]
      elif img_dict['filename'] in val_names:
        val_annos[image_name]=imgs_anns[image_name]
      else:
        train_annos[image_name]=imgs_anns[image_name]

    #for the case where the images are randomically allocated 
  else: 
      if seed: #to make the result reproductible 
        random.seed(seed) 
      dataset_size=len(images_keys) 
      test_size=floor(dataset_size*test_proportion)
      val_size=floor(dataset_size*val_proportion)
      train_size=dataset_size-test_size-val_size

      random.shuffle(images_keys)

      #split the images in train, test and val 
      train_image_keys=images_keys[0:train_size]
      test_image_keys=images_keys[train_size:(train_size+test_size)]
      val_image_keys=images_keys[(train_size+test_size):dataset_size]
      

      for image in images_keys:

        if image in train_image_keys:
          train_annos[image] = imgs_anns[image]

        elif image in test_image_keys:
          test_annos[image] = imgs_anns[image]
        
        else:
          val_annos[image] = imgs_anns[image]
      
      #Gets the images real name and print
      for dataset_key_names in [train_image_keys, test_image_keys, val_image_keys]:
        if len(dataset_key_names)>0:
          for i in range(len(dataset_key_names)): 
            new_image_name = dataset_key_names[i].split('.')
            new_image_name = new_image_name[0]+'.JPG'
            dataset_key_names[i]=new_image_name
      print("Images in  Test:", test_image_keys, "\nImages in val: ", val_image_keys)
      

  # save images and and annotations in the corresponding dataset dir 

  save_dir=os.path.dirname(annotations_path)
  

  for dir in ['train', 'test','val']:
  
    to_move_dir = os.path.join(images_path,dir)
    
    try:
      os.mkdir(to_move_dir)
    except:
      pass
    

    #save annotations 
    with open(os.path.join(to_move_dir, dir + ".json"), "w") as outfile:
      json.dump(eval(dir+"_annos"), outfile)
    
    #moving files 
    image_names = eval(dir+'_image_keys')
    for image_name in image_names:
      
      original_dir = (os.path.join(images_path,image_name))
      to_move_image_dir = os.path.join(to_move_dir,image_name)
      move(original_dir,to_move_image_dir)
