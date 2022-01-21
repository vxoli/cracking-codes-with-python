# Vigenere Cipher Hacker
# https://www.nostarch.com/crackingcodes (BSD Licensed)

import itertools, re
import vigenereCipher, freqAnalysis, detectEnglish

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
MAX_KEY_LENGTH = 16 # Won't attempt key length longer than this
NUM_MOST_FREQ_LETTERS = 4 # Attempt this many letters per subkey
SILENT_MODE = False # If set Ture programe doesn't print anything
NONLETTERS_PATTERN = re.compile('[^A-Z]')

def main():
	ciphertext = """Adiz Avtzqeci Tmzubb wsa m Pmilqev halpqavtakuoi, lgouqdaf, kdmktsvmztsl, izr xoexghzr kkusitaaf. Vz wsa twbhdg ubalmmzhdad qz hce vmhsgohuqbo ox kaakulmd gxiwvos, krgdurdny i rcmmstugvtawz ca tzm ocicwxfg jf "stscmilpy" oid "uwydptsbuci" wabt hce Lcdwig eiovdnw. Bgfdny qe kddwtk qjnkqpsmev ba pz tzm roohwz at xoexghzr kkusicw izr vrlqrwxist uboedtuuznum. Pimifo Icmlv Emf DI, Lcdwig owdyzd xwd hce Ywhsmnemzh Xovm mby Cqxtsm Supacg (GUKE) oo Bdmfqclwg Bomk, Tzuhvif'a ocyetzqofifo ositjm. Rcm a lqys ce oie vzav wr Vpt 8, lpq gzclqab mekxabnittq tjr Ymdavn fihog cjgbhvnstkgds. Zm psqikmp o iuejqf jf lmoviiicqg aoj jdsvkavs Uzreiz qdpzmdg, dnutgrdny bts helpar jf lpq pjmtm, mb zlwkffjmwktoiiuix avczqzs ohsb ocplv nuby swbfwigk naf ohw Mzwbms umqcifm. Mtoej bts raj pq kjrcmp oo tzm Zooigvmz Khqauqvl Dincmalwdm, rhwzq vz cjmmhzd gvq ca tzm rwmsl lqgdgfa rcm a kbafzd-hzaumae kaakulmd, hce SKQ. Wi 1948 Tmzubb jgqzsy Msf Zsrmsv'e Qjmhcfwig Dincmalwdm vt Eizqcekbqf Pnadqfnilg, ivzrw pq onsaafsy if bts yenmxckmwvf ca tzm Yoiczmehzr uwydptwze oid tmoohe avfsmekbqr dn eifvzmsbuqvl tqazjgq. Pq kmolm m dvpwz ab ohw ktshiuix pvsaa at hojxtcbefmewn, afl bfzdakfsy okkuzgalqzu xhwuuqvl jmmqoigve gpcz ie hce Tmxcpsgd-Lvvbgbubnkq zqoxtawz, kciup isme xqdgo otaqfqev qz hce 1960k. Bgfdny'a tchokmjivlabk fzsmtfsy if i ofdmavmz krgaqqptawz wi 1952, wzmz vjmgaqlpad iohn wwzq goidt uzgeyix wi tzm Gbdtwl Wwigvwy. Vz aukqdoev bdsvtemzh rilp rshadm tcmmgvqg (xhwuuqvl uiehmalqab) vs sv mzoejvmhdvw ba dmikwz. Hpravs rdev qz 1954, xpsl whsm tow iszkk jqtjrw pug 42id tqdhcdsg, rfjm ugmbddw xawnofqzu. Vn avcizsl lqhzreqzsy tzif vds vmmhc wsa eidcalq; vds ewfvzr svp gjmw wfvzrk jqzdenmp vds vmmhc wsa mqxivmzhvl. Gv 10 Esktwunsm 2009, fgtxcrifo mb Dnlmdbzt uiydviyv, Nfdtaat Dmiem Ywiikbqf Bojlab Wrgez avdw iz cafakuog pmjxwx ahwxcby gv nscadn at ohw Jdwoikp scqejvysit xwd "hce sxboglavs kvy zm ion tjmmhzd." Sa at Haq 2012 i bfdvsbq azmtmd'g widt ion bwnafz tzm Tcpsw wr Zjrva ivdcz eaigd yzmbo Tmzubb a kbmhptgzk dvrvwz wa efiohzd."""
	hackedMessage = hackVigenere(ciphertext)

	if hackVigenere != None:
		print(hackedMessage)
	else:
		print('Failed to decrypt message')

