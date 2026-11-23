
#============================================
# Imports and paths
#============================================
import thumby
import math
import gc
import time

try:
    import random
except ImportError:
    random = None


#============================================
# Configuration constants
#============================================
GAME_DIRECTORY = "/Games/MaidDash2"
HIGHSCORE_SAVE_NAME = "MaidDash2"
HIGHSCORE_SAVE_KEY = "highscores"
GAME_VERSION = "1.0.0-rc.1"

# Sound effects: (frequency in Hz, duration in milliseconds).
SOUND_READY = (659, 100)
SOUND_START = (784, 200)
SOUND_JUMP = (500, 50)
SOUND_AIR_JUMP = (500, 70)
SOUND_FINISHED = (220, 120)
SOUND_CURSOR = (880, 60)
SOUND_CONFIRM = (1320, 100)


def playSound(sound):
    thumby.audio.play(sound[0], sound[1])


GAME_CONFIG = {
    "initialScore": 0,
    "display": {"fps": 30},
    "intro": {"width": 72, "height": 40, "durationFrames": 60},
    "game": {
        "score": {
            "x": 4,
            "y": 1,
            "font": {
                "filePath": "/lib/font5x7.bin",
                "width": 5,
                "height": 7,
                "space": 1,
            },
        },
    },
    "highscore": {
        "font": {"filePath": "/lib/font5x7.bin", "width": 5, "height": 7, "space": 1},
        "rank1": {"x": 30, "y": 12},
        "rank2": {"x": 30, "y": 21},
        "rank3": {"x": 30, "y": 30},
    },
    "result": {
        "score": {
            "x": 14,
            "y": 18,
            "font": {
                "filePath": "/lib/font5x7.bin",
                "width": 5,
                "height": 7,
                "space": 1,
            },
        },
    },
    "player": {
        "width": 12,
        "height": 12,
        "frameCount": 3,
        "startX": 5,
        "startY": 25,
        "collision": {"x": 6, "y": 11, "width": 5, "height": 1},
        "jumpHeightPixels": 15.0,
        "doubleJumpHeightPixels": 5.4,
        "jumpHoverTimeSeconds": 0.3,
        "gravity": 333.333333,
        "maxJumps": 2,
    },
    "platform": {
        "height": 3,
        "start": {"x": 0, "y": 37, "width": 48, "height": 3},
        "generation": {
            "randomSeed": 17,
            "randomizeSeed": True,
            "minY": 12,
            "maxY": 36,
            "gapMargin": 3,
            "minGapPixels": 3,
            "maxAttempts": 8,
        },
    },
    "stageLevels": [
        {"level": 1, "startScore": 0, "scrollIntervalSeconds": 0.1, "platformWidth": 13, "heightDifferenceRate": 42, "horizontalGapRate": 100},
        {"level": 2, "startScore": 4, "scrollIntervalSeconds": 0.095, "platformWidth": 12, "heightDifferenceRate": 42, "horizontalGapRate": 100},
        {"level": 3, "startScore": 9, "scrollIntervalSeconds": 0.09, "platformWidth": 12, "heightDifferenceRate": 50, "horizontalGapRate": 100},
        {"level": 4, "startScore": 15, "scrollIntervalSeconds": 0.085, "platformWidth": 11, "heightDifferenceRate": 50, "horizontalGapRate": 100},
        {"level": 5, "startScore": 25, "scrollIntervalSeconds": 0.08, "platformWidth": 11, "heightDifferenceRate": 58, "horizontalGapRate": 100},
        {"level": 6, "startScore": 40, "scrollIntervalSeconds": 0.075, "platformWidth": 10, "heightDifferenceRate": 58, "horizontalGapRate": 100},
        {"level": 7, "startScore": 60, "scrollIntervalSeconds": 0.07, "platformWidth": 10, "heightDifferenceRate": 67, "horizontalGapRate": 100},
        {"level": 8, "startScore": 85, "scrollIntervalSeconds": 0.065, "platformWidth": 9, "heightDifferenceRate": 67, "horizontalGapRate": 100},
        {"level": 9, "startScore": 110, "scrollIntervalSeconds": 0.06, "platformWidth": 9, "heightDifferenceRate": 75, "horizontalGapRate": 100},
        {"level": 10, "startScore": 140, "scrollIntervalSeconds": 0.055, "platformWidth": 8, "heightDifferenceRate": 75, "horizontalGapRate": 100},
        {"level": 11, "startScore": 175, "scrollIntervalSeconds": 0.05, "platformWidth": 8, "heightDifferenceRate": 83, "horizontalGapRate": 100},
        {"level": 12, "startScore": 210, "scrollIntervalSeconds": 0.045, "platformWidth": 7, "heightDifferenceRate": 83, "horizontalGapRate": 100},
        {"level": 13, "startScore": 250, "scrollIntervalSeconds": 0.04, "platformWidth": 7, "heightDifferenceRate": 92, "horizontalGapRate": 100},
        {"level": 14, "startScore": 300, "scrollIntervalSeconds": 0.035, "platformWidth": 6, "heightDifferenceRate": 92, "horizontalGapRate": 100},
        {"level": 15, "startScore": 400, "scrollIntervalSeconds": 0.03, "platformWidth": 6, "heightDifferenceRate": 100, "horizontalGapRate": 100},
    ],
}

INITIAL_SCORE = GAME_CONFIG["initialScore"]
DISPLAY_FPS = GAME_CONFIG["display"]["fps"]
DELTA_TIME_SECONDS = 1.0 / DISPLAY_FPS
INTRO_WIDTH = GAME_CONFIG["intro"]["width"]
INTRO_HEIGHT = GAME_CONFIG["intro"]["height"]
INTRO_FRAMES = GAME_CONFIG["intro"]["durationFrames"]
gameScoreDisplayConfig = GAME_CONFIG["game"]["score"]
GAME_SCORE_POSITION = gameScoreDisplayConfig
GAME_SCORE_FONT_CONFIG = gameScoreDisplayConfig["font"]
highscoreDisplayConfig = GAME_CONFIG["highscore"]
HIGHSCORE_FONT_CONFIG = highscoreDisplayConfig["font"]
HIGHSCORE_RANK_POSITIONS = (
    highscoreDisplayConfig["rank1"],
    highscoreDisplayConfig["rank2"],
    highscoreDisplayConfig["rank3"]
)
RESULT_SCORE_POSITION = GAME_CONFIG["result"]["score"]
RESULT_SCORE_FONT_CONFIG = RESULT_SCORE_POSITION["font"]

PLAYER_WIDTH = GAME_CONFIG["player"]["width"]
PLAYER_HEIGHT = GAME_CONFIG["player"]["height"]
PLAYER_FRAME_COUNT = GAME_CONFIG["player"]["frameCount"]
PLAYER_START_X = GAME_CONFIG["player"]["startX"]
PLAYER_START_Y = GAME_CONFIG["player"]["startY"]
playerCollisionConfig = GAME_CONFIG["player"]["collision"]
collisionOffsetX = playerCollisionConfig["x"]
collisionOffsetY = playerCollisionConfig["y"]
collisionWidth = playerCollisionConfig["width"]
collisionHeight = playerCollisionConfig["height"]
jumpHeightPixels = GAME_CONFIG["player"]["jumpHeightPixels"]
doubleJumpHeightPixels = GAME_CONFIG["player"]["doubleJumpHeightPixels"]
jumpHoverTimeSeconds = GAME_CONFIG["player"]["jumpHoverTimeSeconds"]
gravity = GAME_CONFIG["player"]["gravity"]
jumpPower = -math.sqrt(2 * gravity * jumpHeightPixels)
doubleJumpPower = -math.sqrt(2 * gravity * doubleJumpHeightPixels)
maxJumps = GAME_CONFIG["player"]["maxJumps"]

platformHeight = GAME_CONFIG["platform"]["height"]
platformGenerationConfig = GAME_CONFIG["platform"]["generation"]
platformRandomSeed = platformGenerationConfig["randomSeed"]
platformRandomizeSeed = platformGenerationConfig["randomizeSeed"]
platformMinY = platformGenerationConfig["minY"]
platformMaxY = platformGenerationConfig["maxY"]
platformGapMargin = platformGenerationConfig["gapMargin"]
platformMinGapPixels = platformGenerationConfig["minGapPixels"]
platformGenerationAttempts = platformGenerationConfig["maxAttempts"]
startPlatformConfig = GAME_CONFIG["platform"]["start"]

STAGE_LEVEL_CONFIGS = GAME_CONFIG["stageLevels"]
STAGE_LEVEL_START_SCORES = [
    levelConfig["startScore"] for levelConfig in STAGE_LEVEL_CONFIGS
]
STAGE_SCROLL_INTERVAL_SECONDS = [
    levelConfig["scrollIntervalSeconds"] for levelConfig in STAGE_LEVEL_CONFIGS
]
MAX_STAGE_LEVEL = len(STAGE_LEVEL_CONFIGS)


#============================================
# Configuration validation
#============================================
def validateStageLevelConfigs():
    for levelConfig in STAGE_LEVEL_CONFIGS:
        heightRate = levelConfig["heightDifferenceRate"]
        horizontalGapRate = levelConfig["horizontalGapRate"]
        platformWidthForLevel = levelConfig["platformWidth"]
        if heightRate < 0 or heightRate > 100:
            raise ValueError("heightDifferenceRate must be between 0 and 100")
        if horizontalGapRate < 0 or horizontalGapRate > 100:
            raise ValueError("horizontalGapRate must be between 0 and 100")
        if platformWidthForLevel <= 0:
            raise ValueError("platformWidth must be greater than 0")


