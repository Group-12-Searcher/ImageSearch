# import the necessary packages
import argparse
import glob
import cv2
import csv

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = False, default='dataset\\dataset',
	help = "Path to the directory that contains the images to be indexed")
ap.add_argument("-i", "--index_text", required = False, default='index_text.csv',
	help = "Path to where the computed index will be stored")
args = vars(ap.parse_args())

# open the output index file for writing
output = open(args['index_text'], "w")

reader = csv.reader(open(args["dataset"] + "\\combined_text_tags.txt"), delimiter=" ")
invertedFile = {}

# Generate the Inverted File Index inside invertedFile variable.
for line in reader:
        for i in range(len(line)):
                if (i == 0):
                        img_name = line[0]
                elif (line[i] == '') :
                        continue
                else:
                        if (invertedFile.get(line[i]) == None):
                                invertedFile[line[i]] = [img_name]
                        else:
                                invertedFile[line[i]].append(img_name)       


# Write invertedFile variable into the csv file
for word, img in invertedFile.items():
        output.write("%s,%s\n" % (word, ",".join(img)))

# close the index file
output.close()


