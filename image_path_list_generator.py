import glob

image_list = open('image_list.txt', 'w')

# use glob to grab the image paths and loop over them
for imagePath in glob.glob("dataset\dataset\*.jpg"):
	# extract the image ID (i.e. the unique filename) from the image
	# path and load the image itself
	print imagePath
	
	# write the image path-name to file
	tempstr = "..\\..\\ImageSeach_demo\\" + "%s\n" % imagePath
	image_list.write(tempstr.replace("\\","\\\\"))

# close the index file
image_list.close()
