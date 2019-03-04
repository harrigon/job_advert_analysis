# Import/download that only needs to be run once
# import nltk
# nltk.download('stopwords')
#####################################
"""
This program is taking the already downloaded job descriptions from trademe.co.nz, tokenizing them and stemming using
the porter snowball stemmer from the nltk library. Run the program tradeMe_job_downloader first to generate the file
 jobDescriptions.xls to work from. Uses python 3.5.
"""
import csv

import sys
import xlrd as xlrd
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import re
from collections import OrderedDict
from operator import itemgetter

def main():

    print(len(sys.argv))
    print(sys.argv[1], sys.argv[2])
    if (sys.argv[1] != 'allSkills') and (sys.argv[1] != 'softSkills'):
        print("Please enter correct parameters. Refer to README.txt for more information")
        exit()
    if (sys.argv[2] != 'stem') and (sys.argv[2] != 'noStem'):
        print("Please enter correct parameters. Refer to README.txt for more information")
        exit()

    skillCondition = sys.argv[1]
    stemCondition = sys.argv[2]

    workbook = xlrd.open_workbook('Job Descriptions/tradeMeJobDescriptions.xls', on_demand=True)
    sheet = workbook.sheet_by_index(0)
    row_dict = {}
    for row_number in range(sheet.nrows):
        row_dict[row_number] = (int(sheet.cell(row_number, 0).value),
                                sheet.cell(row_number, 1).value)
    last_workbook_len = sheet.nrows
    workbook = xlrd.open_workbook('Job Descriptions/githubJobDescriptions.xls', on_demand=True)
    sheet = workbook.sheet_by_index(0)
    for row_number in range(sheet.nrows):
        index = last_workbook_len + row_number
        row_dict[index] = (sheet.cell(row_number, 0).value,
                                sheet.cell(row_number, 1).value)


    tokenized_dict = tokenize_words(row_dict, skillCondition, stemCondition)

    writer = csv.writer(open("Word Frequency/processedJobs-" + skillCondition + '-' + stemCondition + ".csv", 'w+', newline=''))
    for entry in tokenized_dict:
        id = tokenized_dict[entry][0]
        description = ' '.join(str(x) for x in tokenized_dict[entry][1])
        writer.writerow((id, description))

    writer = csv.writer(open("Word Frequency/wordFrequency-" + skillCondition + '-' + stemCondition + ".csv", 'w+', newline=''))
    count_dict = dict()
    for i in tokenized_dict:
        for j in tokenized_dict[i][1]:
            if j not in count_dict:
                count_dict[j] = 1
            else:
                count_dict[j] += 1


    for i in OrderedDict(sorted(count_dict.items(), key = itemgetter(1), reverse= True)):
        writer.writerow((i, count_dict[i]))


def tokenize_words(row_dict, skillCondition, stemCondition):
    """Function that takes a dictionary of summary and description strings. Converts the strings to lowercase. Then
    splits the strings on white space to tokenize into words. Using the nltk library it also removes all stopwords from
    the words."""

    tokenized_dict = {}
    stop_words = set(stopwords.words('english'))
    porter_stemmer = SnowballStemmer("porter")

    #Personal stop words that I have chosen to remove typical job hunting crap
    ##either way we add the general stop words to the set
    myFile = open('stopwords/generalStopWords.txt')
    personalStopWords = set(line.lower().strip() for line in myFile)
    if skillCondition == 'softSkills':
        myFile = open('stopwords/hardSkillStopWords.txt')
        hardSkillStopWords = set(line.lower().strip() for line in myFile)
        personalStopWords.update(hardSkillStopWords)

    stemmedPersonalStopWords = set()
    for word in personalStopWords:
        stemmedPersonalStopWords.add(porter_stemmer.stem(word))


    if(stemCondition == 'stem'):
        for row_key in row_dict:
            id = row_dict[row_key][0]
            description = row_dict[row_key][1].lower().split()
            description_filtered = []

            for word in description:
                if word not in stop_words: #Check if it is in the preset stop words
                    stem_word = porter_stemmer.stem(word) #Stem the word
                    if re.match('^[\w-]+$', stem_word) is not None and (stem_word not in stemmedPersonalStopWords): #check against our stemmed stop words
                        description_filtered.append(stem_word)

            tokenized_dict[row_key] = (id, description_filtered)

    if(stemCondition == 'noStem'):
        for row_key in row_dict:
            id = row_dict[row_key][0]
            description = row_dict[row_key][1].lower().split()
            description_filtered = []

            for word in description:
                if word not in stop_words: #Check if it is in the preset stop words
                    if re.match('^[\w-]+$', word) is not None and (word not in personalStopWords): #check against our stemmed stop words
                        description_filtered.append(word)

            tokenized_dict[row_key] = (id, description_filtered)

    return tokenized_dict



if __name__ == "__main__":
    main()