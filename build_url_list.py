# https://canovasjm.netlify.app/2020/11/29/github-actions-run-a-python-script-on-schedule-and-commit-changes/

from __future__ import print_function
import os
import shutil
import datetime
from posixpath import dirname
import ast
import pprint
print("Starting URL list builder using Python in GH Action...")

# Each game's asset is appended to the end of this, like https://raw.githubusercontent.com/TinyCircuits/TinyCircuits-Thumby-Games/master/MyGame/MyGame.py
raw_url_base = "https://raw.githubusercontent.com/TinyCircuits/TinyCircuits-Thumby-Games/master/"

# Open file that urls will be written to
url_list_file = open("url_list.txt", "w")

def addDirFilesToList(path, childDir, file_paths):
    if childDir == False:
        url_list_file.write("NAME=" + path + "\n")
    items = os.listdir(path)
    for item in items:
        abs_path = path + "/" + item
        
        if os.path.isdir(abs_path):
            addDirFilesToList(abs_path, True, file_paths)
        else:
            if ".webm" not in abs_path and ".png" not in abs_path and "arcade_description.txt" not in abs_path:
                file_paths.append(abs_path)

            url_list_file.write(raw_url_base + abs_path + "\n")


topLevelItems = os.listdir()
unsortedPairs = []
for item in topLevelItems:
    if os.path.isdir(item) and item != ".github" and item != ".git" and item != "APKS":
        pipe = os.popen("git log -- \"" + item + "\"").read()
        # print("Loaded " + item)
        if len(pipe) == 0:
            continue
        try:
            for line in pipe.splitlines():
                if line[:4] == "Date":    
                    dateStr = line[8:]
                    break
        except IndexError:
            print(str(item) + " Has malformed git log!")
        # print(dateStr)
        try:
            date = datetime.datetime.strptime(dateStr, '%a %b %d %H:%M:%S %Y %z')
        except:
            print("ERROR")
        unsortedPairs.append((date, item))



sortedPairsNewestAtLast = sorted(unsortedPairs, key=lambda x: x[0])
sortedPairsNewestAtLast.reverse()



for pair in sortedPairsNewestAtLast:
    game_name = pair[1]
    file_paths = []

    addDirFilesToList(game_name, False, file_paths)

    url_list_file.write("\n")
    
    
url_list_file.close()