def validateScoreConfig():
    if INITIAL_SCORE < 0:
        raise ValueError("initialScore must be non-negative")


def validatePlatformGenerationConfig():
    if type(platformRandomizeSeed) is not bool:
        raise ValueError("randomizeSeed must be a boolean")
    if type(platformRandomSeed) is not int or platformRandomSeed < 0:
        raise ValueError("randomSeed must be a non-negative integer")
    if type(platformMinGapPixels) is not int or platformMinGapPixels < 0:
        raise ValueError("minGapPixels must be a non-negative integer")


def validatePlayerCollisionConfig():
    if collisionOffsetX < 0 or collisionOffsetY < 0:
        raise ValueError("collision offsets must be non-negative")
    if collisionWidth <= 0 or collisionHeight <= 0:
        raise ValueError("collision dimensions must be greater than 0")
    if collisionOffsetX + collisionWidth > PLAYER_WIDTH:
        raise ValueError("collision rectangle exceeds player width")
    if collisionOffsetY + collisionHeight > PLAYER_HEIGHT:
        raise ValueError("collision rectangle exceeds player height")


def validateJumpPhysicsConfig():
    if jumpHeightPixels <= 0 or doubleJumpHeightPixels <= 0:
        raise ValueError("jump heights must be greater than 0")
    if jumpHoverTimeSeconds < 0:
        raise ValueError("jump timing values are invalid")
    if gravity <= 0:
        raise ValueError("gravity must be greater than 0")


def validateFontConfig(fontConfig, displayName):
    fontFilePath = fontConfig["filePath"]
    fontWidth = fontConfig["width"]
    fontHeight = fontConfig["height"]
    fontSpace = fontConfig["space"]
    if type(fontFilePath) is not str or len(fontFilePath) == 0:
        raise ValueError(displayName + " font file path must be non-empty")
    if type(fontWidth) is not int or fontWidth <= 0:
        raise ValueError(displayName + " font width must be greater than 0")
    if type(fontHeight) is not int or fontHeight <= 0:
        raise ValueError(displayName + " font height must be greater than 0")
    if type(fontSpace) is not int or fontSpace < 0:
        raise ValueError(displayName + " font space must be non-negative")


def getTextDisplayWidth(fontConfig, characterCount):
    return (
        fontConfig["width"] * characterCount
        + fontConfig["space"] * (characterCount - 1)
    )


def validateScoreTextPosition(position, fontConfig, displayName):
    positionX = position["x"]
    positionY = position["y"]
    if type(positionX) is not int:
        raise ValueError(displayName + " X position must be an integer")
    if type(positionY) is not int:
        raise ValueError(displayName + " Y position must be an integer")
    if positionX < 0 or positionX + getTextDisplayWidth(fontConfig, 3) > INTRO_WIDTH:
        raise ValueError(displayName + " X position exceeds display width")
    if positionY < 0 or positionY + fontConfig["height"] > INTRO_HEIGHT:
        raise ValueError(displayName + " Y position exceeds display height")


def validateScoreDisplayConfigs():
    validateFontConfig(GAME_SCORE_FONT_CONFIG, "game score")
    validateFontConfig(HIGHSCORE_FONT_CONFIG, "highscore")
    validateFontConfig(RESULT_SCORE_FONT_CONFIG, "result score")
    validateScoreTextPosition(
        GAME_SCORE_POSITION,
        GAME_SCORE_FONT_CONFIG,
        "game score"
    )
    for rankPosition in HIGHSCORE_RANK_POSITIONS:
        validateScoreTextPosition(
            rankPosition,
            HIGHSCORE_FONT_CONFIG,
            "highscore"
        )
    validateScoreTextPosition(
        RESULT_SCORE_POSITION,
        RESULT_SCORE_FONT_CONFIG,
        "result score"
    )


def setDisplayFont(fontConfig):
    thumby.display.setFont(
        fontConfig["filePath"],
        fontConfig["width"],
        fontConfig["height"],
        fontConfig["space"]
    )


validateStageLevelConfigs()
validateScoreConfig()
validatePlatformGenerationConfig()
validatePlayerCollisionConfig()
validateJumpPhysicsConfig()
validateScoreDisplayConfigs()


#============================================
# Highscore persistence
#============================================
def normalizeHighscores(scores):
    if not isinstance(scores, list) or len(scores) != 3:
        return None

    normalizedScores = []
    for value in scores:
        if type(value) is not int or value < 0 or value > 999:
            return None
        normalizedScores.append(value)

    for index in range(2):
        for nextIndex in range(index + 1, 3):
            if normalizedScores[nextIndex] > normalizedScores[index]:
                temporaryScore = normalizedScores[index]
                normalizedScores[index] = normalizedScores[nextIndex]
                normalizedScores[nextIndex] = temporaryScore
    return normalizedScores


def loadHighscores():
    try:
        thumby.saveData.setName(HIGHSCORE_SAVE_NAME)
        if not thumby.saveData.hasItem(HIGHSCORE_SAVE_KEY):
            return [0, 0, 0]
        normalizedScores = normalizeHighscores(
            thumby.saveData.getItem(HIGHSCORE_SAVE_KEY)
        )
        if normalizedScores is not None:
            return normalizedScores
    except (OSError, ValueError, TypeError, AttributeError):
        pass
    return [0, 0, 0]


def saveHighscores(scores):
    try:
        thumby.saveData.setItem(HIGHSCORE_SAVE_KEY, scores)
        thumby.saveData.save()
        return True
    except (OSError, ValueError, TypeError, AttributeError):
        return False


def recordHighscore(scoreToRecord):
    global highscores

    if scoreToRecord <= highscores[2]:
        return False

    updatedScores = normalizeHighscores([
        scoreToRecord,
        highscores[0],
        highscores[1]
    ])
    if updatedScores is None or not saveHighscores(updatedScores):
        return False

    highscores = updatedScores
    return True


highscores = loadHighscores()

#============================================
# Bitmap and sprite assets
#============================================
# Bitmap data is stored as raw bytes.  Do not use JSON hex strings here:
# parsing every string and then converting it doubles the asset memory during
# startup, which exceeds the heap available on a physical Thumby.
ASSET_PACK_PATH = GAME_DIRECTORY + "/MaidDash2.bin"

# (byte offset, byte count) within MaidDash2.bin. Keep this table in the same
# order as tools/convert_image_data.py's ASSET_ORDER.
ASSET_LAYOUT = {
    "fadeTexture": (0, 1440),
    "fadeTexture_mask": (1440, 1440),
    "titleTransitionImage": (2880, 1800),
    "titleCharacter1": (4680, 720),
    "titleCharacter1_mask": (5400, 720),
    "titleCharacter2": (6120, 1440),
    "titleCharacter2_mask": (7560, 1440),
    "title_electUiStart": (9000, 360),
    "title_electUiStart_mask": (9360, 360),
    "title_electUiScore": (9720, 360),
    "title_electUiScore_mask": (10080, 360),
    "titleBackground": (10440, 360),
    "highscoreBackground": (10800, 360),
    "resultBackground": (11160, 360),
    "resultCharacter": (11520, 720),
    "resultCharacter_mask": (12240, 720),
    "resultSelectUI": (12960, 720),
    "resultSelectUI_mask": (13680, 720),
    "resultTransitionImageInversion": (14400, 1800),
    "highscoreButton": (16200, 720),
    "highscoreButton_mask": (16920, 720),
    "ready": (17640, 360),
    "ready_mask": (18000, 360),
    "start": (18360, 360),
    "start_mask": (18720, 360),
    "finished": (19080, 360),
    "finished_mask": (19440, 360),
    "playerSpriteSheet": (19800, 72),
    "playerMaskSheet": (19872, 72),
    "playerJumpSpriteSheet": (19944, 24),
    "playerJumpMaskSheet": (19968, 24),
    "playerFallSpriteSheet": (19992, 24),
    "playerFallMaskSheet": (20016, 24)
}


def loadBitmapData(assetName):
    assetOffset, byteCount = ASSET_LAYOUT[assetName]
    bitmapData = bytearray(byteCount)
    with open(ASSET_PACK_PATH, "rb") as bitmapFile:
        bitmapFile.seek(assetOffset)
        bytesRead = bitmapFile.readinto(bitmapData)
    if bytesRead != byteCount:
        raise OSError("Invalid bitmap asset: " + assetName)
    return bitmapData


