import csv
import re
from time import time
import math
import psutil

frenchTranslation = {}
frequency = {}


def csvReader(fileName):
    with open(fileName, 'r') as csvFile:
        reader = csv.reader(csvFile)

        for row in reader:
            frenchTranslation[row[0]] = row[1]


def caseChecker(englishWord, frenchWord):
    frenchWord = frenchWord.lower()

    if englishWord.isupper():
        frenchWord = frenchWord.upper()
    else:
        if englishWord[0].isupper():
            frenchWord = frenchWord.capitalize()

    return frenchWord


def translator(fileName):
    with open('find_words.txt', 'r') as file:
        findWordsList = file.read().splitlines()

    with open(fileName, "r") as inputFile:
        contents = inputFile.readlines()

    for num1, line in enumerate(contents, 1):
        wordList = line.split(" ")

        for num, word in enumerate(wordList, 0):
            for originalWord in findWordsList:
                if re.search(rf"\b{originalWord}\b", word, re.IGNORECASE):
                    if originalWord in frequency:
                        frequency[originalWord] += 1
                    else:
                        frequency[originalWord] = 1

                    englishWord = re.search(rf"\b{originalWord}\b", wordList[num], re.IGNORECASE).group()
                    frenchWord = caseChecker(englishWord, frenchTranslation[originalWord])

                    wordList[num] = re.sub(pattern=rf"\b{originalWord}\b", repl=frenchWord,
                                           string=wordList[num], flags=re.IGNORECASE, count=1)

        num1 = num1 - 1
        contents[num1] = " ".join(wordList)
        num1 = num1 + 1

        print(contents[num1-1])

    with open("t8.shakespeare.translated.txt", 'a') as outputFile:
        contents = "".join(contents)
        outputFile.write(contents)

    with open("frequency.csv", 'a') as frequencyFile:
        writer = csv.writer(frequencyFile, dialect='excel')
        headers = ["English word", "French word", "Frequency"]
        writer.writerow(headers)

        for word in frequency:
            row = [word, frenchTranslation[word], frequency[word]]
            writer.writerow(row)


def timeCalculator(startTime, endTime):
    processTime = (endTime - startTime) / 60
    formattedTime = math.modf(processTime)

    seconds = int(formattedTime[0] * 100)
    minutes = int(formattedTime[1])

    with open('performance.txt', 'a') as outputFile:
        timeOutput = "Time to process: " + str(minutes) + " minutes " + str(seconds) + " seconds\n"
        outputFile.write(timeOutput)


def memoryCalculator():
    with open('performance.txt', 'a') as outputFile:
        memoryUsed = psutil.virtual_memory().used >> 20
        memoryOutput = "Memory used: " + str(memoryUsed) + " MB"
        outputFile.write(memoryOutput)


def main():
    startTime = time()
    csvReader('french_dictionary.csv')
    translator('t8.shakespeare.txt')
    endTime = time()

    timeCalculator(startTime, endTime)
    memoryCalculator()


if __name__ == '__main__':
    main()
