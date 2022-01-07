# Transposition Cipher Decryption
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)

import math

def main():
	myMessage = 'Cenoonommstmme oo snnio. s s c'
	myKey = 8

	plaintext = decryptMessage(myKey, myMessage)

	print('|' + plaintext + '|')

def decryptMessage(key, message):
	numOfColumns = int(math.ceil(len(message)/ float(key)))
	numOfRows = key
	numOfShadedBoxes = (numOfColumns*numOfRows)-len(message)

	plaintext = ['']*numOfRows

	column = row = 0

	for symbol in message:
		plaintext[column] += symbol
		column += 1


		if (column == numOfColumns) or (column == numOfColumns - 1 and row >= numOfRows - numOfShadedBoxes):
			column = 0
			row += 1

	return ''.join(plaintext)

if __name__ == '__main__':
	main()
