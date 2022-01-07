# Caesar Cipher
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)

#message = 'This is my secret message.' # message to encrypt/ decrypt
message = '"You can show black is white by argument," said Filby, "but you will never convince me."'
key = 8 #set encryption key

mode = 'encrypt' # Set to encrypt or decrypt

SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?.'

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

print(translated)
