import csv

def get_precision(queryCategory, results):
    count = 0
    index_categories = open("index_categories\\index_categories.csv", 'r')
    catReader = csv.reader(index_categories)
    imageCat = {}
    for row in catReader:
        imageCat[row[0]] = row[1:]
    index_categories.close()

    # print(imageCat)

    for (score, resultID) in results:
        imageID = str(resultID.split("\\")[2])
        # print(resultID.split("\\")[2])
        if imageID in imageCat:
            if str(queryCategory) in imageCat[imageID]:
                count += 1
    return count
