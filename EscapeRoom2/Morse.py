def decodeMorse( morse ):
    result = ""
    for letter in morse.split( ' ' ):
        if   ''      == letter: result += ' '
        elif '.-'    == letter: result += 'A'
        elif '-...'  == letter: result += 'B'
        elif '-.-.'  == letter: result += 'C'
        elif '-..'   == letter: result += 'D'
        elif '.'     == letter: result += 'E'
        elif '..-.'  == letter: result += 'F'
        elif '--.'   == letter: result += 'G'
        elif '....'  == letter: result += 'H'
        elif '..'    == letter: result += 'I'
        elif '.---'  == letter: result += 'J'
        elif '-.-'   == letter: result += 'K'
        elif '.-..'  == letter: result += 'L'
        elif '--'    == letter: result += 'M'
        elif '-.'    == letter: result += 'N'
        elif '---'   == letter: result += 'O'
        elif '.--.'  == letter: result += 'P'
        elif '--.-'  == letter: result += 'Q'
        elif '.-.'   == letter: result += 'R'
        elif '...'   == letter: result += 'S'
        elif '-'     == letter: result += 'T'
        elif '..-'   == letter: result += 'U'
        elif '...-'  == letter: result += 'V'
        elif '.--'   == letter: result += 'W'
        elif '-..-'  == letter: result += 'X'
        elif '-.--'  == letter: result += 'Y'
        elif '--..'  == letter: result += 'Z'
        elif '-----' == letter: result += '0'
        elif '.----' == letter: result += '1'
        elif '..---' == letter: result += '2'
        elif '...--' == letter: result += '3'
        elif '....-' == letter: result += '4'
        elif '.....' == letter: result += '5'
        elif '-....' == letter: result += '6'
        elif '--...' == letter: result += '7'
        elif '---..' == letter: result += '8'
        elif '----.' == letter: result += '9'
        else: result += '?'
    return result

def parseMorse( timings ):
    timingsLen = len( timings )
    if timingsLen % 2 == 0:
        raise Exception( 'Expected odd number of timings.' )
    if timingsLen < 3 == 0:
        raise Exception( 'Expected at least three timings.' )

    morse = ""

    #At first, key up
    #    Time this lasts is irrelevant
    #Then key down for count of n1
    #    We don't know if this is a dit or a dah!
    beepLen = timings[ 1 ]

    # If that was the only beep, we have to guess dit or dah from absolute length
    if timingsLen == 3:
        if beepLen <= 20:
            morse = '.'
        else:
            morse = '-'
    else:
        #Then key up for count of n2
        #    If somewhat shorter than n1, it's a gaplet, and n1 was a dah
        #    If similar to n1, it's a gaplet, and n1 was a dit
        #    If somewhat longer than n1, this is a letter gap
        #        Infer whether n1 was dit or dah from the ratio of lengths
        #    If much longer than n1, this is a word gap
        #        Infer whether n1 was dit or dah from the ratio of lengths
        ratio = beepLen / timings [ 2 ]
        comparison = int( ratio + 0.6666 )
        if comparison == 1:
            morse += '.'
        elif comparison > 1:
            morse += '-'
        else:
            if ratio < 0.4:
                morse += '.'
            else:
                morse += '-'
            gapRatio = int( ratio * 10 + 0.6666 )
            if gapRatio >= 3:
                morse += ' '
            else:
                morse += '  '
        if morse[ 0 ] == '.':
            ditLen = beepLen
        else:
            ditLen = beepLen / 3

    index = 3
    while index < timingsLen:
        #Then key down for n3
        #    We know the lengths so we can choose dit or dah
        beepLen = timings[ index ]
        ratio = beepLen / ditLen
        if ratio < 2:
            morse += '.'
        else:
            morse += '-'
        index += 1

        #Then key up for count of n4
        #    We know the lengths so we can choose gaplet or letter gap
        gapLen = timings[ index ]
        ratio = gapLen / ditLen
        if ratio < 3:
            pass # gaplet
        elif ratio <= 4.5:
            morse += ' '
        else:
            morse += '  '
        index += 1

    morse = morse.strip()
    print( morse )
    return decodeMorse( morse )
