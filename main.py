# Robert Boutillier
# Assignment 3
# Page Point system, user enters a text file at the command line with 0-4 'keywords'
# Each keyword is then scored and outputted to a text file called report.txt
import sys
from collections import OrderedDict
import operator

# Checking for user input error
if 1 < len(sys.argv) < 7:
    try:
        # read the lines and the words
        linesFile = open(sys.argv[1])
        wordFile = open(sys.argv[1])
        print(sys.argv[1] + " has been opened")
        outputFile = open("report.txt", "w")
        lines = linesFile.readlines()

        for i in range(0, len(lines)):
            lines[i] = lines[i].lower()
        words = wordFile.read()
        words = words.split()

        i = 0
        # lower and strip words of anything in front or the back, such as commas, periods, quotations marks, etc.
        while i < len(words):
            words[i] = words[i].lower()
            words[i] = words[i].strip('"')
            words[i] = words[i].strip("',?.-")
            words[i] = words[i].strip(":;_")
            words[i] = words[i].strip("()")
            words[i] = words[i].strip("!")
            if len(words[i]) < 3:
                del words[i]
                i = i - 1
            i = i + 1

        words.sort()
        count = 0
        wordSet = set(words)
        ind = 0
        print("Counting words")

        wordDict = dict()
        wordDictValues = list()
        wordLines = list()
        wordPages = list()
        # This is where the first dictionary is filled
        print("Getting the lines and pages")
        for i in range(0, len(wordSet)):
            for x in range(0, len(lines)):
                if list(wordSet)[i] in lines[x]:
                    wordLines.append(x)
            wordLines = set(wordLines)
            wordDictValues.append(len(wordLines))
            wordDictValues.append(wordLines)
            for y in range(0, len(wordLines)):
                wordPages.append(int(list(wordLines)[y]) // 25)
            wordPages = set(wordPages)
            wordDictValues.append(wordPages)
            wordDict[list(wordSet)[i]] = wordDictValues
            wordDictValues = list()
            wordLines = list()
            wordPages = list()

        # This first dictionary is sorted.
        sortedWordDict = dict(OrderedDict(sorted(wordDict.items(), key=lambda x: x[1])))
        sortedWordKeys = list(sortedWordDict.keys())
        newWordDict = dict()

        # The secondary dictionary is now the first dictionary minus the bottom 10%.
        for i in range(int(len(sortedWordDict) * 0.10), len(sortedWordDict)):
            newWordDict[sortedWordKeys[i]] = sortedWordDict.get(sortedWordKeys[i])

        print("Dictionary is full")

        # Page points and ranking, all is outputted to a text file called report.txt
        if len(sys.argv) == 2:
            print("No keywords entered, no report generated")

        # Page points for one keyword
        elif len(sys.argv) == 3:
            print("One keyword entered, generating report...")
            keyword = sys.argv[2]
            keyword.lower()
            pagePoints = dict()
            keywordPages = list(newWordDict[keyword][2])
            for page in keywordPages:
                pagePoints[page] = 1

            sortedPagePoints = sorted(pagePoints.items(), key=operator.itemgetter(1))

            outputFile.write("Top ten pages ranked:\n")
            for i in range(0, 10):
                outputFile.write("Page = " + str(sortedPagePoints[(len(sortedPagePoints) - 1) - i][0]) + " Value = "
                                 + str(sortedPagePoints[(len(sortedPagePoints) - 1) - i][1]) + "\n")

            begLine = sortedPagePoints[(len(sortedPagePoints) - 1)][0] * 25
            endLine = begLine + 25
            outputFile.write("\n")

            newLines = list()
            for i in range(begLine, endLine):
                newLines.append(lines[i])
            for i in range(0, len(newLines)):
                newLines[i] = newLines[i].split()

            for i in range(0, len(newLines)):
                for x in range(0, len(newLines[i])):
                    if keyword == newLines[i][x]:
                        newLines[i][x] = newLines[i][x].upper()

            lineword = ""
            for i in range(0, len(newLines)):
                if not newLines[i]:
                    newLines[i] = "\n"
                else:
                    for x in range(0, len(newLines[i])):
                        if not(x == len(newLines[i]) - 1):
                            lineword = lineword + newLines[i][x] + " "
                        else:
                            lineword = lineword + newLines[i][x] + "\n"
                    newLines[i] = lineword
                    lineword = ""
            for line in newLines:
                outputFile.write(line)

        # Page points for two keywords
        elif len(sys.argv) == 4:
            print("Two keywords entered, generating report...")
            keyword1 = sys.argv[2]
            keyword2 = sys.argv[3]
            keyword1.lower()
            keyword2.lower()
            pages = set()
            if keyword1 in newWordDict and keyword2 in newWordDict:
                keyword1Lines = list(newWordDict[keyword1][1])
                keyword2Lines = list(newWordDict[keyword2][1])

                for page in list(newWordDict[keyword1][2]):
                    pages.add(page)
                for page in list(newWordDict[keyword2][2]):
                    pages.add(page)
                pagePoints = dict()
                for page in list(pages):
                    pagePoints[page] = 0

                for page in list(newWordDict[keyword1][2]):
                    pagePoints[page] = 1
                for page in list(newWordDict[keyword2][2]):
                    if pagePoints[page] == 1:
                        pagePoints[page] = 4
                    else:
                        pagePoints[page] = 1
                for line1 in keyword1Lines:
                    for line2 in keyword2Lines:
                        if line1 == line2:
                            pagePoints[line1 // 25] = pagePoints[line1 // 25] + 5
                sortedPagePoints = sorted(pagePoints.items(), key=operator.itemgetter(1))

                outputFile.write("Top ten pages ranked:\n")
                for i in range(0, 10):
                    outputFile.write("Page = " + str(sortedPagePoints[(len(sortedPagePoints) - 1) - i][0]) +
                                     "\tValue = " + str(sortedPagePoints[(len(sortedPagePoints) - 1) - i][1]) + "\n")

                begLine = sortedPagePoints[(len(sortedPagePoints) - 1)][0] * 25
                endLine = begLine + 25
                outputFile.write("\n")

                newLines = list()
                for i in range(begLine, endLine):
                    newLines.append(lines[i])
                for i in range(0, len(newLines)):
                    newLines[i] = newLines[i].split()

                for i in range(0, len(newLines)):
                    for x in range(0, len(newLines[i])):
                        if keyword1 == newLines[i][x] or keyword2 == newLines[i][x]:
                            newLines[i][x] = newLines[i][x].upper()

                lineword = ""
                for i in range(0, len(newLines)):
                    if not newLines[i]:
                        newLines[i] = "\n"
                    else:
                        for x in range(0, len(newLines[i])):
                            if not (x == len(newLines[i]) - 1):
                                lineword = lineword + newLines[i][x] + " "
                            else:
                                lineword = lineword + newLines[i][x] + "\n"
                        newLines[i] = lineword
                        lineword = ""
                for line in newLines:
                    outputFile.write(line)
            else:
                print("Not all of the keywords are in the dictionary.")

        # Page points for three keywords
        elif len(sys.argv) == 5:
            print("Three keywords entered, generating report...")
            keyword1 = sys.argv[2]
            keyword2 = sys.argv[3]
            keyword3 = sys.argv[4]
            print(keyword3)
            keyword1.lower()
            keyword2.lower()
            keyword3.lower()
            pages = set()
            if keyword1 in newWordDict and keyword2 in newWordDict and keyword3 in newWordDict:
                keyword1Lines = list(newWordDict[keyword1][1])
                keyword2Lines = list(newWordDict[keyword2][1])
                keyword3Lines = list(newWordDict[keyword3][1])

                for page in list(newWordDict[keyword1][2]):
                    pages.add(page)
                for page in list(newWordDict[keyword2][2]):
                    pages.add(page)
                for page in list(newWordDict[keyword3][2]):
                    pages.add(page)
                pagePoints = dict()
                for page in list(pages):
                    pagePoints[page] = 0

                for page in list(newWordDict[keyword1][2]):
                    pagePoints[page] = pagePoints[page] + 1
                for page in list(newWordDict[keyword2][2]):
                    if pagePoints[page] == 1:
                        pagePoints[page] = pagePoints[page] + 3
                    else:
                        pagePoints[page] = pagePoints[page] + 1
                for page in list(newWordDict[keyword3][2]):
                    if pagePoints[page] == 1:
                        pagePoints[page] = pagePoints[page] + 3
                    elif pagePoints[page] == 4:
                        pagePoints[page] = pagePoints[page] + 4
                    else:
                        pagePoints[page] = pagePoints[page] + 1
                for line1 in keyword1Lines:
                    for line2 in keyword2Lines:
                        if line1 == line2:
                            pagePoints[line1 // 25] = pagePoints[line1 // 25] + 5
                for line1 in keyword1Lines:
                    for line3 in keyword3Lines:
                        if line1 == line3:
                            pagePoints[line1 // 25] = pagePoints[line1 // 25] + 5
                for line2 in keyword2Lines:
                    for line3 in keyword3Lines:
                        if line2 == line3:
                            pagePoints[line2 // 25] = pagePoints[line2 // 25] + 5
                for line1 in keyword1Lines:
                    for line2 in keyword2Lines:
                        for line3 in keyword3Lines:
                            if line1 == line2 and line1 == line3:
                                pagePoints[line1 // 25] = pagePoints[line1 // 25] + 6
                sortedPagePoints = sorted(pagePoints.items(), key=operator.itemgetter(1))

                outputFile.write("Top ten pages ranked:\n")
                for i in range(0, 10):
                    outputFile.write("Page = " + str(sortedPagePoints[(len(sortedPagePoints) - 1) - i][0]) +
                                     "\tValue = " + str(sortedPagePoints[(len(sortedPagePoints) - 1) - i][1]) + "\n")

                begLine = sortedPagePoints[(len(sortedPagePoints) - 1)][0] * 25
                endLine = begLine + 25
                outputFile.write("\n")

                newLines = list()
                for i in range(begLine, endLine):
                    newLines.append(lines[i])
                for i in range(0, len(newLines)):
                    newLines[i] = newLines[i].split()

                for i in range(0, len(newLines)):
                    for x in range(0, len(newLines[i])):
                        if keyword1 == newLines[i][x] or keyword2 == newLines[i][x] or keyword3 == newLines[i][x]:
                            newLines[i][x] = newLines[i][x].upper()

                lineword = ""
                for i in range(0, len(newLines)):
                    if not newLines[i]:
                        newLines[i] = "\n"
                    else:
                        for x in range(0, len(newLines[i])):
                            if not (x == len(newLines[i]) - 1):
                                lineword = lineword + newLines[i][x] + " "
                            else:
                                lineword = lineword + newLines[i][x] + "\n"
                        newLines[i] = lineword
                        lineword = ""
                for line in newLines:
                    outputFile.write(line)
            else:
                print("Not all of the keywords are in the dictionary.")

        # Page Points for 4 keywords
        elif len(sys.argv) == 6:
            print("Four keywords entered, generating report...")
            keyword1 = sys.argv[2]
            keyword2 = sys.argv[3]
            keyword3 = sys.argv[4]
            keyword4 = sys.argv[5]
            keyword1.lower()
            keyword2.lower()
            keyword3.lower()
            keyword4.lower()
            pages = set()
            if keyword1 in newWordDict and keyword2 in newWordDict and keyword3 in newWordDict and keyword4 in \
                    newWordDict:
                keyword1Lines = list(newWordDict[keyword1][1])
                keyword2Lines = list(newWordDict[keyword2][1])
                keyword3Lines = list(newWordDict[keyword3][1])
                keyword4Lines = list(newWordDict[keyword4][1])

                for page in list(newWordDict[keyword1][2]):
                    pages.add(page)
                for page in list(newWordDict[keyword2][2]):
                    pages.add(page)
                for page in list(newWordDict[keyword3][2]):
                    pages.add(page)
                for page in list(newWordDict[keyword4][2]):
                    pages.add(page)
                pagePoints = dict()
                for page in list(pages):
                    pagePoints[page] = 0

                for page in list(newWordDict[keyword1][2]):
                    pagePoints[page] = pagePoints[page] + 1
                for page in list(newWordDict[keyword2][2]):
                    if pagePoints[page] == 1:
                        pagePoints[page] = pagePoints[page] + 3
                    else:
                        pagePoints[page] = pagePoints[page] + 1
                for page in list(newWordDict[keyword3][2]):
                    if pagePoints[page] == 1:
                        pagePoints[page] = pagePoints[page] + 3
                    elif pagePoints[page] == 4:
                        pagePoints[page] = pagePoints[page] + 4
                    else:
                        pagePoints[page] = pagePoints[page] + 1
                for page in list(newWordDict[keyword3][2]):
                    if pagePoints[page] == 1:
                        pagePoints[page] = pagePoints[page] + 3
                    elif pagePoints[page] == 4:
                        pagePoints[page] = pagePoints[page] + 4
                    elif pagePoints[page] == 8:
                        pagePoints[page] = pagePoints[page] + 5
                    else:
                        pagePoints[page] = pagePoints[page] + 1

                for line1 in keyword1Lines:
                    for line2 in keyword2Lines:
                        if line1 == line2:
                            pagePoints[line1 // 25] = pagePoints[line1 // 25] + 5
                for line1 in keyword1Lines:
                    for line3 in keyword3Lines:
                        if line1 == line3:
                            pagePoints[line1 // 25] = pagePoints[line1 // 25] + 5
                for line2 in keyword2Lines:
                    for line3 in keyword3Lines:
                        if line2 == line3:
                            pagePoints[line2 // 25] = pagePoints[line2 // 25] + 5
                for line1 in keyword1Lines:
                    for line2 in keyword2Lines:
                        for line3 in keyword3Lines:
                            if line1 == line2 and line1 == line3:
                                pagePoints[line1 // 25] = pagePoints[line1 // 25] + 6
                for line1 in keyword1Lines:
                    for line4 in keyword4Lines:
                        if line1 == line4:
                            pagePoints[line1 // 25] = pagePoints[line1 // 25] + 5
                for line2 in keyword2Lines:
                    for line4 in keyword4Lines:
                        if line2 == line4:
                            pagePoints[line2 // 25] = pagePoints[line2 // 25] + 5
                for line3 in keyword3Lines:
                    for line4 in keyword4Lines:
                        if line4 == line3:
                            pagePoints[line3 // 25] = pagePoints[line3 // 25] + 5
                for line1 in keyword1Lines:
                    for line2 in keyword2Lines:
                        for line3 in keyword3Lines:
                            for line4 in keyword4Lines:
                                if line1 == line2 and line1 == line3 and line1 == 4:
                                    pagePoints[line1 // 25] = pagePoints[line1 // 25] + 7
                sortedPagePoints = sorted(pagePoints.items(), key=operator.itemgetter(1))

                outputFile.write("Top ten pages ranked:\n")
                for i in range(0, 10):
                    outputFile.write("Page = " + str(sortedPagePoints[(len(sortedPagePoints) - 1) - i][0]) +
                                     "\tValue = " + str(sortedPagePoints[(len(sortedPagePoints) - 1) - i][1]) + "\n")

                begLine = sortedPagePoints[(len(sortedPagePoints) - 1)][0] * 25
                endLine = begLine + 25
                outputFile.write("\n")

                newLines = list()
                for i in range(begLine, endLine):
                    newLines.append(lines[i])
                for i in range(0, len(newLines)):
                    newLines[i] = newLines[i].split()

                for i in range(0, len(newLines)):
                    for x in range(0, len(newLines[i])):
                        if keyword1 == newLines[i][x] or keyword2 == newLines[i][x] or keyword3 == newLines[i] or \
                        keyword4 == newLines[i][x]:
                            newLines[i][x] = newLines[i][x].upper()

                lineword = ""
                for i in range(0, len(newLines)):
                    if not newLines[i]:
                        newLines[i] = "\n"
                    else:
                        for x in range(0, len(newLines[i])):
                            if not (x == len(newLines[i]) - 1):
                                lineword = lineword + newLines[i][x] + " "
                            else:
                                lineword = lineword + newLines[i][x] + "\n"
                        newLines[i] = lineword
                        lineword = ""
                for line in newLines:
                    outputFile.write(line)
            else:
                print("Not all of the keywords are in the dictionary.")

        print("Report generated")
        outputFile.close()
        linesFile.close()
        wordFile.close()
    except FileNotFoundError:
        print("ERROR, file not found")
elif len(sys.argv) > 7:
    print("ERROR, maximum of 4 keywords")
else:
    print("You need to enter a file")
