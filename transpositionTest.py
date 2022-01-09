# Transposition Cipher Test
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)

import random, sys, string, transpositionEncrypt, transpositionDecrypt

def main():
	random.seed(42)
	for i in range(20):
			message = (string.ascii_letters + string.punctuation + string.digits) * random.randint(4,50)
			message = list(message)
			random.shuffle(message)
			message = ''.join(message)

			print('Test #%s: len: %s "%s..."'% (i+1, len(message), message[:50]))

			for key in range(1, int(len(message)/2)):
				encrypted = transpositionEncrypt.encryptMessage(key, message)
				decrypted = transpositionDecrypt.decryptMessage(key, transpositionEncrypt.encryptMessage(key, message))

				if message != decrypted:
					print('Mismatch with key %s and message %s' % (key, message))
					print('decrypted as: %s' + decrypted)
					sys.exit()

	print('Transpotition cipher passed.')


# If transpositionTest.py is run (instead of imported as a module) call
# the main() function:
if __name__ == '__main__':
	main()