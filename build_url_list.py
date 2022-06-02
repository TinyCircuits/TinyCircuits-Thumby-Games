# https://canovasjm.netlify.app/2020/11/29/github-actions-run-a-python-script-on-schedule-and-commit-changes/

import os
import datetime
from posixpath import dirname
print("Starting URL list builder using Python in GH Action...")

# Each game's asset is appended to the end of this, like https://raw.githubusercontent.com/TinyCircuits/TinyCircuits-Thumby-Games/master/MyGame/MyGame.py
raw_url_base = "https://raw.githubusercontent.com/TinyCircuits/TinyCircuits-Thumby-Games/master/"

# Open file that urls will be written to
f = open("url_list.txt", "w")

def addDirFilesToList(path, childDir=False):
    if childDir == False:
        f.write("NAME=" + path + "\n")
    items = os.listdir(path)
    for item in items:
        abs_path = path + "/" + item
        if os.path.isdir(abs_path):
            addDirFilesToList(abs_path, True)
        else:
            f.write(raw_url_base + abs_path + "\n")


topLevelItems = os.listdir()
unsortedPairs = []
for item in topLevelItems:
    if os.path.isdir(item) and item != ".github" and item != ".git":
        pipe = os.popen("git log -- \"" + item + "\"").read()
        print("Loaded " + item)
        if len(pipe) == 0:
            continue
        try:
            for line in pipe.splitlines():
                if line[:4] == "Date":    
                    dateStr = line[8:]
                    break
        except IndexError:
            print(str(item) + " Has malformed git log!")
        print(dateStr)
        try:
            date = datetime.datetime.strptime(dateStr, '%a %b %d %H:%M:%S %Y %z')
        except:
            print("ERROR")
        unsortedPairs.append((date, item))


sortedPairsNewestAtLast = sorted(unsortedPairs, key=lambda x: x[0])
sortedPairsNewestAtLast.reverse()

for pair in sortedPairsNewestAtLast:
    addDirFilesToList(pair[1])
    f.write("\n")

f.close()