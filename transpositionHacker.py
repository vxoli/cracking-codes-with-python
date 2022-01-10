# Transposition Cipher Hacker
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)

import detectEnglish, transpositionDecrypt

def main():
    myMessage = """AaKoosoeDe5 b5sn ma reno ora'lhlrrceey e  enlh na  indeit n uhoretrm au ieu v er Ne2 gmanw,forwnlbsya apor tE.no euarisfatt  e mealefedhsppmgAnlnoe(c -or)alat r lw o eb  nglom,Ain one dtes ilhetcdba. t tg eturmudg,tfl1e1 v  nitiaicynhrCsaemie-sp ncgHt nie cetrgmnoa yc r,ieaa  toesa- e a0m82e1w shcnth  ekh gaecnpeutaaieetgn iodhso d ro hAe snrsfcegrt NCsLc b17m8aEheideikfr aBercaeu thllnrshicwsg etriebruaisss  d iorr."""
    
    hackedMessage = hackTransposition(myMessage)

    if hackedMessage == None:
        print('Failed to hack encryption')
    else:
        print('Decrypted')
        print(hackedMessage)

    return

def hackTransposition(message):
    print('Hacking')

    for key in range(1, len(message)):
        print('Trying key: %s' % (key))
        decryptedText = transpositionDecrypt.decryptMessage(key, message)

        if detectEnglish.isEnglish(decryptedText):
            print()
            print('Possible hack:')
            print('Key %s: %s' % (key, decryptedText[:100]))
            return decryptedText

    return None

if __name__ == '__main__':
    main()

