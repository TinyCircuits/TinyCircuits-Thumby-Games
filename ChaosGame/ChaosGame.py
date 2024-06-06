while(1):
    import thumby
    import random
    thumby.display.setFPS(15)
    thumby.display.fill(0)
    thumby.display.update
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
    StartingPoints = 3
    R = 0.5
    while(1):
        thumby.display.fill(0)
        thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
        thumby.display.drawText("Vertices", 21, 10, 1)
        thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
        thumby.display.drawText(str(StartingPoints), 35, 20, 1)
        if thumby.buttonU.justPressed():
            StartingPoints = StartingPoints + 1
            if (StartingPoints >= 9):
                StartingPoints = 8
        if thumby.buttonR.justPressed():
            StartingPoints = StartingPoints + 1
            if (StartingPoints >= 9):
                StartingPoints = 8
        if thumby.buttonD.justPressed():
            StartingPoints = StartingPoints - 1
            if (StartingPoints <= 2):
                StartingPoints = 3
        if thumby.buttonL.justPressed():
            StartingPoints = StartingPoints - 1
            if (StartingPoints <= 2):
                StartingPoints = 3
                
        if thumby.buttonA.justPressed():
            break
        thumby.display.update()
    while(1):
        thumby.display.fill(0)
        thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
        thumby.display.drawText("Ratio", 27, 10, 1)
        thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
        thumby.display.drawText(str(R), 28, 20, 1)
        if thumby.buttonU.justPressed():
            R = round(R, 2) + 0.05
            if (R >= 1):
                R = 1
        if thumby.buttonR.justPressed():
            R = round(R, 2) + 0.05
            if (R >= 1):
                R = 1
        if thumby.buttonD.justPressed():
            R = round(R, 2) - 0.05
            if (R <= 0):
                R = 0
        if thumby.buttonL.justPressed():
            R = round(R, 2) - 0.05
            if (R <= 0):
                R = 0
                
        if thumby.buttonA.justPressed():
            break
        thumby.display.update()
    thumby.display.setFPS(0)
    thumby.display.fill(0)
    thumby.display.update()
    if (StartingPoints == 3):
        point1X = 36
        point2X = 14
        point3X = 58
        point1Y = 0
        point2Y = 39
        point3Y = 39
        pointX = 0
        pointY = 0
        AllPoints = [[point1X, point1Y], [point2X, point2Y], [point3X, point3Y]]
        thumby.display.setPixel(point1X, point1Y, 1)
        thumby.display.setPixel(point2X, point2Y, 1)
        thumby.display.setPixel(point3X, point3Y, 1)
        
    if (StartingPoints == 4):
        point1X = 16
        point2X = 16
        point3X = 53
        point4X = 53
        point1Y = 0
        point2Y = 39
        point3Y = 0
        point4Y = 39
        pointX = 0
        pointY = 0
       # R = 0.6
        AllPoints = [[point1X, point1Y], [point2X, point2Y], [point3X, point3Y], [point4X, point4Y]]
        thumby.display.setPixel(point1X, point1Y, 1)
        thumby.display.setPixel(point2X, point2Y, 1)
        thumby.display.setPixel(point3X, point3Y, 1)
        thumby.display.setPixel(point4X, point4Y, 1)
    
    if (StartingPoints == 5):
        point1X = 36
        point2X = 14
        point3X = 58
        point4X = 23
        point5X = 48
        point1Y = 0
        point2Y = 16
        point3Y = 16
        point4Y = 39
        point5Y = 39
        pointX = 0
        pointY = 0
        #R = 0.618
        AllPoints = [[point1X, point1Y], [point2X, point2Y], [point3X, point3Y], [point4X, point4Y], [point5X, point5Y]]
        thumby.display.setPixel(point1X, point1Y, 1)
        thumby.display.setPixel(point2X, point2Y, 1)
        thumby.display.setPixel(point3X, point3Y, 1)
        thumby.display.setPixel(point4X, point4Y, 1)
        thumby.display.setPixel(point5X, point5Y, 1)
        
    if (StartingPoints == 6):
        point1X = 25
        point2X = 47
        point3X = 14
        point4X = 58
        point5X = 25
        point6X = 47
        point1Y = 0
        point2Y = 0
        point3Y = 19
        point4Y = 19
        point5Y = 39
        point6Y = 39
        pointX = 36
        pointY = 39
        AllPoints = [[point1X, point1Y], [point2X, point2Y], [point3X, point3Y], [point4X, point4Y], [point5X, point5Y], [point6X, point6Y]]
        thumby.display.setPixel(point1X, point1Y, 1)
        thumby.display.setPixel(point2X, point2Y, 1)
        thumby.display.setPixel(point3X, point3Y, 1)
        thumby.display.setPixel(point4X, point4Y, 1)
        thumby.display.setPixel(point5X, point5Y, 1)
        thumby.display.setPixel(point6X, point6Y, 1)
    if (StartingPoints == 7):
        point1X = 26
        point2X = 46
        point3X = 16
        point4X = 56
        point5X = 20
        point6X = 52
        point7X = 36
        point1Y = 39
        point2Y = 39
        point3Y = 24
        point4Y = 24
        point5Y = 8
        point6Y = 8
        point7Y = 0
        pointX = 36
        pointY = 39
        AllPoints = [[point1X, point1Y], [point2X, point2Y], [point3X, point3Y], [point4X, point4Y], [point5X, point5Y], [point6X, point6Y], [point7X, point7Y]]
        thumby.display.setPixel(point1X, point1Y, 1)
        thumby.display.setPixel(point2X, point2Y, 1)
        thumby.display.setPixel(point3X, point3Y, 1)
        thumby.display.setPixel(point4X, point4Y, 1)
        thumby.display.setPixel(point5X, point5Y, 1)
        thumby.display.setPixel(point6X, point6Y, 1)
        thumby.display.setPixel(point7X, point7Y, 1)
    if (StartingPoints == 8):
        point1X = 28
        point2X = 44
        point3X = 16
        point4X = 56
        point5X = 16
        point6X = 56
        point7X = 28
        point8X = 44
        point1Y = 39
        point2Y = 39
        point3Y = 27
        point4Y = 27
        point5Y = 12
        point6Y = 12
        point7Y = 0
        point8Y = 0
        pointX = 36
        pointY = 39
        AllPoints = [[point1X, point1Y], [point2X, point2Y], [point3X, point3Y], [point4X, point4Y], [point5X, point5Y], [point6X, point6Y], [point7X, point7Y], [point8X, point8Y]]
        thumby.display.setPixel(point1X, point1Y, 1)
        thumby.display.setPixel(point2X, point2Y, 1)
        thumby.display.setPixel(point3X, point3Y, 1)
        thumby.display.setPixel(point4X, point4Y, 1)
        thumby.display.setPixel(point5X, point5Y, 1)
        thumby.display.setPixel(point6X, point6Y, 1)
        thumby.display.setPixel(point7X, point7Y, 1)
        thumby.display.setPixel(point8X, point8Y, 1)
    
    while(1):
        randomPoint1 = random.choice(AllPoints)
        AllPoints.remove(randomPoint1)
        if (pointX == 0):
            randomPoint2 = random.choice(AllPoints)
        if (pointX >= 1):
            randomPoint2 = [pointX, pointY]
        pointX = (R * randomPoint1[0] + (1 - R) * randomPoint2[0])
        pointY = (R * randomPoint1[1] + (1 - R) * randomPoint2[1])
        thumby.display.setPixel(round(pointX), round(pointY), 1)
        thumby.display.update()
        if (StartingPoints == 3):
            AllPoints = [[point1X, point1Y], [point2X, point2Y], [point3X, point3Y], [pointX, pointY]]
        if (StartingPoints == 4):
            AllPoints = [[point1X, point1Y], [point2X, point2Y], [point3X, point3Y], [point4X, point4Y], [pointX, pointY]]
        if (StartingPoints == 5):
            AllPoints = [[point1X, point1Y], [point2X, point2Y], [point3X, point3Y], [point4X, point4Y], [point5X, point5Y], [pointX, pointY]]   
        if (StartingPoints == 6):
            AllPoints = [[point1X, point1Y], [point2X, point2Y], [point3X, point3Y], [point4X, point4Y], [point5X, point5Y], [point6X, point6Y], [pointX, pointY]] 
        if (StartingPoints == 7):
            AllPoints = [[point1X, point1Y], [point2X, point2Y], [point3X, point3Y], [point4X, point4Y], [point5X, point5Y], [point6X, point6Y], [point7X, point7Y], [pointX, pointY]]
        if (StartingPoints == 8):
            AllPoints = [[point1X, point1Y], [point2X, point2Y], [point3X, point3Y], [point4X, point4Y], [point5X, point5Y], [point6X, point6Y], [point7X, point7Y], [point8X, point8Y], [pointX, pointY]]
        
        if thumby.buttonA.justPressed():
            break