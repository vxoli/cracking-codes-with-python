# Makes the wordPatterns.py File
# https://www.nostarch.com/crackingcodes (BSD Licensed)

# Creates wordPatterns.py based on the words in our dictionary
# text file, dictionary.txt. (Download this file from
# https://invpy.com/dictionary.txt)

import pprint


def getWordPattern(word):
    # Returns a string of the pattern form of the given word.
    # e.g. '0.1.2.3.4.1.2.3.5.6' for 'DUSTBUSTER'
    word = word.upper()
    nextNum = 0
    letterNums = {}
    wordPattern = []

    for letter in word:
        if letter not in letterNums:
            letterNums[letter] = str(nextNum)
            nextNum += 1
        wordPattern.append(letterNums[letter])
    return '.'.join(wordPattern)


def main():
    allPatterns = {}

    # Modifications for file OxfordEnglishDictionary
    # split on \n\n not just \n as there is line between entries
    #each line will have word and dictioary entry with difinition/ usage/ history etc.
    #these are split off and blank entries dropped
    fo = open('OxfordEnglishDictionary.txt')
    wordList = fo.read().split('\n\n')
    fo.close()
    wordList = list([wordList[i].split(' ')[0].upper() for i in range(len(wordList)) if (wordList[i] != '')])

    for word in wordList:
        if word == '': continue
        # Get the pattern for each string in wordList:
        pattern = getWordPattern(word)

        if pattern not in allPatterns:
            allPatterns[pattern] = [word]
        else:
            allPatterns[pattern].append(word)

    # This is code that writes code. The wordPatterns.py file contains
    # one very, very large assignment statement:
    fo = open('wordPatterns.py', 'w')
    fo.write('allPatterns = ')
    fo.write(pprint.pformat(allPatterns))
    fo.close()


if __name__ == '__main__':
    main()