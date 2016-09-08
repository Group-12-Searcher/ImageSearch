# USAGE
# python index.py --dataset dataset --index index.csv

# import the necessary packages
from pyimagesearch.semanticsreader import SemanticsReader
import argparse
import glob
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--semantics", required = False, default='semantics',
	help = "Path to the directory that contains the images to be indexed")
ap.add_argument("-i", "--index_semantics", required = False, default='index_semantics.csv',
	help = "Path to where the computed index will be stored")
args = vars(ap.parse_args())

# initialize the semantics reader
sr = SemanticsReader()

# open the output index file for writing
output = open(args['index_semantics'], "w")

# use glob to grab the image paths and loop over them
for textFile in glob.glob(args["semantics"] + "/*.txt"):
        if '/' in textFile:
                imageID = textFile[textFile.rfind("/") + 1:].split(".")[0]+".jpg"
        else:
                imageID = textFile[textFile.rfind("\\") + 1:].split(".")[0]+".jpg"
        # extract semantics values from text file
        features = sr.read(textFile)

        # write the features to file
        features = [str(f) for f in features]
        output.write("%s,%s\n" % (imageID, ",".join(features)))

# close the index file
output.close()


