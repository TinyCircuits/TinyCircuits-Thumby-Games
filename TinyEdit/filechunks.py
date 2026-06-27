from os import stat, mkdir, listdir, remove

class ChunkProblem( Exception ):
    pass

class Line:
    def __init__( self, text ):
        self.setText( text )

    def getText( self, position ):
        if position > self.size:
            return '<'
        if position > 0:
            result = '<'
        else:
            result=' '
        maxRight = position + 10
        result += self.text[ position : min( maxRight, self.size ) ]
        if maxRight < self.size:
            result = result + '>'
        return result

    def setText( self, newText ):
        self.text = newText[ 0 : -1 ] if newText.endswith( '\n' ) else newText
        self.size = len( self.text )

class FileChunk:
    CHUNK_PATH = "/Games/TinyEdit/tmp"

    def __init__( self, lines, startIndex ):
        self.lines = [ Line( line ) for line in lines ]
        self.name = None
        self.startIndex = startIndex
        self.lnCount = len( lines )

    def setName( self, name ):
        self.name = str( name )

    def getPath( self ):
        if not self.name:
            raise ChunkProblem( 'Chunk path not set' )
        return FileChunk.CHUNK_PATH + '/' + self.name + '.chunk'

    def write( self ):
        # Possible optimisation: don't write unless content changed since last write
        with open( self.getPath(), 'w', encoding = 'utf-8' ) as f:
            for line in self.lines:
                f.write( line.text )
                f.write( '\n' )

    def read( self ):
        self.lines = []
        with open( self.getPath(), 'r', encoding = 'utf-8' ) as f:
            for line in f:
                self.lines.append( Line( line ) )
        self.lnCount = len( self.lines )
        return self.lines

    def dropContent( self ):
        self.lines = []

    def writeDrop( self ):
        self.write()
        self.dropContent()

    def lineCount( self ):
        return self.lnCount

    def lastIndex( self ):
        return self.startIndex + self.lnCount - 1

    def includes( self, index ):
        return index >= self.startIndex and index < self.startIndex + self.lineCount()

    def nearTop( self, index ):
        return self.startIndex > 0 and index - 2 < self.startIndex

    def nearBottom( self, index ):
        return index + 2 > self.lastIndex()

    def includesX( self, index ):
        if not self.includes( index ):
            raise ChunkProblem( "Requested index " + str( index ) + " not in range " + str( self.startIndex ) + " to " + str( self.lastIndex() ) )

    def getLine( self, index ):
        self.includesX( index )
        return self.lines[ index - self.startIndex ]

    def replaceLine( self, index, newText ):
        self.includesX( index )
        self.lines[ index - self.startIndex ].setText( newText )
        self.write()

    def writeTo( self, f ):
        empty = 0 == len( self.lines )
        if empty:
            self.read()
        for line in self.lines:
            f.write( line.text )
            f.write( '\n' )
        if empty:
            self.dropContent()

    def duplicateLine( self, index ):
        self.includesX( index )
        offset = index - self.startIndex
        self.lines.insert( offset, Line( self.lines[ offset ].text ) )
        self.lnCount = len( self.lines )
        self.write()

    def deleteLine( self, index ):
        self.includesX( index )
        offset = index - self.startIndex
        deletedLine = self.lines.pop( offset )
        self.lnCount = len( self.lines )
        self.write()
        return deletedLine.text

    def appendLine( self, text ):
        self.lines.append( Line( text ) )
        self.lnCount = len( self.lines )
        self.write()

    def insertLine( self, index, text ):
        self.lines.insert( index - self.startIndex, Line( text ) )
        self.lnCount = len( self.lines )
        self.write()

    def adjustIndexes( self, adjustment ):
        self.startIndex += adjustment

    def moveUp( self, index ):
        self.includesX( index )
        if index == self.startIndex:
            raise ChunkProblem( "Can't move first line of chunk up" )
        offset = index - self.startIndex
        self.lines.insert( offset - 1, self.lines.pop( offset ) )
        self.write()

    def moveDown( self, index ):
        self.includesX( index )
        if index == self.lastIndex():
            raise ChunkProblem( "Can't move last line of chunk down" )
        offset = index - self.startIndex
        self.lines.insert( offset + 1, self.lines.pop( offset ) )
        self.write()

    def close( self ):
        self.lines = []
        remove( self.getPath() )