def findRepeatSequencesSpacings(message):
	# Goes through message and finds 3-5 letter sequences
	# that are repeated. Returns a dict with the keys of the sequence and
	# values of a list of spacings (num letters between the repeats)

	# Use regex to remove non-letters from message
	message = NONLETTERS_PATTERN.sub('',message.upper())

	# Compile a list of seqLen-Letter combinations found in the message
	seqSpacings = {} # Keys are sequences, values are lists of int spacings
	for seqLen in range(3,6):
		for seqStart in range(len(message)-seqLen):
			# Determine what sequence is and store in seq
			seq = message[seqStart:seqStart+seqLen]

			# Look for this sequene in the rest of the message
			for i in range(seqStart+seqLen,len(message)-seqLen):
				if message[i:i+seqLen] == seq:
					# Found a repeating sequence
					if seq not in seqSpacings:
						seqSpacings[seq] = [] #initialise blank list
					# Append the spacing distance between the repeated
					# sequences and the original sequence
					seqSpacings[seq].append(i-seqStart)

	return seqSpacings

def getUsefulfactors(num):
	# Returns a list of useful factors of num
	# Useful means factors less than MAY_KEY_LENGTH + 1 and not 1.
	# For example getUsefulFactors(144) returns [2,3,4,6,8,9,12,16]

	if num < 2:
		return{} # Numbers less than 2 have no useful factors

	factors = []
	for i in range(2,MAX_KEY_LENGTH+1): # Don't test 1 : its not useful
		if num % i == 0:
			factors.append(i)
			otherFactor = int(num/i)
			if otherFactor < MAX_KEY_LENGTH+1 and otherFactor != 1:
				factors.append(otherFactor)

	return list(set(factors)) # Removes duplicates

def getItemAtIndexOne(x):
	return x[1]

def getMostCommonFactors(seqFactors):
	# First get a count of how many times the factor in seqFactors
	factorCounts = {} # Key is factor, value is list of the factors of the spacings

	for seq in seqFactors:
		factorList = seqFactors[seq]
		for factor in factorList:
			if factor not in factorCounts:
				factorCounts[factor] = 0
			factorCounts[factor] += 1
	# Second place factor and its count in a tuple and make a list of these tuples so can be sorted
	factorsByCount = []
	for factor in factorCounts:
		#Exclude factors larger than MAX_KEY_LENGTH
		if factor <= MAX_KEY_LENGTH:
			factorsByCount.append((factor,factorCounts[factor]))
	# Sort the list by factor count
	factorsByCount.sort(key=getItemAtIndexOne, reverse = True)

	return factorsByCount

def kasiskiExamination(ciphertext):
	# Find the sequences of 3-5 letters that occur multiple times
	# in the ciphertext. 
	repeatedSeqSpacings = findRepeatSequencesSpacings(ciphertext)
	seqFactors = {}
	for seq in repeatedSeqSpacings:
		seqFactors[seq] = []
		for spacing in repeatedSeqSpacings[seq]:
			seqFactors[seq].extend(getUsefulfactors(spacing))
	factorsByCount = getMostCommonFactors(seqFactors)

	allLikelyKeyLengths = []
	for twoIntTuple in factorsByCount:
		allLikelyKeyLengths.append(twoIntTuple[0])

	return allLikelyKeyLengths

def getNthSubkeysLetters(nth, keyLength, message):
	# Returns every nth letter for each keyLength set of letters in text.
	# E.g. getNthSubkeysLetters(1, 3, 'ABCABCABC') returns 'AAA'
	#      getNthSubkeysLetters(2, 3, 'ABCABCABC') returns 'BBB'
	#      getNthSubkeysLetters(3, 3, 'ABCABCABC') returns 'CCC'
	#      getNthSubkeysLetters(1, 5, 'ABCDEFGHI') returns 'AF'
	# Use a regular expression to remove non-letters from the message:
	message = NONLETTERS_PATTERN.sub('', message.upper())

	i = nth - 1
	letters = []
	while i < len(message):
		letters.append(message[i])
		i += keyLength

	return ''.join(letters)

