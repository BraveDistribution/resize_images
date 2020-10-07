import argparse
import cv2
import os
import shutil

from pathlib import Path

SUPPORTED_METHODS = ["INTER_NEAREST", "INTER_LINEAR", "INTER_AREA", "INTER_CUBIC", "INTER_LANCZOS4"]

# In case that you use any other image, feel free to add it here.
IMAGES_EXTENSION_SUPPORTED = (".jpg", ".png", ".jpeg")


def ig_f(directory, files):
    return [f for f in files if os.path.isfile(os.path.join(directory, f))]

def is_image_file(filename): 
    """ Check extension and returns true if extension is one of IMAGES_EXTENSION_SUPPORTER, otherwise false""" 
    if filename.lower().endswith(IMAGES_EXTENSION_SUPPORTED):
        return True
    else:
        return False

def transform_image(image, method, img_width, img_height):
    """ Transforms given image and returns it back """
    if method == "INTER_NEAREST":
        return cv2.resize(image, dsize=(img_width, img_height),  interpolation=cv2.INTER_NEAREST)
    if method == "INTER_AREA":
        return cv2.resize(image, dsize=(img_width, img_height),  interpolation=cv2.INTER_AREA)
    if method == "INTER_CUBIC":
        return cv2.resize(image, dsize=(img_width, img_height),  interpolation=cv2.INTER_CUBIC)
    if method == "INTER_LANCZOS4":
        return cv2.resize(image, dsize=(img_width, img_height),  interpolation=cv2.INTER_LANCZOS4)
    if method == "INTER_LINEAR":
        return cv2.resize(image, dsize=(img_width, img_height), interpolation=cv2.INTER_LINEAR)

parser = argparse.ArgumentParser(description="Script that resize images by specificd method while perserving the folder structure")
parser.add_argument('--path', type=str, help="Full path to the root node where the images are saved")
parser.add_argument('--method', type=str, help="One of %s" % SUPPORTED_METHODS)
parser.add_argument('--img_width', type=int, help="Wanted img width")
parser.add_argument('--img_height', type=int, help="Wanted img height") 
args = parser.parse_args()

dir_path = args.path
method = args.method
img_width = args.img_width
img_height = args.img_height

dir_path = str(Path(dir_path))
print('Path: %s' % dir_path) 
print('Method used: %s' % method)
print('Images will be resized into img_width: %f, img_height: %f' % (img_width, img_height))

dataset_name = dir_path.split("/", -1)[-1]

if method not in SUPPORTED_METHODS: 
    raise ValueError("Method \"%s\" is not supported, choose one of: %s" % (method, SUPPORTED_METHODS))
if not os.path.exists(dir_path):
    raise ValueError("Dir with path \"%s\" does not exist" % dir_path)

# directory will be created with the same structure and name with method appended to it. ex CheXPert/CheXPert_INTER_NEAREST
path_to_save = dir_path + "_" + method
print("Path to save new dataset: ", path_to_save)

# TODO: in the future we should let to choose where the new dataset should be saved, but this is for the current situation sufficient
if os.path.exists(path_to_save):
    raise ValueError("Path \"%s\" already exists" % path_to_save)

shutil.copytree(dir_path, path_to_save, ignore=ig_f)

# The structure of folders should be copied, now let's walk through the image and if there is a file (not image) copy it, if there is an image file transform it and save on the same path.

for root, dirs, files in os.walk(dir_path, topdown=False):
    for file_name in files:
        "Root = dir where the image should be saved, but with the changed upper root dir"
        "File name = name of the file that should be copied"
        file_name_with_path = root+"/"+file_name 
        if is_image_file(file_name):
            """ Transform and copy the file """
            img = cv2.imread(file_name_with_path)
            img = transform_image(img, method, img_width, img_height)
            cv2.imwrite(file_name_with_path.replace(dataset_name, dataset_name+"_" + method), img)
        else:
            """ Just copy over the file """    
            shutil.copyfile(file_name_with_path, file_name_with_path.replace(dataset_name, dataset_name+"_" + method))