class FileChunks:
    def __init__( self, fileName ):
        try:
            x = stat( FileChunk.CHUNK_PATH )
            if x[ 0 ] & 0x4000 != 0x4000: # if not a dir
                raise ChunkProblem( "Temp dir " + FileChunk.CHUNK_PATH + " exists but is not a directory: " + str( x ) )
        except Exception as x:
            mkdir( FileChunk.CHUNK_PATH )
        def newChunk( chunks, lines, lineIndex, chunkIndex ):
            chunk = FileChunk( lines, lineIndex )
            chunks.chunkList.append( chunk )
            chunk.setName( chunkIndex )
            chunk.write()
            if chunks.topChunkIndex < 0:
                chunks.topChunkIndex = chunkIndex
            elif chunks.bottomChunkIndex < 0:
                chunks.bottomChunkIndex = chunkIndex
            else:
                chunk.dropContent()
        self.chunkList = []
        chunkIndex = 0
        self.topChunkIndex = -1
        self.bottomChunkIndex = -1
        thisChunkLines = []
        thisChunkSize = 0
        if fileName:
            with open( fileName, encoding = "utf-8" ) as f:
                fileLineIndex = 0
                chunkStartLineIndex = 0
                for line in f:
                    thisChunkLines.append( line )
                    thisChunkSize += len( line )
                    if thisChunkSize >= 2048 and len( thisChunkLines ) >= 10:
                        newChunk( self, thisChunkLines, chunkStartLineIndex, chunkIndex )
                        thisChunkLines = []
                        thisChunkSize = 0
                        chunkStartLineIndex = fileLineIndex + 1
                        chunkIndex += 1
                    fileLineIndex += 1
        if thisChunkSize:
            newChunk( self, thisChunkLines, chunkStartLineIndex, chunkIndex )
        if len( self.chunkList ) == 0:
            newChunk( self, [], 0, 0 )
        self.currentLineIndex = 0

    def getChunkX( self, index ):
        return self.chunkList[ self.getChunkIndexX( index ) ]

    def getChunkIndexX( self, index ):
        if self.topChunkIndex >= 0 and self.chunkList[ self.topChunkIndex ].includes( index ):
            return self.topChunkIndex
        if self.bottomChunkIndex >= 0 and self.chunkList[ self.bottomChunkIndex ].includes( index ):
            return self.bottomChunkIndex
        if index == 0 and len( self.chunkList ) == 1 and self.topChunkIndex == 0 and self.chunkList[ 0 ].lineCount() == 0:
            return 0
        topChunk = self.chunkList[ self.topChunkIndex ]
        bottomChunk = self.chunkList[ self.bottomChunkIndex ]
        raise ChunkProblem( 'Line index ' + str( index ) + ' not in top (' + str( topChunk.startIndex ) + ',' + str( topChunk.lastIndex() ) + ') or bottom (' + str( bottomChunk.startIndex ) + ',' + str( bottomChunk.lastIndex() ) + ') chunk.' )

    def getLine( self, index ):
        return self.getChunkX( index ).getLine( index )

    def lineCount( self ):
        return sum( [ chunk.lineCount() for chunk in self.chunkList ] )

    def getCurrentLineIndex( self ):
        return self.currentLineIndex

    def getCurrentLine( self ):
        return self.getLine( self.currentLineIndex )

    def replaceCurrentLine( self, newText ):
        self.getChunkX( self.currentLineIndex ).replaceLine( self.currentLineIndex, newText )

    def duplicateCurrentLine( self ):
        self.getChunkX( self.currentLineIndex ).duplicateLine( self.currentLineIndex )
        for chunk in self.chunkList[ self.getChunkIndexX( self.currentLineIndex ) + 1 : ]:
            chunk.adjustIndexes( 1 )

    def insertLine( self, text ):
        self.getChunkX( self.currentLineIndex ).insertLine( self.currentLineIndex, text )
        for chunk in self.chunkList[ self.getChunkIndexX( self.currentLineIndex ) + 1 : ]:
            chunk.adjustIndexes( 1 )

    def deleteCurrentLine( self ):
        nextChunkIndex = self.getChunkIndexX( self.currentLineIndex ) + 1
        self.getChunkX( self.currentLineIndex ).deleteLine( self.currentLineIndex )
        for chunk in self.chunkList[ nextChunkIndex : ]:
            chunk.adjustIndexes( -1 )
        self.maybeMergeX()

    def maybeMergeX( self ):
        if len( self.chunkList ) == 1:
            return
        thisChunk = self.getChunkX( self.currentLineIndex )
        if len( thisChunk.lines ) >= 10:
            return
        # I *think* we could just drop the content here without writing...
        self.chunkList[ self.topChunkIndex ].writeDrop()
        self.chunkList[ self.bottomChunkIndex ].writeDrop()
        thisChunkIndex = self.getChunkIndexX( self.currentLineIndex )
        if thisChunkIndex == 0:
            chunkToGrowIndex = 0
            newTopIndex = 0
            newBottomIndex = 1
        elif thisChunkIndex == len( self.chunkList ) - 1:
            chunkToGrowIndex = thisChunkIndex - 1
            newTopIndex = chunkToGrowIndex - 1
        else:
            lenAbove = self.chunkList[ thisChunkIndex - 1 ].lnCount
            lenBelow = self.chunkList[ thisChunkIndex + 1 ].lnCount
            if lenAbove < lenBelow:
                chunkToGrowIndex = thisChunkIndex - 1
            else:
                chunkToGrowIndex = thisChunkIndex
            newTopIndex = chunkToGrowIndex
        chunkToGrow = self.chunkList[ chunkToGrowIndex ]
        self.chunkList[ chunkToGrowIndex     ].read()
        self.chunkList[ chunkToGrowIndex + 1 ].read()
        for line in self.chunkList[ chunkToGrowIndex + 1 ].lines:
            chunkToGrow.appendLine( line.text )
        del( self.chunkList[ chunkToGrowIndex + 1 ] )
        self.chunkList[ chunkToGrowIndex ].writeDrop()
        self.topChunkIndex = newTopIndex
        self.bottomChunkIndex = newTopIndex + 1
        self.chunkList[ self.topChunkIndex ].read()
        self.chunkList[ self.bottomChunkIndex ].read()

    def moveUp( self ):
        index = self.currentLineIndex
        chunk = self.getChunkX( index )
        if self.bottomChunkIndex == self.getChunkIndexX( index ) and index == chunk.startIndex:
            #move line between chunks
            textToMoveUp = chunk.deleteLine( index )
            topChunk = self.chunkList[ self.topChunkIndex ]
            textToMoveDown = topChunk.deleteLine( index - 1 )
            topChunk.appendLine( textToMoveUp )
            chunk.insertLine( index, textToMoveDown )
        else:
            #move line within chunk
            chunk.moveUp( index )
        self.setCurrentLineIndex( index - 1 )

    def moveDown( self ):
        index = self.currentLineIndex
        chunk = self.getChunkX( index )
        if self.topChunkIndex == self.getChunkIndexX( index ) and index == chunk.lastIndex():
            #move line between chunks
            textToMoveDown = chunk.deleteLine( index )
            bottomChunk = self.chunkList[ self.bottomChunkIndex ]
            textToMoveUp = bottomChunk.deleteLine( index + 1 )
            chunk.appendLine( textToMoveUp )
            bottomChunk.insertLine( index + 1, textToMoveDown )
        else:
            #move line within chunk
            chunk.moveDown( index )
        self.setCurrentLineIndex( index + 1 )

    def setCurrentLineIndex( self, index ):
        self.currentLineIndex = index
        if self.topChunkIndex >= 0 and self.chunkList[ self.topChunkIndex ].nearTop( index ):
            # Probably the prev chunk, but not if it's a big jump
            # So get rid of both chunks and read new ones
            # Possible optimisation: decide if we can keep one chunk
            self.chunkList[ self.topChunkIndex ].writeDrop()
            self.chunkList[ self.bottomChunkIndex ].writeDrop()
            while True:
                self.topChunkIndex -= 1
                isFirstChunk = self.topChunkIndex == 0
                chunkEndsBeforeIndex = self.chunkList[ self.topChunkIndex ].lastIndex() < index
                if isFirstChunk or chunkEndsBeforeIndex:
                    break;
            self.bottomChunkIndex = self.topChunkIndex + 1
            self.chunkList[ self.topChunkIndex ].read()
            self.chunkList[ self.bottomChunkIndex ].read()
        elif self.bottomChunkIndex >= 0 and self.bottomChunkIndex + 1 < len( self.chunkList ) and self.chunkList[ self.bottomChunkIndex ].nearBottom( index ):
            # Probably the next chunk, but not if it's a big jump
            # So get rid of both chunks and read new ones
            # Possible optimisation: decide if we can keep one chunk
            self.chunkList[ self.topChunkIndex ].writeDrop()
            self.chunkList[ self.bottomChunkIndex ].writeDrop()
            while True:
                self.bottomChunkIndex += 1
                isLastChunk = self.bottomChunkIndex == len( self.chunkList ) - 1
                chunkStartsAfterIndex = self.chunkList[ self.bottomChunkIndex ].startIndex > index
                if isLastChunk or chunkStartsAfterIndex:
                    break;
            self.topChunkIndex = self.bottomChunkIndex - 1
            self.chunkList[ self.topChunkIndex ].read()
            self.chunkList[ self.bottomChunkIndex ].read()

    def writeTo( self, f ):
        for chunk in self.chunkList:
            chunk.writeTo( f )

    def close( self ):
        for chunk in self.chunkList:
            chunk.close()
        self.chunkList = []
        for f in listdir( FileChunk.CHUNK_PATH ):
            remove( FileChunk.CHUNK_PATH + '/' + f )