def attemptHackWithKeyLength(ciphertext, mostLikelyKeyLength):
	# Determine the most likely letters for each letter in the key:
	ciphertextUp = ciphertext.upper()
	# allFreqScores is a list of mostLikelyKeyLength number of lists.
	# These inner lists are the freqScores lists:
	allFreqScores = []
	for nth in range(1, mostLikelyKeyLength + 1):
		nthLetters = getNthSubkeysLetters(nth, mostLikelyKeyLength, ciphertextUp)

		# freqScores is a list of tuples like
		# [(<letter>, <Eng. Freq. match score>), ... ]
		# List is sorted by match score. Higher score means better match.
		# See the englishFreqMatchScore() comments in freqAnalysis.py.
		freqScores = []
		for possibleKey in LETTERS:
			decryptedText = vigenereCipher.decryptMessage(possibleKey, nthLetters)
			keyAndFreqMatchTuple = (possibleKey, freqAnalysis.englishFreqMatchScore(decryptedText))
			freqScores.append(keyAndFreqMatchTuple)
		# Sort by match score:
		freqScores.sort(key=getItemAtIndexOne, reverse=True)
		allFreqScores.append(freqScores[:NUM_MOST_FREQ_LETTERS])

	if not SILENT_MODE:
		for i in range(len(allFreqScores)):
		# Use i + 1 so the first letter is not called the "0th" letter:
			print('Possible letters for letter %s of the key: ' % (i + 1), end='')
			for freqScore in allFreqScores[i]:
				print('%s ' % freqScore[0], end='')
			print() # Print a newline.

	# Try every combination of the most likely letters for each position
	# in the key:
	for indexes in itertools.product(range(NUM_MOST_FREQ_LETTERS), repeat=mostLikelyKeyLength):
		# Create a possible key from the letters in allFreqScores:
		possibleKey = ''
		for i in range(mostLikelyKeyLength):
			possibleKey += allFreqScores[i][indexes[i]][0]

		if not SILENT_MODE:
			print('Attempting with key: %s' % (possibleKey))

		decryptedText = vigenereCipher.decryptMessage(possibleKey, ciphertextUp)

		if detectEnglish.isEnglish(decryptedText):
		# Set the hacked ciphertext to the original casing:
			origCase = []
			for i in range(len(ciphertext)):
				if ciphertext[i].isupper():
					origCase.append(decryptedText[i].upper())
				else:
					origCase.append(decryptedText[i].lower())
			decryptedText = ''.join(origCase)

		# Check with user to see if the key has been found:
			print('Possible encryption hack with key %s:' % (possibleKey))
			print(decryptedText[:200]) # Only show first 200 characters.
			print()
			
			return decryptedText

	# No English-looking decryption found, so return None:
	return None

def hackVigenere(ciphertext):
     # First, we need to do Kasiski examination to figure out what the
     # length of the ciphertext's encryption key is:
     allLikelyKeyLengths = kasiskiExamination(ciphertext)
     if not SILENT_MODE:
         keyLengthStr = ''
         for keyLength in allLikelyKeyLengths:
             keyLengthStr += '%s ' % (keyLength)
         print('Kasiski examination results say the most likely key lengths are: ' + keyLengthStr + '\n')
     hackedMessage = None
     for keyLength in allLikelyKeyLengths:
         if not SILENT_MODE:
             print('Attempting hack with key length %s (%s possible keys)...'
                   % (keyLength, NUM_MOST_FREQ_LETTERS ** keyLength))
         hackedMessage = attemptHackWithKeyLength(ciphertext, keyLength)
         if hackedMessage != None:
             break

     # If none of the key lengths found using Kasiski examination
     # worked, start brute-forcing through key lengths:
     if hackedMessage == None:
         if not SILENT_MODE:
             print('Unable to hack message with likely key length(s). Brute-forcing key length...')
         for keyLength in range(1, MAX_KEY_LENGTH + 1):
             # Don't recheck key lengths already tried from Kasiski:
             if keyLength not in allLikelyKeyLengths:
                 if not SILENT_MODE:
                     print('Attempting hack with key length %s (%s possible keys)...' % (keyLength, NUM_MOST_FREQ_LETTERS ** keyLength))
                 hackedMessage = attemptHackWithKeyLength(ciphertext,
                       keyLength)
                 if hackedMessage != None:
                     break
     return hackedMessage

if __name__ == main():
	main()