# Caesar Hacker
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)

#message = 'This is my secret message.' # message to encrypt/ decrypt
message = 'qeFIP?eGSeECNNS,'

SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.'

mode = 'decrypt' # Set to encrypt or decrypt

for key in range(len(SYMBOLS)):

	translated = ''

	for symbol in message:
		if symbol in SYMBOLS:
			symbolIndex = SYMBOLS.find(symbol)
			if mode == 'encrypt':
				translatedIndex = (symbolIndex + key) % len(SYMBOLS)
			elif mode == 'decrypt':
				translatedIndex = (symbolIndex - key) % len(SYMBOLS)

			translated = translated + SYMBOLS[translatedIndex]
		else:
			translated = translated + symbol

	print('Key #%s: %s'% (key, translated))
