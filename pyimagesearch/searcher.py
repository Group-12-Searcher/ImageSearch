# import the necessary packages
import numpy as np
import csv
import cv2
import glob
import subprocess
import os
import threading
from mysift import myMatch, myMatch2

class Searcher:        
	def __init__(self, indexPath, semanticsPath):
		# store our index path
		self.indexPath = indexPath
		self.semanticsPath = semanticsPath
                self.WEIGHT_CH = 0.25
                self.WEIGHT_SEM = 0.5
                self.WEIGHT_SIFT = 0.25
                self.results = {}

        class myThread(threading.Thread):
            def __init__(self, searcher, dbImage):
                threading.Thread.__init__(self)
                self.searcher = searcher
                self.dbImage = dbImage
                
            def run(self):
                exe = 'match'
                im1 = "temp/query.pgm"
                k1 = "temp/query.key"
                im2 = self.dbImage+".pgm"
                k2 = self.dbImage+".key" 
                args = [exe, '-im1', im1, '-k1', k1, '-im2', im2, '-k2', k2]
                FNULL = open(os.devnull, 'w')

                p = subprocess.Popen(args, stdout=FNULL, stderr=subprocess.PIPE)
                line = p.stderr.readline()
                print(line[0:-2]+" with "+self.dbImage)

                numMatches = line.split(' ')[1]
                d = float(numMatches)
                self.searcher.results["dataset\\dataset\\"+self.dbImage+".jpg"] -= d * self.searcher.WEIGHT_SIFT                

	def search(self, queryFeatures, querySemantics, limit = 32):
		# open the color histogram index file for reading
		with open(self.indexPath) as f:
			# initialize the CSV reader
			reader = csv.reader(f)

			# loop over the rows in the index
			for row in reader:
				# parse out the image ID and features, then compute the
				# chi-squared distance between the features in our index
				# and our query features
				features = [float(x) for x in row[1:]]
				d = self.chi2_distance(features, queryFeatures)
				
				# now that we have the distance between the two feature
				# vectors, we can udpate the self.results dictionary -- the
				# key is the current image ID in the index and the
				# value is the distance we just computed, representing
				# how 'similar' the image in the index is to our query
				self.results[row[0]] = d * self.WEIGHT_CH
				
			# close the reader
			f.close()

		# open the semantics index file for reading
		with open(self.semanticsPath) as f:
			# initialize the CSV reader
			reader = csv.reader(f)

			# loop over the rows in the index
			for row in reader:
				# parse out the image ID and features, then compute the
				# chi-squared distance between the features in our index
				# and our query features
				features = [float(x) for x in row[1:]]
				'''
                                features = []
                                for x in row[1:]:
                                        print(x)
                                        print("---")
                                        features.append(float(x))
                                '''

                                                        
				d = self.chi2_distance(features, querySemantics)
				
				# now that we have the distance between the two feature
				# vectors, we can udpate the results dictionary -- the
				# key is the current image ID in the index and the
				# value is the distance we just computed, representing
				# how 'similar' the image in the index is to our query
				self.results[row[0]] += d * self.WEIGHT_SEM
				
			# close the reader
			f.close()


                # Do sift matching
                os.chdir("sift")
                threads = []
                for f in glob.glob("*.key"):
                        dbImage = f.split('/')[-1].split('.')[0]
                        t = self.myThread(self, dbImage)
                        t.start()
                        threads.append(t)
                for t in threads:
                        t.join()
                        
                ### My own experimental sift ###
                '''
                os.chdir("sift")
                for f in glob.glob("*.key"):
                        dbImage = f.split('/')[-1].split('.')[0]
                        im1 = "temp/query.pgm"
                        im2 = dbImage+".pgm"
                        d = myMatch(im1, im2)
                        self.results["dataset\\dataset\\"+dbImage+".jpg"] -= d * self.WEIGHT_SIFT
                '''
                
                os.chdir("..")

		# sort our results, so that the smaller distances (i.e. the
		# more relevant images are at the front of the list)
		self.results = sorted([(v, k) for (k, v) in self.results.items()])
		
		# return our (limited) self.results
		return self.results[:limit]

	def chi2_distance(self, histA, histB, eps = 1e-10):
		# compute the chi-squared distance
		d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
			for (a, b) in zip(histA, histB)])

		# return the chi-squared distance
		return d