titleBackgroundData = loadBitmapData("titleBackground")
highscoreBackgroundData = loadBitmapData("highscoreBackground")
highscoreButtonData = loadBitmapData("highscoreButton")
highscoreButtonMaskData = loadBitmapData("highscoreButton_mask")
resultBackgroundData = loadBitmapData("resultBackground")
resultCharacterData = loadBitmapData("resultCharacter")
resultCharacterMaskData = loadBitmapData("resultCharacter_mask")
resultSelectUiData = loadBitmapData("resultSelectUI")
resultSelectUiMaskData = loadBitmapData("resultSelectUI_mask")
titleCharacter1Data = loadBitmapData("titleCharacter1")
titleCharacter1MaskData = loadBitmapData("titleCharacter1_mask")
titleCharacter2Data = loadBitmapData("titleCharacter2")
titleCharacter2MaskData = loadBitmapData("titleCharacter2_mask")
titleTransitionImageData = loadBitmapData("titleTransitionImage")
resultTransitionImageInversionData = loadBitmapData("resultTransitionImageInversion")
fadeTextureData = loadBitmapData("fadeTexture")
fadeTextureMaskData = loadBitmapData("fadeTexture_mask")
titleSelectUiStartData = loadBitmapData("title_electUiStart")
titleSelectUiStartMaskData = loadBitmapData("title_electUiStart_mask")
titleSelectUiScoreData = loadBitmapData("title_electUiScore")
titleSelectUiScoreMaskData = loadBitmapData("title_electUiScore_mask")
ready = loadBitmapData("ready")
ready_mask = loadBitmapData("ready_mask")
start = loadBitmapData("start")
start_mask = loadBitmapData("start_mask")
finished = loadBitmapData("finished")
finished_mask = loadBitmapData("finished_mask")
playerSpriteSheet = loadBitmapData("playerSpriteSheet")
playerMaskSheet = loadBitmapData("playerMaskSheet")
playerJumpSpriteSheet = loadBitmapData("playerJumpSpriteSheet")
playerJumpMaskSheet = loadBitmapData("playerJumpMaskSheet")
playerFallSpriteSheet = loadBitmapData("playerFallSpriteSheet")
playerFallMaskSheet = loadBitmapData("playerFallMaskSheet")
gc.collect()
titleBackground = thumby.Sprite(
    INTRO_WIDTH, INTRO_HEIGHT, titleBackgroundData, 0, 0
)
highscoreBackground = thumby.Sprite(
    INTRO_WIDTH, INTRO_HEIGHT, highscoreBackgroundData, 0, 0
)
highscoreButton = thumby.Sprite(
    INTRO_WIDTH, INTRO_HEIGHT, highscoreButtonData, 0, 0
)
highscoreButtonMask = thumby.Sprite(
    INTRO_WIDTH, INTRO_HEIGHT, highscoreButtonMaskData, 0, 0
)
resultBackground = thumby.Sprite(
    INTRO_WIDTH, INTRO_HEIGHT, resultBackgroundData, 0, 0
)
resultCharacter = thumby.Sprite(
    INTRO_WIDTH, INTRO_HEIGHT, resultCharacterData, 0, 0
)
resultCharacterMask = thumby.Sprite(
    INTRO_WIDTH, INTRO_HEIGHT, resultCharacterMaskData, 0, 0
)
resultSelectUi = thumby.Sprite(
    INTRO_WIDTH, INTRO_HEIGHT, resultSelectUiData, 0, 0
)
resultSelectUiMask = thumby.Sprite(
    INTRO_WIDTH, INTRO_HEIGHT, resultSelectUiMaskData, 0, 0
)
titleCharacter1 = thumby.Sprite(
    INTRO_WIDTH, INTRO_HEIGHT, titleCharacter1Data, 0, 0
)
titleCharacter1Mask = thumby.Sprite(
    INTRO_WIDTH, INTRO_HEIGHT, titleCharacter1MaskData, 0, 0
)
titleCharacter2 = thumby.Sprite(
    INTRO_WIDTH, INTRO_HEIGHT, titleCharacter2Data, 0, 0
)
titleCharacter2Mask = thumby.Sprite(
    INTRO_WIDTH, INTRO_HEIGHT, titleCharacter2MaskData, 0, 0
)
titleTransitionImage = thumby.Sprite(
    INTRO_WIDTH, INTRO_HEIGHT, titleTransitionImageData, 0, 0
)
resultTransitionImageInversion = thumby.Sprite(
    INTRO_WIDTH, INTRO_HEIGHT, resultTransitionImageInversionData, 0, 0
)
fadeTexture = thumby.Sprite(
    INTRO_WIDTH, INTRO_HEIGHT, fadeTextureData, 0, 0
)
fadeTextureMask = thumby.Sprite(
    INTRO_WIDTH, INTRO_HEIGHT, fadeTextureMaskData, 0, 0
)
titleSelectUiStart = thumby.Sprite(
    INTRO_WIDTH, INTRO_HEIGHT, titleSelectUiStartData, 0, 0
)
titleSelectUiStartMask = thumby.Sprite(
    INTRO_WIDTH, INTRO_HEIGHT, titleSelectUiStartMaskData, 0, 0
)
titleSelectUiScore = thumby.Sprite(
    INTRO_WIDTH, INTRO_HEIGHT, titleSelectUiScoreData, 0, 0
)
titleSelectUiScoreMask = thumby.Sprite(
    INTRO_WIDTH, INTRO_HEIGHT, titleSelectUiScoreMaskData, 0, 0
)
readySprite = thumby.Sprite(INTRO_WIDTH, INTRO_HEIGHT, ready, 0, 0)
readyMaskSprite = thumby.Sprite(INTRO_WIDTH, INTRO_HEIGHT, ready_mask, 0, 0)
startSprite = thumby.Sprite(INTRO_WIDTH, INTRO_HEIGHT, start, 0, 0)
startMaskSprite = thumby.Sprite(INTRO_WIDTH, INTRO_HEIGHT, start_mask, 0, 0)
finishedSprite = thumby.Sprite(INTRO_WIDTH, INTRO_HEIGHT, finished, 0, 0)
finishedMaskSprite = thumby.Sprite(INTRO_WIDTH, INTRO_HEIGHT, finished_mask, 0, 0)

player = thumby.Sprite(PLAYER_WIDTH, PLAYER_HEIGHT, playerSpriteSheet, PLAYER_START_X, PLAYER_START_Y)
playerMask = thumby.Sprite(PLAYER_WIDTH, PLAYER_HEIGHT, playerMaskSheet, PLAYER_START_X, PLAYER_START_Y)
playerJump = thumby.Sprite(
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    playerJumpSpriteSheet,
    PLAYER_START_X,
    PLAYER_START_Y
)
playerJumpMask = thumby.Sprite(
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    playerJumpMaskSheet,
    PLAYER_START_X,
    PLAYER_START_Y
)
playerFall = thumby.Sprite(
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    playerFallSpriteSheet,
    PLAYER_START_X,
    PLAYER_START_Y
)
playerFallMask = thumby.Sprite(
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    playerFallMaskSheet,
    PLAYER_START_X,
    PLAYER_START_Y
)
#============================================
# Player state and collision helpers
#============================================
playerFrame = 0
playerFrameScrollDistance = 0.0

# Physics parameters.
velocityY = 0.0
playerY = float(player.y)


def getPlayerCollisionRect(currentPlayerY):
    collisionLeft = player.x + collisionOffsetX
    collisionTop = currentPlayerY + collisionOffsetY
    collisionRight = collisionLeft + collisionWidth
    collisionBottom = collisionTop + collisionHeight
    return collisionLeft, collisionTop, collisionRight, collisionBottom


def playerCollisionOverlapsPlatformX(platform, currentPlayerY):
    collisionLeft, _, collisionRight, _ = getPlayerCollisionRect(currentPlayerY)
    return (
        collisionLeft < platform.x + platform.width
        and collisionRight > platform.x
    )

#============================================
# Jump and platform calculation helpers
#============================================
# Jump state.
jumpCount = 0

# Hover at the highest point.
hoverTimer = 0.0
isHovering = False

# Ground state.

# Moving platforms.
# List of normal platforms represented as [x, y, width, height].

def nextPlatformRandom(maxValue):
    global platformRandomSeed
    platformRandomSeed = (platformRandomSeed * 73 + 41) % 997
    return platformRandomSeed % maxValue


def getInitialPlatformRandomSeed():
    if not platformRandomizeSeed:
        return platformGenerationConfig["randomSeed"]

    if random is not None:
        try:
            return random.getrandbits(16) % 997
        except (AttributeError, OSError, ValueError):
            pass

    return time.ticks_ms() % 997


def getStageLevelFromScore(score):
    level = 1
    for index in range(len(STAGE_LEVEL_START_SCORES)):
        if score >= STAGE_LEVEL_START_SCORES[index]:
            level = index + 1
    return min(level, MAX_STAGE_LEVEL)


def resetStageLevel():
    return 1


def getStageScrollSpeed(stageLevel):
    speedIndex = stageLevel - 1
    if speedIndex < 0:
        speedIndex = 0
    if speedIndex >= len(STAGE_SCROLL_INTERVAL_SECONDS):
        speedIndex = len(STAGE_SCROLL_INTERVAL_SECONDS) - 1

    intervalSeconds = STAGE_SCROLL_INTERVAL_SECONDS[speedIndex]
    if intervalSeconds <= 0:
        return 0

    # The table defines seconds per pixel. Convert to pixels per frame.
    return 1.0 / (intervalSeconds * DISPLAY_FPS)


def getStagePlatformConfig(stageLevel):
    configIndex = stageLevel - 1
    if configIndex < 0:
        configIndex = 0
    if configIndex >= MAX_STAGE_LEVEL:
        configIndex = MAX_STAGE_LEVEL - 1
    return STAGE_LEVEL_CONFIGS[configIndex]


