from nltk.corpus import wordnet
import operator

db_categories = []
deeplearning_categories = []

f = open("category_names.txt", 'r')
for line in f:
    db_categories.append(line.split('\n')[0])
#print(db_categories)

f = open("imagenet_class_index.json", 'r')
classes = f.readline().split(':')
for c in classes[1:]:
    deeplearning_categories.append(c.split('"')[3])
#print(deeplearning_categories)

outputCSV = open("index_deeplearning.csv", "w")
categs = [str(c) for c in db_categories]
outputCSV.write("%s,%s\n" % (" ", ",".join(categs)))

outputTXT = open("index_deeplearning.txt", "w")
for word1 in deeplearning_categories:
    result = {}
    scores = []
    for word2 in db_categories:
        wordFromList1 = wordnet.synsets(word1)
        wordFromList2 = wordnet.synsets(word2)
        if wordFromList1 and wordFromList2:
            score = 0
            for w1 in wordFromList1:
                for w2 in wordFromList2:
                    s = w1.wup_similarity(w2)
                    if s > score:
                        score = s
            result[word2] = score
            scores.append(score)
            #print(word1, word2, score)
    scores = [str(s) for s in scores]
    outputCSV.write("%s,%s\n" % (word1, ",".join(scores)))
    sorted_result = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
    print(word1, sorted_result)
    outputTXT.write("%s: %s\n" % (word1, sorted_result))
    print("")
    
outputCSV.close()
outputTXT.close()

'''p = wordnet.synsets('peacock')
d = wordnet.synsets('dog')
b = wordnet.synsets('bird')
print(p, d, b)
for pp in p:
    print(pp)
    for dd in d:
        print(dd, pp.wup_similarity(dd))
for pp in p:
    print(pp)
    for bb in b:
        print(bb, pp.wup_similarity(bb))'''

'''p = wordnet.synsets('printer')
c = wordnet.synsets('computer')
print(p,c)
for pp in p:
    print(pp)
    for dd in c:
        print(dd, pp.wup_similarity(dd))'''



