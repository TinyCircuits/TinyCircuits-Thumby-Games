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


def get_functions_to_await(file_str, functions_to_await, structure, game_dir):
    

    def test_add_to_await(func, structure):
        function_name = ""

        if "ast.Attribute" in str(func):
            function_name = func.attr
        elif "ast.Name" in str(func):
            function_name = str(func.id)
        
        structure["calls"].append(function_name)

        # If this called function was update or one that called update, make sure its parents are in the to await list
        if function_name == "update" or function_name == "pressed" or function_name in functions_to_await:
            s = structure
            while s["parent"] != None:
                if s["name"] not in functions_to_await:
                    functions_to_await.append(s["name"])
                s = s["parent"]


    def recursive_find(body, structure):
        for statement in body:
            if "ast.FunctionDef" in str(statement):
                next_structure = {"parentName": structure["name"], "parent": structure, "name": statement.name, "defs": [], "calls": []}
                structure["defs"].append(next_structure)
                recursive_find(statement.body, next_structure)
            elif ("ast.Expr" in str(statement) or "ast.Return" in str(statement)) and "ast.Call" in str(statement.value):
                test_add_to_await(statement.value.func, structure)
            elif "ast.If" in str(statement):
                if hasattr(statement.test, "values"):
                    for value in statement.test.values:
                        if "ast.Call" in str(value):
                            test_add_to_await(value.func, structure)
                recursive_find(statement.body, structure)

            elif hasattr(statement, "body"):
            # elif "ast.Class" in str(statement) or "ast.While" in str(statement) or "ast.For" in str(statement) or "ast.If" in str(statement):
                recursive_find(statement.body, structure)

    try:
        recursive_find(ast.parse(file_str).body, structure)
    except Exception as e:
        print("ERROR: " + game_dir + " -> " + str(e))



def convert_file_contents(file_contents, functions_to_await, is_main=True):
    converted_game_contents = ""

    for line_number in range(0, len(file_contents), 1):
        line = file_contents[line_number]

        if "global" in line and is_main:
            # Replace global keywords with nonlocal since functions are now defined in function main
            line = line.replace("global", "nonlocal")
        if "thumby.display.update()" in line:
            # Async sleep is defined in update but it needs awaited using async def main():
            line = line.replace("thumby.display.update()", "await thumby.display.update()")
        if "thumby.buttonA.pressed()" in line:
            line = line.replace("thumby.buttonA.pressed()", "await thumby.buttonA.pressed()")
        if "thumby.buttonB.pressed()" in line:
            line = line.replace("thumby.buttonB.pressed()", "await thumby.buttonB.pressed()")
        if "thumby.buttonU.pressed()" in line:
            line = line.replace("thumby.buttonU.pressed()", "await thumby.buttonU.pressed()")
        if "thumby.buttonD.pressed()" in line:
            line = line.replace("thumby.buttonD.pressed()", "await thumby.buttonD.pressed()")
        if "thumby.buttonL.pressed()" in line:
            line = line.replace("thumby.buttonL.pressed()", "await thumby.buttonL.pressed()")
        if "thumby.buttonR.pressed()" in line:
            line = line.replace("thumby.buttonR.pressed()", "await thumby.buttonR.pressed()")
        if "@micropython.native" in line:
            # Remove decorator (needs done for viper too but there are other things to remove, maybe look into how to define blank decorators with the same names)
            line = line.replace("@micropython.native", "")
        if "@micropython.viper" in line:
            line = line.replace("@micropython.viper", "")
        if ":int" in line:
            line = line.replace(":int", "")
        if ("ptr8(") in line:
            start_index = line.find("ptr8(")
            end_index = line.find(")", start_index)

            line = line[0:start_index] + line[start_index+5:end_index] + line[end_index+1:]
        
        for func in functions_to_await:
            if "def " + func in line:
                line = line.replace("def " + func, "async def " + func, -1)
            elif func in line:
                line = line.replace(func, "await " + func, -1)

        if(is_main):
            converted_game_contents += "\t" + line
        else:
            converted_game_contents += line
    
    return converted_game_contents



sortedPairsNewestAtLast = sorted(unsortedPairs, key=lambda x: x[0])
sortedPairsNewestAtLast.reverse()



for pair in sortedPairsNewestAtLast:
    
    game_name = pair[1]

    file_paths = []
    addDirFilesToList(game_name, False, file_paths)
    
    functions_to_await = []

    # Now that only the files for the game are found, copy them to the build folder
    file_path: str
    for file_path in file_paths:
        sub_path = file_path[0:file_path.rfind("/")]
        
        os.makedirs("APKS/building/Games/" + sub_path, exist_ok=True)
        shutil.copyfile(file_path, "APKS/building/Games/" + file_path)

        # Get functions to await and from all files and then use it later
        if ".py" in file_path:
            f = open("APKS/building/Games/" + file_path, "r")
            structure = {"parent": None, "name": None, "defs": [], "calls": []}
            try:
                get_functions_to_await(f.read(), functions_to_await, structure, file_path)
            except Exception as e:
                print(str(e))
            f.close()

    if "TinyHeli" in file_path:
        print("")
        print("")
        pprint.pprint(structure)
        print("")
        print("")
        print(functions_to_await)
        print("")
        print("")

    # Game folder copied with just the game files and none of the arcade images/txt, convert to async
    for file_path in file_paths:
        if ".py" in file_path:
            f = open("APKS/building/Games/" + file_path, "r")
            file_lines = f.readlines()
            f.close()

            f = open("APKS/building/Games/" + file_path, "w")
            if game_name in file_path:
                f.write(convert_file_contents(file_lines, functions_to_await))
            else:
                f.write(convert_file_contents(file_lines, functions_to_await), False)
            f.close()


    # Now that all functions are awaited, make the main entry point file as required by pygbag: https://pypi.org/project/pygbag/
    f = open("APKS/building/Games/" + game_name + "/" + game_name + ".py", "r")
    file_lines = f.readlines()
    f.close()

    wasm_file = open("APKS/building/Games/" + game_name + "/" + game_name + ".py", "w")

    wasm_file.write("""
        
# Add common but missing functions to time module (from redefined/recreated Micropython module)
import asyncio
import pygame
import os
import sys

sys.path.append(\"lib\")

import time
import utime

time.ticks_ms = utime.ticks_ms
time.ticks_us = utime.ticks_us
time.ticks_diff = utime.ticks_diff
time.sleep_ms = utime.sleep_ms


# See thumbyGraphics.__init__() for set_mode() call
pygame.init()
pygame.display.set_caption("Thumby game")

""")
    

    # Add main loop
    wasm_file.write("async def main():\n")
        
    for line in file_lines:
        wasm_file.write(line)
    
    wasm_file.write("\nasyncio.run(main())")

    wasm_file.close()

    url_list_file.write("\n")

url_list_file.close()


main_file = open("APKS/building/main.py", "w")
main_file.write("""
print(\"DUMMY MAIN RAN!\")
"""
)
main_file.close()

# Make the web build containing all apks
os.system("pygbag --build --ume_block 0 " + "APKS/building/")

# Copy APK file out of build dir
shutil.copyfile("APKS/building/build/web/building.apk", "APKS/" + "building" + ".apk")

# Delete everything used for building
shutil.rmtree("APKS/building/Games")
shutil.rmtree("APKS/building/build")
os.remove("APKS/building/main.py")