def calculateMaxReachableHeight():
    # Simulate the same vertical update used by gameplay. Try every legal
    # frame for the second jump and keep the highest point reached.
    maxReachableHeight = 0.0
    simulationFrames = 120
    secondJumpFrames = range(-1, simulationFrames)

    for secondJumpFrame in secondJumpFrames:
        simulatedY = 0.0
        simulatedVelocityY = jumpPower
        simulatedJumpCount = 1
        simulatedIsHovering = False

        for frame in range(simulationFrames):
            if (
                frame == secondJumpFrame
                and simulatedJumpCount < maxJumps
                and (simulatedIsHovering or simulatedVelocityY > 0)
            ):
                simulatedVelocityY = doubleJumpPower
                simulatedJumpCount += 1
                simulatedIsHovering = False

            previousVelocityY = simulatedVelocityY
            simulatedVelocityY += gravity * DELTA_TIME_SECONDS

            if (
                jumpHoverTimeSeconds > 0
                and simulatedJumpCount <= maxJumps
                and previousVelocityY < 0
                and simulatedVelocityY >= 0
            ):
                simulatedVelocityY = 0
                simulatedIsHovering = True
            else:
                simulatedY += simulatedVelocityY * DELTA_TIME_SECONDS

            if -simulatedY > maxReachableHeight:
                maxReachableHeight = -simulatedY

    if maxReachableHeight <= 0:
        raise ValueError("Jump settings must allow upward movement")
    return maxReachableHeight


MAX_REACHABLE_HEIGHT = calculateMaxReachableHeight()


def calculateMaxAirborneFrames():
    # Simulate the gameplay vertical update and keep the longest time until
    # the player returns to the takeoff platform height. Try every legal frame
    # for the second jump, including the no-second-jump case.
    maxAirborneFrames = 0
    simulationFrames = 240
    secondJumpFrames = range(-1, simulationFrames)

    for secondJumpFrame in secondJumpFrames:
        simulatedY = 0.0
        simulatedVelocityY = jumpPower
        simulatedJumpCount = 1
        simulatedIsHovering = False
        simulatedHoverTimer = 0.0

        for frame in range(simulationFrames):
            if (
                frame == secondJumpFrame
                and simulatedJumpCount < maxJumps
                and (simulatedIsHovering or simulatedVelocityY > 0)
            ):
                simulatedVelocityY = doubleJumpPower
                simulatedJumpCount += 1
                simulatedIsHovering = False
                simulatedHoverTimer = 0.0

            previousY = simulatedY

            if simulatedIsHovering:
                simulatedHoverTimer += DELTA_TIME_SECONDS

                if simulatedHoverTimer >= jumpHoverTimeSeconds:
                    simulatedIsHovering = False
                    simulatedVelocityY = 0
            else:
                previousVelocityY = simulatedVelocityY
                simulatedVelocityY += gravity * DELTA_TIME_SECONDS

                if (
                    jumpHoverTimeSeconds > 0
                    and simulatedJumpCount <= maxJumps
                    and previousVelocityY < 0
                    and simulatedVelocityY >= 0
                ):
                    simulatedVelocityY = 0
                    simulatedIsHovering = True
                    simulatedHoverTimer = 0
                else:
                    simulatedY += simulatedVelocityY * DELTA_TIME_SECONDS

            airborneFrames = frame + 1
            if (
                not simulatedIsHovering
                and previousY < 0
                and simulatedY >= 0
            ):
                if airborneFrames > maxAirborneFrames:
                    maxAirborneFrames = airborneFrames
                break

    if maxAirborneFrames <= 0:
        raise ValueError("Jump settings must allow airborne movement")
    return maxAirborneFrames


MAX_AIRBORNE_FRAMES = calculateMaxAirborneFrames()


def getStagePlatformWidth(stageLevel):
    return getStagePlatformConfig(stageLevel)["platformWidth"]


def getStageMaxHeightDiff(stageLevel):
    heightRate = getStagePlatformConfig(stageLevel)["heightDifferenceRate"]
    return int(MAX_REACHABLE_HEIGHT * heightRate / 100)

#============================================
# Platform objects and runtime state
#============================================
# Ground contact state.
onPlatform = False
onStartPlatform = True
currentPlatform = None
score = INITIAL_SCORE
stageLevel = getStageLevelFromScore(score)

# Generate several platforms ahead at startup.
# Platform types, equivalent to an enum for MicroPython.
class PlatformType:
    START = 0
    NORMAL = 1

class Platform:
    def __init__(self, x, y, width, height, platformType):
        self.x = float(x)
        self.y = y
        self.width = width
        self.height = height
        self.platformType = platformType

    def move(self, speed):
        self.x -= speed

def resetGameplayState():
    global onPlatform, onStartPlatform, currentPlatform
    global score, stageLevel, platformRandomSeed
    global startPlatform, normalPlatform, platforms
    global velocityY, playerY, playerFrame, playerFrameScrollDistance
    global jumpCount, hoverTimer, isHovering

    onPlatform = False
    onStartPlatform = True
    currentPlatform = None
    score = INITIAL_SCORE
    stageLevel = getStageLevelFromScore(score)
    platformRandomSeed = getInitialPlatformRandomSeed()

    startPlatform = Platform(
        startPlatformConfig["x"],
        startPlatformConfig["y"],
        startPlatformConfig["width"],
        startPlatformConfig["height"],
        PlatformType.START
    )
    normalPlatform = createGeneratedNormalPlatform(startPlatform, True)
    platforms = [startPlatform, normalPlatform]

    velocityY = 0.0
    playerY = float(PLAYER_START_Y)
    playerFrame = 0
    playerFrameScrollDistance = 0.0
    jumpCount = 0
    hoverTimer = 0.0
    isHovering = False

    player.x = PLAYER_START_X
    player.y = PLAYER_START_Y
    player.setFrame(0)
    playerMask.x = PLAYER_START_X
    playerMask.y = PLAYER_START_Y
    playerMask.setFrame(0)
    playerJump.x = PLAYER_START_X
    playerJump.y = PLAYER_START_Y
    playerJumpMask.x = PLAYER_START_X
    playerJumpMask.y = PLAYER_START_Y
    playerFall.x = PLAYER_START_X
    playerFall.y = PLAYER_START_Y
    playerFallMask.x = PLAYER_START_X
    playerFallMask.y = PLAYER_START_Y

#============================================
# Platform generation
#============================================
# Generation constraints: keep only candidates reachable from the previous platform.
maxJumpFrames = MAX_AIRBORNE_FRAMES


def getStageMaxPlatformGap(stageLevel):
    stageSpeed = getStageScrollSpeed(stageLevel)
    physicalMaxGap = int(stageSpeed * maxJumpFrames)
    horizontalGapRate = getStagePlatformConfig(stageLevel)["horizontalGapRate"]
    effectiveMaxGap = int(physicalMaxGap * horizontalGapRate / 100)
    return max(0, effectiveMaxGap - platformGapMargin)


def getStagePlatformGapRange(stageLevel):
    maximumGap = getStageMaxPlatformGap(stageLevel)
    minimumGap = min(platformMinGapPixels, maximumGap)
    return minimumGap, maximumGap


def createGeneratedNormalPlatform(previousPlatform, randomizeFallbackGap=False):
    currentPlatformWidth = getStagePlatformWidth(stageLevel)
    currentMaxHeightDiff = getStageMaxHeightDiff(stageLevel)
    currentMinPlatformGap, currentMaxPlatformGap = getStagePlatformGapRange(
        stageLevel
    )

    for attempt in range(platformGenerationAttempts):
        gap = (
            currentMinPlatformGap
            + nextPlatformRandom(
                currentMaxPlatformGap - currentMinPlatformGap + 1
            )
        )
        heightChange = nextPlatformRandom(currentMaxHeightDiff * 2 + 1) - currentMaxHeightDiff
        candidateX = previousPlatform.x + previousPlatform.width + gap
        candidateY = previousPlatform.y + heightChange

        if candidateY < platformMinY:
            candidateY = platformMinY
        if candidateY > platformMaxY:
            candidateY = platformMaxY

        horizontalGap = candidateX - (previousPlatform.x + previousPlatform.width)
        verticalGap = abs(candidateY - previousPlatform.y)
        if (
            currentMinPlatformGap <= horizontalGap <= currentMaxPlatformGap
            and verticalGap <= currentMaxHeightDiff
        ):
            return Platform(
                candidateX,
                candidateY,
                currentPlatformWidth,
                platformHeight,
                PlatformType.NORMAL
            )

    # The initial platform starts lower than the normal generation range.
    # Keep it safe at the start height while still varying its gap.
    fallbackGap = currentMinPlatformGap
    if randomizeFallbackGap:
        fallbackGap += nextPlatformRandom(
            currentMaxPlatformGap - currentMinPlatformGap + 1
        )
    return Platform(
        (
            previousPlatform.x
            + previousPlatform.width
            + fallbackGap
        ),
        previousPlatform.y,
        currentPlatformWidth,
        platformHeight,
        PlatformType.NORMAL
    )


# Keep the player start platform fixed, then generate the first normal platform.
platformRandomSeed = getInitialPlatformRandomSeed()
startPlatform = Platform(
    startPlatformConfig["x"],
    startPlatformConfig["y"],
    startPlatformConfig["width"],
    startPlatformConfig["height"],
    PlatformType.START
)
normalPlatform = createGeneratedNormalPlatform(startPlatform, True)
platforms = [startPlatform, normalPlatform]


