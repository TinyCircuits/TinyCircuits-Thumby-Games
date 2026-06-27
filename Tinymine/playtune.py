from thumbyAudio import audio
from time import sleep

class Note:
    def __init__( self, pitch, length, flags ):
        self.pitch = int( pitch ) # 0 = C4, one ledger line down on treble clef
        self.length = int( length ) # 16 = crotchet
        self.flags = flags # dotted, pizzicato, etc

    @classmethod
    def parse( cls, initStr ):
        initElems = initStr.split( '|' )
        return cls( initElems[ 0 ], initElems[ 1 ], initElems[ 2 ] )

    def play( self, tempo ):
        totalMillis = ( 3750.0 / tempo ) * self.length
        if '.' in self.flags:
            totalMillis = totalMillis * 1.5
        if not 'r' in self.flags:
            if 'z' in self.flags:
                soundMillis = totalMillis * 1.1
            elif 's' in self.flags:
                soundMillis = totalMillis * 0.75
            else:
                soundMillis = totalMillis * 0.95
            audio.play(
                int(
                    261.63 *
                        pow(
                            1.059463094359,
                            self.pitch
                        )
                ),
                int( soundMillis )
            )
        sleep( totalMillis / 1000 )

class Tune:
    def __init__( self, initString ):
        self.notes = []
        parts = initString.split( ':' )
        if len( parts ) == 1:
            self.tempo = 240
        else:
            self.tempo = int( parts[ 0 ] )
        for noteStr in parts[ -1 ].split( ',' ):
            self.notes.append( Note.parse( noteStr ) )

    def play( self ):
        for note in self.notes:
            note.play( self.tempo )
