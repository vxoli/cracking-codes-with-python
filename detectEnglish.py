# Detect English module
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)

# To use, type this code:
#   import detectEnglish
#   detectEnglish.isEnglish(someString) # Returns True or False
# (There must be a "dictionary.txt" file in this directory with all
# English words in it, one word per line. You can download this from
# https://www.nostarch.com/crackingcodes/.)
UPPERLETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LETTERS_AND_SPACE = UPPERLETTERS + UPPERLETTERS.lower() + ' \t\n'

def loadDictionary():
    ## English words contains 47006 entries including alpha-numeric words
    # dictionaryFile = open('EnglishWords.txt')
    # englishWords = {}
    # for word in dictionaryFile.read().split('\n'):
    #     englishWords[word.upper()] = None
    # dictionaryFile.close()
    ## If using Oxford Dictionary - 31436 words - but also contains meanings and exaplantions that have to be stripped out:
    dictionaryFile = open('OxfordEnglishDictionary.txt')
    englishWords = {}
    for word in dictionaryFile.read().split('\n'):
        englishWords[word.split(' ')[0].upper()] = None
    dictionaryFile.close()
    return englishWords
ENGLISH_WORDS = loadDictionary()

def getEnglishCount(message):
    message = message.upper()
    message = removeNonLetters(message)
    possibleWords = message.split()

    if possibleWords == []:
        return 0.0 # No words so return 0.0
    matches = 0
    for word in possibleWords:
        if word in ENGLISH_WORDS:
            matches += 1
    return float(matches) / len(possibleWords)

def removeNonLetters(message):
    lettersOnly = []
    for symbol in message:
        if symbol in LETTERS_AND_SPACE:
            lettersOnly.append(symbol)
    return ''.join(lettersOnly)

def isEnglish(message, wordPercentage = 75, letterPercentage = 85):
    # By default, 20% of the words must exist in the dictionary file, and
    # 85% of all the characters in the message must be letters or spaces
    # (not punctuation or numbers).

    wordsMatch = getEnglishCount(message)*100 >= wordPercentage
    numLetters = len(removeNonLetters(message))
    messageLettersPercentage = float(numLetters) / len(message) *100
    lettersMatch = messageLettersPercentage >= letterPercentage
    return wordsMatch and lettersMatch