def drawGameBackground(renderPlayer, renderPlayerMask, startPlatformIsActive):
    thumby.display.fill(1)
    setDisplayFont(GAME_SCORE_FONT_CONFIG)
    thumby.display.drawText(
        "{:03d}".format(min(score, 999)),
        GAME_SCORE_POSITION["x"],
        GAME_SCORE_POSITION["y"],
        0
    )

    for renderPlatform in platforms:
        thumby.display.drawFilledRectangle(
            math.floor(renderPlatform.x),
            renderPlatform.y,
            renderPlatform.width,
            renderPlatform.height,
            0
        )

    if startPlatformIsActive:
        thumby.display.drawFilledRectangle(
            math.floor(startPlatform.x),
            startPlatform.y,
            startPlatform.width,
            startPlatform.height,
            0
        )

    thumby.display.drawSpriteWithMask(renderPlayer, renderPlayerMask)


def drawFinishedScene():
    finishedStartPlatformActive = startPlatform.x + startPlatform.width > 0
    drawGameBackground(
        activePlayer,
        activePlayerMask,
        finishedStartPlatformActive
    )
    thumby.display.drawSpriteWithMask(finishedSprite, finishedMaskSprite)


def drawResultScene(resultSelectEnd, resultScoreText, resultScoreDigits):
    thumby.display.drawSprite(resultBackground)
    setDisplayFont(RESULT_SCORE_FONT_CONFIG)
    # Reveal the score from the ones place to the hundreds place.
    if resultScoreDigits >= 1:
        thumby.display.drawText(
            resultScoreText[2],
            RESULT_SCORE_POSITION["x"]
            + (RESULT_SCORE_FONT_CONFIG["width"]
               + RESULT_SCORE_FONT_CONFIG["space"]) * 2,
            RESULT_SCORE_POSITION["y"],
            0
        )
    if resultScoreDigits >= 2:
        thumby.display.drawText(
            resultScoreText[1],
            RESULT_SCORE_POSITION["x"]
            + RESULT_SCORE_FONT_CONFIG["width"]
            + RESULT_SCORE_FONT_CONFIG["space"],
            RESULT_SCORE_POSITION["y"],
            0
        )
    if resultScoreDigits >= 3:
        thumby.display.drawText(
            resultScoreText[0],
            RESULT_SCORE_POSITION["x"],
            RESULT_SCORE_POSITION["y"],
            0
        )
    resultCharacterFrame = 1 if resultScoreDigits >= 3 else 0
    resultCharacter.setFrame(resultCharacterFrame)
    resultCharacterMask.setFrame(resultCharacterFrame)
    thumby.display.drawSpriteWithMask(resultCharacter, resultCharacterMask)
    resultSelectUiFrame = 0 if resultSelectEnd else 1
    resultSelectUi.setFrame(resultSelectUiFrame)
    resultSelectUiMask.setFrame(resultSelectUiFrame)
    thumby.display.drawSpriteWithMask(resultSelectUi, resultSelectUiMask)


def drawHighscoreScene():
    thumby.display.drawSprite(highscoreBackground)
    setDisplayFont(HIGHSCORE_FONT_CONFIG)
    for rankIndex in range(3):
        rankPosition = HIGHSCORE_RANK_POSITIONS[rankIndex]
        thumby.display.drawText(
            "{:03d}".format(highscores[rankIndex]),
            rankPosition["x"],
            rankPosition["y"],
            0
        )
    highscoreButton.setFrame(highscoreButtonFrame)
    highscoreButtonMask.setFrame(highscoreButtonFrame)
    thumby.display.drawSpriteWithMask(
        highscoreButton,
        highscoreButtonMask
    )


#============================================
# Main game loop states
#============================================
thumby.display.setFPS(DISPLAY_FPS)

# Game start sequence state.
TITLE = 0
TITLE_START_ANIMATION = 1
TITLE_FADE_TEXTURE_ANIMATION = 2
TITLE_TRANSITION_IMAGE_ANIMATION = 3
TITLE_FADE_TEXTURE_REVERSE_ANIMATION = 4
READY = 5
START = 6
PLAYING = 7
FINISHED = 8
HIGHSCORE = 9
TITLE_HIGHSCORE_FADE_TEXTURE_ANIMATION = 10
HIGHSCORE_FADE_TEXTURE_REVERSE_ANIMATION = 11
HIGHSCORE_FADE_TEXTURE_ANIMATION = 12
TITLE_HIGHSCORE_FADE_TEXTURE_REVERSE_ANIMATION = 13
GAME_RESULT_FADE_TEXTURE_ANIMATION = 14
RESULT_FADE_TEXTURE_REVERSE_ANIMATION = 15
RESULT = 16
RESULT_TITLE_FADE_TEXTURE_ANIMATION = 17
RESULT_TITLE_TRANSITION_IMAGE_ANIMATION = 18
RESULT_TITLE_FINAL_FADE_TEXTURE_ANIMATION = 19
RESULT_RETRY_FADE_TEXTURE_ANIMATION = 20
RESULT_RETRY_FADE_TEXTURE_REVERSE_ANIMATION = 21
gameState = TITLE
introTimer = 0
titleSelectStart = True
titleCharacterFrame = 0
titleCharacterFrameTimer = 0
titleCharacterFrameDurations = (
    DISPLAY_FPS * 3 // 2,
    DISPLAY_FPS // 2
)
titleStartAnimationFrame = 0
titleStartAnimationFrameTimer = 0
titleStartAnimationFrameDurations = (
    DISPLAY_FPS // 5,
    DISPLAY_FPS // 5,
    DISPLAY_FPS // 5,
    DISPLAY_FPS * 8 // 5
)
titleFadeTextureFrame = 0
titleFadeTextureFrameTimer = 0
titleFadeTextureFrameDurations = (
    DISPLAY_FPS // 4,
    DISPLAY_FPS // 4,
    DISPLAY_FPS // 4,
    DISPLAY_FPS * 3 // 4
)
titleFadeTextureReverseFrame = 3
titleFadeTextureReverseFrameTimer = 0
titleTransitionImageFrame = 0
titleTransitionImageFrameTimer = 0
titleTransitionImageFrameDuration = DISPLAY_FPS // 4
highscoreButtonFrame = 0
highscoreButtonFrameTimer = 0
highscoreButtonFrameDuration = DISPLAY_FPS
titleHighscoreFadeTextureFrame = 0
titleHighscoreFadeTextureFrameTimer = 0
titleHighscoreFadeTextureReverseFrame = 3
titleHighscoreFadeTextureReverseFrameTimer = 0
highscoreFadeTextureFrame = 0
highscoreFadeTextureFrameTimer = 0
highscoreFadeTextureReverseFrame = 3
highscoreFadeTextureReverseFrameTimer = 0
gameResultFadeTextureFrame = 0
gameResultFadeTextureFrameTimer = 0
resultFadeTextureReverseFrame = 3
resultFadeTextureReverseFrameTimer = 0
resultSelectEnd = False
resultScoreText = "000"
resultScoreValue = 0
resultScoreDigits = 0
resultScoreFrameTimer = 0
resultScoreInputEnabled = False
resultScoreSaved = False
resultTitleFadeTextureFrame = 0
resultTitleFadeTextureFrameTimer = 0
resultTitleTransitionImageFrame = 0
resultTitleTransitionImageFrameTimer = 0
resultTitleFinalFadeTextureFrame = 3
resultTitleFinalFadeTextureFrameTimer = 0
resultTitleFinalFadeTextureFrameDurations = (
    DISPLAY_FPS // 4,
    DISPLAY_FPS // 4,
    DISPLAY_FPS // 4,
    DISPLAY_FPS * 3 // 4
)
resultRetryFadeTextureFrame = 0
resultRetryFadeTextureFrameTimer = 0
resultRetryFadeTextureReverseFrame = 3
resultRetryFadeTextureReverseFrameTimer = 0

