# resize_images
Resizing the images in one folder recursively. Different resizing techniques available.

If you have structure like this:
commonpath/Dataset/train/1/img0.png
commonpath/Dataset/test/0/img1.png

you will transformed (resized images) in this structure:
commonpath/Dataset_method/train/1/img0.png
commonpath/Dataset_method/test/0/img1.png

where method is the provided string as an argument
