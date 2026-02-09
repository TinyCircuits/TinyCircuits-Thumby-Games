import time
import thumby
import math
from random import randint

restartBmp = bytearray([240,12,2,2,1,1,1,1,1,2,2,12,240,0,1,6,8,8,16,16,16,0,0,14,12,10,1,0])
restartSprite = thumby.Sprite(14,14,restartBmp)
returnBmp = bytearray([0,4,14,21,4,4,4,4,4,4,4,8,8,240,0,0,0,0,2,2,2,2,2,2,2,1,1,0])
returnSprite = thumby.Sprite(14,14,returnBmp)
restartSprite.x = 72-14
restartSprite.y = 9
returnSprite.x = 0
returnSprite.y = 9
def drawSorting():
    thumby.display.fill(0) # Fill canvas to black
    thumby.display.drawText("A",62,0,1)
    thumby.display.drawText("B",4,0,1)
    thumby.display.drawSprite(restartSprite)
    thumby.display.drawSprite(returnSprite)
arr = list(range(1,41))
def shuffle(seq):
    for _ in range(200):
        i,j = randint(0,len(seq)-1),randint(0,len(seq)-1)
        seq[i],seq[j] = seq[j],seq[i]
sortingOps = []
thumby.display.setFPS(60)
def quicksort(i=0,j=39):
    if j-i < 1:return
    mid = (i+j)//2
    partition = arr[mid]
    l = i
    r = j
    while l < r:
        while arr[l] < partition:
            l += 1
        while arr[r] > partition:
            r -= 1
        if l < r:
            swap(l,r)
    quicksort(i,r)
    quicksort(r+1,j)

def heapify(n, i):
  largest = i
  left = i*2 + 1
  right = i*2 + 2
  if left < n and arr[left] > arr[largest]:
    largest = left
  if right < n and arr[right] > arr[largest]:
    largest = right
  if largest != i:
    swap(i, largest)
    heapify(n, largest)
def heapSort():
  for i in range(40<<1 - 1,-1,-1):
    heapify(40, i)
  for i in range(39,0,-1):
    swap(0, i)
    heapify(i, 0)
  return arr

def bubbleSort():
  sorts = 1
  while sorts > 0:
    sorts = 0
    for i in range(1,40):
      if (arr[i] < arr[i-1]):
        swap(i,i-1)
        sorts += 1

def mergeSort(oglow=0,oghigh=-1):
    if oghigh == -1: oghigh=39
    high,low=oghigh,oglow
    while high-low > 0:
        mid = (oghigh-oglow)//2 + oglow
        mergeSort(oglow,mid)
        mid = (oghigh-oglow)//2 + oglow
        mergeSort(mid+1,oghigh)
        mid = (oghigh-oglow)//2 + oglow
        start2 = mid + 1
        if arr[mid] <= arr[start2]: break
        while low <= mid and start2 <= high:
            if arr[low] <= arr[start2]: low += 1
            else:
                shiftDown(low,start2)
                low += 1
                mid += 1
                start2 += 1
        break

def combSort():
  length = 40
  shrink = 1.3
  gap = length
  sorted = False
  while not sorted:
    gap = int(gap/shrink)
    if gap <= 1:
      sorted = True
      gap = 1
    for i in range(40-gap):
        sm = gap + i
        if arr[i] > arr[sm]:
            swap(i,sm)
            sorted = False
def bitonicSort():
    k = 2
    while k <= 32:
        j = k//2
        while j > 0:
            for i in range(32):
                l = i ^ j
                if (l > i):
                    if ( ((i&k)==0) and (arr[i] > arr[l]) or ( ( (i&k)!=0) and (arr[i] < arr[l])) ):
                        swap(i,l)
            j //= 2
        k *= 2
def cocktailShakerSort():
    isSorted = False
    while (not isSorted):
        isSorted = True
        for i in range(39):
            if arr[i] > arr[i + 1]:
                swap(i,i+1)
                isSorted = False
        if (isSorted): break
        isSorted = True
        for j in range(39,0,-1):
            if (arr[j-1] > arr[j]):
                swap(j,j-1)
                isSorted = False

def swap(i,j):
    arr[i],arr[j] = arr[j],arr[i]
    sortingOps.append((i,j))
def shiftDown(i,j):
    sortingOps.append((i,j))
    temp = arr[j]
    for k in range(j,i,-1):
        arr[k] = arr[k-1]
    arr[i] = temp
count = 0
sortingOps = []
sorts = {
    "Quicksort":quicksort,
    "Merge Sort":mergeSort,
    "Heapsort":heapSort,
    "Bubble Sort":bubbleSort,
    "Cocktail Sh":cocktailShakerSort,
    "Comb Sort":combSort,
    "Bitonic":bitonicSort,
}
options = ["Quicksort","Merge Sort","Heapsort","Bubble Sort","Cocktail Sh","Comb Sort","Bitonic"]
FPSs = [10,10,15,30,30,10,20]
def drawMenu():
    thumby.display.fill(0) # Fill canvas to black
    for i in range(offset,min(len(options),offset+5)):
        thumby.display.drawText((">" if selected == i else " ") + options[i],0,(i-offset)*8,1)
state = "menu"
selected = 0
offset = 0
drawMenu()
pressing = False
while(1):
    t0 = time.ticks_ms()   # Get time (ms)
    restarting = False
    if state == "sorting":
        if count < len(sortingOps):
            i,j = sortingOps[count]
            while i == j and count < len(sortingOps):
                count += 1
                i,j = sortingOps[count]
            if j != i:
                if selected == 1:
                    temp = duplicate[j]
                    for k in range(j,i,-1):
                        duplicate[k] = duplicate[k-1]
                    duplicate[i] = temp
                    thumby.audio.play(int((2**(temp/40))*440), int(900/FPSs[selected]))
                    for k in range(i,j+1):
                        thumby.display.drawLine(16+k,0,16+k,39,0)
                        thumby.display.drawLine(16+k,40-duplicate[k],16+k,39,1)
                else:
                    duplicate[i],duplicate[j] = duplicate[j],duplicate[i]
                    thumby.audio.play(int(2**(min(duplicate[i],duplicate[j])/40)*440), int(900/FPSs[selected]))
                    thumby.display.drawLine(16+i,0,16+i,39,0)
                    thumby.display.drawLine(16+i,40-duplicate[i],16+i,39,1)
                    thumby.display.drawLine(16+j,0,16+j,39,0)
                    thumby.display.drawLine(16+j,40-duplicate[j],16+j,39,1)
            count += 1
        if thumby.buttonA.pressed():
            restarting = True
        if thumby.buttonB.pressed() or restarting:
            state = "menu"
            thumby.display.setFPS(60)
            drawMenu()
    if state == "menu":
        if thumby.buttonU.pressed():
            if not pressing:
                pressing = True
                selected = max(0,selected-1)
                if selected < offset:
                   offset -= 1
                drawMenu()
        elif thumby.buttonD.pressed():
            if not pressing:
                pressing = True
                selected = min(len(options)-1,selected+1)
                if selected > offset+4:
                   offset += 1
                drawMenu()
        elif thumby.buttonA.pressed() or restarting:
            state = "sorting"
            drawSorting()
            if options[selected] in ["Bitonic"]:
               arr = list(range(1,33))
            else:
               arr = list(range(1,41))
            shuffle(arr)
            sortingOps = []
            duplicate = arr[:]
            count = 0
            for i,val in enumerate(arr):
                thumby.display.drawLine(16+i,40-val,16+i,39,1)
            thumby.display.setFPS(FPSs[selected])
            sorts[options[selected]]()
        else:
           pressing = False
    thumby.display.update()