while True:

    # TITLE is a true pause: select a menu item before showing the game intro.
    if gameState == TITLE:
        titleUpPressed = thumby.buttonU.justPressed()
        titleDownPressed = thumby.buttonD.justPressed()
        if titleSelectStart and titleDownPressed:
            titleSelectStart = False
            playSound(SOUND_CURSOR)
        elif not titleSelectStart and titleUpPressed:
            titleSelectStart = True
            playSound(SOUND_CURSOR)
        titleConfirmPressed = thumby.buttonA.justPressed()

        thumby.display.drawSprite(titleBackground)
        titleCharacter1.setFrame(titleCharacterFrame)
        titleCharacter1Mask.setFrame(titleCharacterFrame)
        thumby.display.drawSpriteWithMask(
            titleCharacter1,
            titleCharacter1Mask
        )
        if titleSelectStart:
            thumby.display.drawSpriteWithMask(
                titleSelectUiStart,
                titleSelectUiStartMask
            )
        else:
            thumby.display.drawSpriteWithMask(
                titleSelectUiScore,
                titleSelectUiScoreMask
            )
        thumby.display.update()

        titleCharacterFrameTimer += 1
        if (
            titleCharacterFrameTimer
            >= titleCharacterFrameDurations[titleCharacterFrame]
        ):
            titleCharacterFrameTimer = 0
            titleCharacterFrame = (titleCharacterFrame + 1) % 2

        if titleConfirmPressed:
            playSound(SOUND_CONFIRM)
            if titleSelectStart:
                resetGameplayState()
                gameState = TITLE_START_ANIMATION
                titleStartAnimationFrame = 0
                titleStartAnimationFrameTimer = 0
            else:
                gameState = TITLE_HIGHSCORE_FADE_TEXTURE_ANIMATION
                titleHighscoreFadeTextureFrame = 0
                titleHighscoreFadeTextureFrameTimer = 0
        continue

    # Fade the normal title scene before opening the highscore scene.
    if gameState == TITLE_HIGHSCORE_FADE_TEXTURE_ANIMATION:
        thumby.display.drawSprite(titleBackground)
        titleCharacter1.setFrame(titleCharacterFrame)
        titleCharacter1Mask.setFrame(titleCharacterFrame)
        thumby.display.drawSpriteWithMask(
            titleCharacter1,
            titleCharacter1Mask
        )
        thumby.display.drawSpriteWithMask(
            titleSelectUiScore,
            titleSelectUiScoreMask
        )
        fadeTexture.setFrame(titleHighscoreFadeTextureFrame)
        fadeTextureMask.setFrame(titleHighscoreFadeTextureFrame)
        thumby.display.drawSpriteWithMask(fadeTexture, fadeTextureMask)
        thumby.display.update()

        titleHighscoreFadeTextureFrameTimer += 1
        if (
            titleHighscoreFadeTextureFrameTimer
            >= titleFadeTextureFrameDurations[titleHighscoreFadeTextureFrame]
        ):
            titleHighscoreFadeTextureFrameTimer = 0
            if titleHighscoreFadeTextureFrame < 3:
                titleHighscoreFadeTextureFrame += 1
            else:
                gameState = HIGHSCORE_FADE_TEXTURE_REVERSE_ANIMATION
                highscoreFadeTextureReverseFrame = 3
                highscoreFadeTextureReverseFrameTimer = 0
        continue

    # HIGHSCORE loops the button animation and can transition to the title.
    if gameState == HIGHSCORE:
        drawHighscoreScene()
        thumby.display.update()

        highscoreButtonFrameTimer += 1
        if highscoreButtonFrameTimer >= highscoreButtonFrameDuration:
            highscoreButtonFrameTimer = 0
            highscoreButtonFrame = (highscoreButtonFrame + 1) % 2

        if thumby.buttonA.justPressed():
            playSound(SOUND_CONFIRM)
            gameState = HIGHSCORE_FADE_TEXTURE_ANIMATION
            highscoreFadeTextureFrame = 0
            highscoreFadeTextureFrameTimer = 0
        continue

    # Reveal the highscore scene after fading out the title scene.
    if gameState == HIGHSCORE_FADE_TEXTURE_REVERSE_ANIMATION:
        drawHighscoreScene()
        fadeTexture.setFrame(highscoreFadeTextureReverseFrame)
        fadeTextureMask.setFrame(highscoreFadeTextureReverseFrame)
        thumby.display.drawSpriteWithMask(fadeTexture, fadeTextureMask)
        thumby.display.update()

        highscoreFadeTextureReverseFrameTimer += 1
        if (
            highscoreFadeTextureReverseFrameTimer
            >= titleFadeTextureFrameDurations[
                highscoreFadeTextureReverseFrame
            ]
        ):
            highscoreFadeTextureReverseFrameTimer = 0
            if highscoreFadeTextureReverseFrame > 0:
                highscoreFadeTextureReverseFrame -= 1
            else:
                gameState = HIGHSCORE
                highscoreButtonFrame = 0
                highscoreButtonFrameTimer = 0
        continue

    # Fade the highscore scene before returning to the title scene.
    if gameState == HIGHSCORE_FADE_TEXTURE_ANIMATION:
        drawHighscoreScene()
        fadeTexture.setFrame(highscoreFadeTextureFrame)
        fadeTextureMask.setFrame(highscoreFadeTextureFrame)
        thumby.display.drawSpriteWithMask(fadeTexture, fadeTextureMask)
        thumby.display.update()

        highscoreFadeTextureFrameTimer += 1
        if (
            highscoreFadeTextureFrameTimer
            >= titleFadeTextureFrameDurations[highscoreFadeTextureFrame]
        ):
            highscoreFadeTextureFrameTimer = 0
            if highscoreFadeTextureFrame < 3:
                highscoreFadeTextureFrame += 1
            else:
                gameState = TITLE_HIGHSCORE_FADE_TEXTURE_REVERSE_ANIMATION
                titleHighscoreFadeTextureReverseFrame = 3
                titleHighscoreFadeTextureReverseFrameTimer = 0
        continue

    # Reveal the title scene after fading out the highscore scene.
    if gameState == TITLE_HIGHSCORE_FADE_TEXTURE_REVERSE_ANIMATION:
        thumby.display.drawSprite(titleBackground)
        titleCharacter1.setFrame(titleCharacterFrame)
        titleCharacter1Mask.setFrame(titleCharacterFrame)
        thumby.display.drawSpriteWithMask(
            titleCharacter1,
            titleCharacter1Mask
        )
        thumby.display.drawSpriteWithMask(
            titleSelectUiScore,
            titleSelectUiScoreMask
        )
        fadeTexture.setFrame(titleHighscoreFadeTextureReverseFrame)
        fadeTextureMask.setFrame(titleHighscoreFadeTextureReverseFrame)
        thumby.display.drawSpriteWithMask(fadeTexture, fadeTextureMask)
        thumby.display.update()

        titleHighscoreFadeTextureReverseFrameTimer += 1
        if (
            titleHighscoreFadeTextureReverseFrameTimer
            >= titleFadeTextureFrameDurations[
                titleHighscoreFadeTextureReverseFrame
            ]
        ):
            titleHighscoreFadeTextureReverseFrameTimer = 0
            if titleHighscoreFadeTextureReverseFrame > 0:
                titleHighscoreFadeTextureReverseFrame -= 1
            else:
                gameState = TITLE
        continue

    # Play the start transition once, then enter the existing game intro.
    if gameState == TITLE_START_ANIMATION:
        thumby.display.drawSprite(titleBackground)
        titleCharacter2.setFrame(titleStartAnimationFrame)
        titleCharacter2Mask.setFrame(titleStartAnimationFrame)
        thumby.display.drawSpriteWithMask(
            titleCharacter2,
            titleCharacter2Mask
        )
        thumby.display.drawSpriteWithMask(
            titleSelectUiStart,
            titleSelectUiStartMask
        )
        thumby.display.update()

        titleStartAnimationFrameTimer += 1
        if (
            titleStartAnimationFrameTimer
            >= titleStartAnimationFrameDurations[titleStartAnimationFrame]
        ):
            titleStartAnimationFrameTimer = 0
            if titleStartAnimationFrame < 3:
                titleStartAnimationFrame += 1
            else:
                gameState = TITLE_FADE_TEXTURE_ANIMATION
                titleFadeTextureFrame = 0
                titleFadeTextureFrameTimer = 0
        continue

    # Overlay the title screen with the fade texture once before the transition.
    if gameState == TITLE_FADE_TEXTURE_ANIMATION:
        thumby.display.drawSprite(titleBackground)
        titleCharacter2.setFrame(3)
        titleCharacter2Mask.setFrame(3)
        thumby.display.drawSpriteWithMask(
            titleCharacter2,
            titleCharacter2Mask
        )
        thumby.display.drawSpriteWithMask(
            titleSelectUiStart,
            titleSelectUiStartMask
        )
        fadeTexture.setFrame(titleFadeTextureFrame)
        fadeTextureMask.setFrame(titleFadeTextureFrame)
        thumby.display.drawSpriteWithMask(fadeTexture, fadeTextureMask)
        thumby.display.update()

        titleFadeTextureFrameTimer += 1
        if (
            titleFadeTextureFrameTimer
            >= titleFadeTextureFrameDurations[titleFadeTextureFrame]
        ):
            titleFadeTextureFrameTimer = 0
            if titleFadeTextureFrame < 3:
                titleFadeTextureFrame += 1
            else:
                gameState = TITLE_TRANSITION_IMAGE_ANIMATION
                titleTransitionImageFrame = 0
                titleTransitionImageFrameTimer = 0
        continue

    # Play the full-screen transition image once before entering the game intro.
    if gameState == TITLE_TRANSITION_IMAGE_ANIMATION:
        titleTransitionImage.setFrame(titleTransitionImageFrame)
        thumby.display.drawSprite(titleTransitionImage)
        thumby.display.update()

        titleTransitionImageFrameTimer += 1
        if titleTransitionImageFrameTimer >= titleTransitionImageFrameDuration:
            titleTransitionImageFrameTimer = 0
            if titleTransitionImageFrame < 4:
                titleTransitionImageFrame += 1
            else:
                gameState = TITLE_FADE_TEXTURE_REVERSE_ANIMATION
                titleFadeTextureReverseFrame = 3
                titleFadeTextureReverseFrameTimer = 0
        continue

    # Reveal the initial game screen before showing the READY overlay.
    if gameState == TITLE_FADE_TEXTURE_REVERSE_ANIMATION:
        reverseFadeStartPlatformActive = startPlatform.x + startPlatform.width > 0
        drawGameBackground(
            player,
            playerMask,
            reverseFadeStartPlatformActive
        )
        fadeTexture.setFrame(titleFadeTextureReverseFrame)
        fadeTextureMask.setFrame(titleFadeTextureReverseFrame)
        thumby.display.drawSpriteWithMask(fadeTexture, fadeTextureMask)
        thumby.display.update()

        titleFadeTextureReverseFrameTimer += 1
        if (
            titleFadeTextureReverseFrameTimer
            >= titleFadeTextureFrameDurations[titleFadeTextureReverseFrame]
        ):
            titleFadeTextureReverseFrameTimer = 0
            if titleFadeTextureReverseFrame > 0:
                titleFadeTextureReverseFrame -= 1
            else:
                gameState = READY
                introTimer = 0
                playSound(SOUND_READY)
        continue

    # READY is a true pause: do not run gameplay, scrolling, or physics.
    if gameState == READY:
        introTimer += 1
        thumby.buttonA.justPressed()  # consume input so it cannot carry over

        readyStartPlatformActive = startPlatform.x + startPlatform.width > 0
        drawGameBackground(player, playerMask, readyStartPlatformActive)
        thumby.display.drawSpriteWithMask(readySprite, readyMaskSprite)
        thumby.display.update()

        if introTimer >= INTRO_FRAMES:
            gameState = START
            introTimer = 0
            playSound(SOUND_START)
        continue

    # FINISHED pauses the game and can transition to the result scene.
    if gameState == FINISHED:
        drawFinishedScene()
        thumby.display.update()

        if thumby.buttonA.justPressed():
            gameState = GAME_RESULT_FADE_TEXTURE_ANIMATION
            gameResultFadeTextureFrame = 0
            gameResultFadeTextureFrameTimer = 0
            resultSelectEnd = False
            resultScoreValue = min(score, 999)
            resultScoreText = "{:03d}".format(resultScoreValue)
            resultScoreDigits = 0
            resultScoreFrameTimer = 0
            resultScoreInputEnabled = False
            resultScoreSaved = False
        continue

    # Fade the finished game scene before opening the result scene.
    if gameState == GAME_RESULT_FADE_TEXTURE_ANIMATION:
        drawFinishedScene()
        fadeTexture.setFrame(gameResultFadeTextureFrame)
        fadeTextureMask.setFrame(gameResultFadeTextureFrame)
        thumby.display.drawSpriteWithMask(fadeTexture, fadeTextureMask)
        thumby.display.update()

        gameResultFadeTextureFrameTimer += 1
        if (
            gameResultFadeTextureFrameTimer
            >= titleFadeTextureFrameDurations[gameResultFadeTextureFrame]
        ):
            gameResultFadeTextureFrameTimer = 0
            if gameResultFadeTextureFrame < 3:
                gameResultFadeTextureFrame += 1
            else:
                gameState = RESULT_FADE_TEXTURE_REVERSE_ANIMATION
                resultFadeTextureReverseFrame = 3
                resultFadeTextureReverseFrameTimer = 0
        continue

    # Reveal the result scene after fading out the finished game scene.
    if gameState == RESULT_FADE_TEXTURE_REVERSE_ANIMATION:
        drawResultScene(resultSelectEnd, resultScoreText, 0)
        fadeTexture.setFrame(resultFadeTextureReverseFrame)
        fadeTextureMask.setFrame(resultFadeTextureReverseFrame)
        thumby.display.drawSpriteWithMask(fadeTexture, fadeTextureMask)
        thumby.display.update()

        resultFadeTextureReverseFrameTimer += 1
        if (
            resultFadeTextureReverseFrameTimer
            >= titleFadeTextureFrameDurations[resultFadeTextureReverseFrame]
        ):
            resultFadeTextureReverseFrameTimer = 0
            if resultFadeTextureReverseFrame > 0:
                resultFadeTextureReverseFrame -= 1
            else:
                gameState = RESULT
                resultSelectEnd = False
                resultScoreDigits = 0
                resultScoreFrameTimer = 0
                resultScoreInputEnabled = False
                resultScoreSaved = False
        continue

    # RESULT reveals each score digit before enabling End and Retry.
    if gameState == RESULT:
        resultLeftPressed = thumby.buttonL.justPressed()
        resultRightPressed = thumby.buttonR.justPressed()
        resultConfirmPressed = thumby.buttonA.justPressed()

        if resultScoreInputEnabled and (
            resultLeftPressed or resultRightPressed
        ):
            resultSelectEnd = not resultSelectEnd
            playSound(SOUND_CURSOR)

        drawResultScene(
            resultSelectEnd,
            resultScoreText,
            resultScoreDigits
        )
        thumby.display.update()

        if resultScoreDigits < 3:
            resultScoreFrameTimer += 1
            if resultScoreFrameTimer >= DISPLAY_FPS:
                resultScoreFrameTimer = 0
                resultScoreDigits += 1
                if resultScoreDigits < 3:
                    playSound(SOUND_CURSOR)
                else:
                    playSound(SOUND_CONFIRM)
        elif not resultScoreInputEnabled:
            # Enable input only after the hundreds digit has been drawn.
            if not resultScoreSaved:
                recordHighscore(resultScoreValue)
                resultScoreSaved = True
            resultScoreInputEnabled = True
        elif resultConfirmPressed:
            playSound(SOUND_CONFIRM)
            if resultSelectEnd:
                titleSelectStart = True
                gameState = RESULT_TITLE_FADE_TEXTURE_ANIMATION
                resultTitleFadeTextureFrame = 0
                resultTitleFadeTextureFrameTimer = 0
            else:
                gameState = RESULT_RETRY_FADE_TEXTURE_ANIMATION
                resultRetryFadeTextureFrame = 0
                resultRetryFadeTextureFrameTimer = 0
        continue

    # Fade the result scene before restarting the game.
    if gameState == RESULT_RETRY_FADE_TEXTURE_ANIMATION:
        drawResultScene(resultSelectEnd, resultScoreText, 3)
        fadeTexture.setFrame(resultRetryFadeTextureFrame)
        fadeTextureMask.setFrame(resultRetryFadeTextureFrame)
        thumby.display.drawSpriteWithMask(fadeTexture, fadeTextureMask)
        thumby.display.update()

        resultRetryFadeTextureFrameTimer += 1
        if (
            resultRetryFadeTextureFrameTimer
            >= titleFadeTextureFrameDurations[resultRetryFadeTextureFrame]
        ):
            resultRetryFadeTextureFrameTimer = 0
            if resultRetryFadeTextureFrame < 3:
                resultRetryFadeTextureFrame += 1
            else:
                resetGameplayState()
                gameState = RESULT_RETRY_FADE_TEXTURE_REVERSE_ANIMATION
                resultRetryFadeTextureReverseFrame = 3
                resultRetryFadeTextureReverseFrameTimer = 0
        continue

    # Reveal the reset game scene before showing the READY overlay.
    if gameState == RESULT_RETRY_FADE_TEXTURE_REVERSE_ANIMATION:
        retryStartPlatformActive = startPlatform.x + startPlatform.width > 0
        drawGameBackground(player, playerMask, retryStartPlatformActive)
        fadeTexture.setFrame(resultRetryFadeTextureReverseFrame)
        fadeTextureMask.setFrame(resultRetryFadeTextureReverseFrame)
        thumby.display.drawSpriteWithMask(fadeTexture, fadeTextureMask)
        thumby.display.update()

        resultRetryFadeTextureReverseFrameTimer += 1
        if (
            resultRetryFadeTextureReverseFrameTimer
            >= titleFadeTextureFrameDurations[
                resultRetryFadeTextureReverseFrame
            ]
        ):
            resultRetryFadeTextureReverseFrameTimer = 0
            if resultRetryFadeTextureReverseFrame > 0:
                resultRetryFadeTextureReverseFrame -= 1
            else:
                gameState = READY
                introTimer = 0
                playSound(SOUND_READY)
        continue

    # Fade the result scene before returning to the title scene.
    if gameState == RESULT_TITLE_FADE_TEXTURE_ANIMATION:
        drawResultScene(resultSelectEnd, resultScoreText, 3)
        fadeTexture.setFrame(resultTitleFadeTextureFrame)
        fadeTextureMask.setFrame(resultTitleFadeTextureFrame)
        thumby.display.drawSpriteWithMask(fadeTexture, fadeTextureMask)
        thumby.display.update()

        resultTitleFadeTextureFrameTimer += 1
        if (
            resultTitleFadeTextureFrameTimer
            >= titleFadeTextureFrameDurations[resultTitleFadeTextureFrame]
        ):
            resultTitleFadeTextureFrameTimer = 0
            if resultTitleFadeTextureFrame < 3:
                resultTitleFadeTextureFrame += 1
            else:
                gameState = RESULT_TITLE_TRANSITION_IMAGE_ANIMATION
                resultTitleTransitionImageFrame = 0
                resultTitleTransitionImageFrameTimer = 0
        continue

    # Play the inverted transition image before revealing the title scene.
    if gameState == RESULT_TITLE_TRANSITION_IMAGE_ANIMATION:
        resultTransitionImageInversion.setFrame(
            resultTitleTransitionImageFrame
        )
        thumby.display.drawSprite(resultTransitionImageInversion)
        thumby.display.update()

        resultTitleTransitionImageFrameTimer += 1
        if (
            resultTitleTransitionImageFrameTimer
            >= titleTransitionImageFrameDuration
        ):
            resultTitleTransitionImageFrameTimer = 0
            if resultTitleTransitionImageFrame < 4:
                resultTitleTransitionImageFrame += 1
            else:
                gameState = RESULT_TITLE_FINAL_FADE_TEXTURE_ANIMATION
                resultTitleFinalFadeTextureFrame = 3
                resultTitleFinalFadeTextureFrameTimer = 0
        continue

    # Apply the final fade sequence over the title scene.
    if gameState == RESULT_TITLE_FINAL_FADE_TEXTURE_ANIMATION:
        thumby.display.drawSprite(titleBackground)
        titleCharacter1.setFrame(titleCharacterFrame)
        titleCharacter1Mask.setFrame(titleCharacterFrame)
        thumby.display.drawSpriteWithMask(
            titleCharacter1,
            titleCharacter1Mask
        )
        thumby.display.drawSpriteWithMask(
            titleSelectUiStart,
            titleSelectUiStartMask
        )
        fadeTexture.setFrame(resultTitleFinalFadeTextureFrame)
        fadeTextureMask.setFrame(resultTitleFinalFadeTextureFrame)
        thumby.display.drawSpriteWithMask(fadeTexture, fadeTextureMask)
        thumby.display.update()

        resultTitleFinalFadeTextureFrameTimer += 1
        if (
            resultTitleFinalFadeTextureFrameTimer
            >= resultTitleFinalFadeTextureFrameDurations[
                resultTitleFinalFadeTextureFrame
            ]
        ):
            resultTitleFinalFadeTextureFrameTimer = 0
            if resultTitleFinalFadeTextureFrame > 0:
                resultTitleFinalFadeTextureFrame -= 1
            else:
                gameState = TITLE
        continue

    # START begins gameplay immediately, while the START overlay remains for 1s.
    showStart = gameState == START
    if showStart:
        introTimer += 1
        if introTimer >= INTRO_FRAMES:
            gameState = PLAYING
            introTimer = 0

    # --- Move platforms ---
    currentScrollSpeed = getStageScrollSpeed(stageLevel)
    for movingPlatform in platforms:
        movingPlatform.move(currentScrollSpeed)

    startPlatformActive = startPlatform.x + startPlatform.width > 0

    # Keep generating normal platforms so the right side remains covered.
    while platforms[-1].x + platforms[-1].width < thumby.display.width + 24:
        newPlatform = createGeneratedNormalPlatform(platforms[-1])
        platforms.append(newPlatform)

    # Remove normal platforms that leave the screen, except the current platform.
    if (
        len(platforms) > 2
        and platforms[1].x + platforms[1].width <= 0
        and platforms[1] is not currentPlatform
    ):
        platforms.pop(1)
        score += 1
        newStageLevel = getStageLevelFromScore(score)
        if newStageLevel > stageLevel:
            stageLevel = newStageLevel
            currentLevelConfig = STAGE_LEVEL_CONFIGS[stageLevel - 1]

    # Do not regenerate the start platform after it leaves the screen.
    startPlatformActive = startPlatform.x + startPlatform.width > 0

    # --- Horizontal overlap ---
    platformOverlap = (
        onPlatform
        and currentPlatform is not None
        and currentPlatform in platforms
        and playerCollisionOverlapsPlatformX(currentPlatform, playerY)
    )
    startPlatformOverlap = (
        startPlatformActive
        and playerCollisionOverlapsPlatformX(startPlatform, playerY)
    )

    # --- Leaving a platform ---
    if onPlatform and not platformOverlap:
        onPlatform = False
        currentPlatform = None
        # Only an air jump is available after leaving a platform.
        jumpCount = 1

    if onStartPlatform and not startPlatformOverlap:
        onStartPlatform = False
        jumpCount = 1

    # --- Jump with the A button ---
    if thumby.buttonA.justPressed():

        # Normal jump.
        if onStartPlatform or onPlatform:
            velocityY = jumpPower
            playSound(SOUND_JUMP)
            jumpCount = 1
            onPlatform = False
            currentPlatform = None
            onStartPlatform = False

            isHovering = False
            hoverTimer = 0.0

        # Double jump, available while hovering or rising.
        elif (
            jumpCount == 1
            and (isHovering or velocityY > 0)
        ):
            velocityY = doubleJumpPower
            playSound(SOUND_AIR_JUMP)
            jumpCount = 2

            # End the hover state.
            isHovering = False
            hoverTimer = 0

    # --- Player foot position before the update ---
    previousPlayerY = playerY

    # --- Gravity and vertical movement ---
    if not onPlatform and not onStartPlatform:

        if isHovering:
            hoverTimer += DELTA_TIME_SECONDS

            if hoverTimer >= jumpHoverTimeSeconds:
                isHovering = False
                velocityY = 0

        else:
            previousVelocityY = velocityY
            velocityY += gravity * DELTA_TIME_SECONDS

            # Hover only at the highest point of the first jump.
            if (
                jumpCount <= 2
                and previousVelocityY < 0
                and velocityY >= 0
            ):
                velocityY = 0
                isHovering = True
                hoverTimer = 0.0
            else:
                playerY += velocityY * DELTA_TIME_SECONDS

    # --- Landing detection for airborne platforms ---
    if (
        not onPlatform
        and not onStartPlatform
        and (velocityY >= 0 or isHovering)
    ):
        for candidatePlatform in platforms:
            previousCollisionBottom = getPlayerCollisionRect(previousPlayerY)[3]
            currentCollisionTop = getPlayerCollisionRect(playerY)[1]
            currentCollisionBottom = getPlayerCollisionRect(playerY)[3]
            platformBottom = candidatePlatform.y + candidatePlatform.height

            hasHorizontalOverlap = playerCollisionOverlapsPlatformX(
                candidatePlatform,
                playerY,
            )
            hasVerticalOverlap = (
                currentCollisionBottom > candidatePlatform.y
                and currentCollisionTop < platformBottom
            )
            crossedPlatformTop = (
                previousCollisionBottom <= candidatePlatform.y
                and currentCollisionBottom >= candidatePlatform.y
            )

            if (
                hasHorizontalOverlap
                and (crossedPlatformTop or hasVerticalOverlap)
            ):
                playerY = (
                    candidatePlatform.y
                    - collisionOffsetY
                    - collisionHeight
                )
                velocityY = 0
                onPlatform = True
                currentPlatform = candidatePlatform
                jumpCount = 0
                isHovering = False
                break

    # Keep the Y position fixed while on a platform.
    # Landing detection for the start platform.
    if (
        not onPlatform
        and not onStartPlatform
        and (velocityY >= 0 or isHovering)
        and startPlatformOverlap
        and (
            (
                getPlayerCollisionRect(previousPlayerY)[3] <= startPlatform.y
                and getPlayerCollisionRect(playerY)[3] >= startPlatform.y
            )
            or (
                getPlayerCollisionRect(playerY)[3] > startPlatform.y
                and getPlayerCollisionRect(playerY)[1]
                < startPlatform.y + startPlatform.height
            )
        )
    ):
        playerY = startPlatform.y - collisionOffsetY - collisionHeight
        velocityY = 0
        onStartPlatform = True
        jumpCount = 0
        isHovering = False

    if onPlatform:
        if currentPlatform is not None and currentPlatform in platforms:
            playerY = currentPlatform.y - collisionOffsetY - collisionHeight
            velocityY = 0

    # --- Ground contact ---
    if onStartPlatform:
        playerY = startPlatform.y - collisionOffsetY - collisionHeight
        velocityY = 0
        onPlatform = False
        jumpCount = 0
        isHovering = False

    # Update the player's Y coordinate.
    # Finish the game when the player leaves through the bottom of the screen.
    if playerY >= thumby.display.height:
        gameState = FINISHED
        velocityY = 0
        playSound(SOUND_FINISHED)
        continue

    player.y = int(playerY)
    playerMask.x = player.x
    playerMask.y = player.y
    playerJump.x = player.x
    playerJump.y = player.y
    playerJumpMask.x = player.x
    playerJumpMask.y = player.y
    playerFall.x = player.x
    playerFall.y = player.y
    playerFallMask.x = player.x
    playerFallMask.y = player.y

    if onPlatform or onStartPlatform:
        # Advance the running animation for each pixel of ground scroll.
        playerFrameScrollDistance += currentScrollSpeed
        while playerFrameScrollDistance >= 1.0:
            playerFrameScrollDistance -= 1.0
            playerFrame = (playerFrame + 1) % PLAYER_FRAME_COUNT
        player.setFrame(playerFrame)
        playerMask.setFrame(playerFrame)
        activePlayer = player
        activePlayerMask = playerMask
    elif isHovering or velocityY < 0:
        # Jumping uses a single static frame.
        playerJump.setFrame(0)
        playerJumpMask.setFrame(0)
        activePlayer = playerJump
        activePlayerMask = playerJumpMask
    else:
        # Falling uses a single static frame.
        playerFall.setFrame(0)
        playerFallMask.setFrame(0)
        activePlayer = playerFall
        activePlayerMask = playerFallMask

    #============================================
    # Rendering
    #============================================
    drawGameBackground(activePlayer, activePlayerMask, startPlatformActive)

    if showStart:
        thumby.display.drawSpriteWithMask(startSprite, startMaskSprite)

    thumby.display.update()
