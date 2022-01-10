# Affine Cipher Hacker 
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)

import affineCipher, detectEnglish, cryptomath

SILENT_MODE = False

def main():
	myMessage = """5QG9ol3La6QI93!xQxaia6faQL9QdaQG1!!axQARLa!!A
	uaRLQADQALQG93!xQxaGaAfaQ1QX3o1RQARL9Qda!AafARuQLX1LQALQI1
	iQX3o1RN"Q-5!1RQP36ARu"""

	hackedMessage = hackAffine(myMessage)

	if hackedMessage != None:
		print(hackedMessage)
	else:
		print('Failed to hack message')

def hackAffine(message):
	print('Hacking...')

	for key in range(len(affineCipher.SYMBOLS) ** 2):
		keyA = affineCipher.getKeyParts(key)[0]
		if cryptomath.gcd(keyA, len(affineCipher.SYMBOLS)) != 1:
			continue

		decryptedText = affineCipher.decryptMessage(key, message)
		if not SILENT_MODE:
			print('Tried Key: %s...(%s)' % (key, decryptedText[:40]))
		if detectEnglish.isEnglish(decryptedText):
			print('Possible hack:')
			print('Key: %s' % (key))
			print('Decrypted Message: ' + decryptedText[:200])
			print()
			return decryptedText

	return None



if __name__ == '__main__':
	main()