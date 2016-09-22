from nltk.corpus import wordnet
import operator

db_categories = []
deeplearning_categories = []

f = open("category_names.txt", 'r')
for line in f:
    db_categories.append(line.split('\n')[0])
print(db_categories)

f = open("imagenet_class_index.json", 'r')
classes = f.readline().split(':')
for c in classes[1:]:
    deeplearning_categories.append(c.split('"')[3])
print(deeplearning_categories)

output = open("index_deeplearning.csv", "w")
categs = [str(c) for c in db_categories]
output.write("%s,%s\n" % (" ", ",".join(categs)))

for word1 in deeplearning_categories:
    result = {}
    values = []
    for word2 in db_categories:
        wordFromList1 = wordnet.synsets(word1)
        wordFromList2 = wordnet.synsets(word2)
        if wordFromList1 and wordFromList2:
            s = wordFromList1[0].wup_similarity(wordFromList2[0])
            result[word2] = s
            values.append(s)
            print(word1, word2, s)
    values = [str(v) for v in values]
    output.write("%s,%s\n" % (word1, ",".join(values)))
    sorted_result = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
    print(sorted_result)
    
output.close()
