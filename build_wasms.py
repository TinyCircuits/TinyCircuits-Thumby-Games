# To test run games locally: python3 -m pip install pygame                        

from cgi import print_arguments
from genericpath import isdir
import os
from pprint import pprint
import shutil
import ast



# Delete the folder of previously built wasms
shutil.rmtree("Games")

# Get the list of game directories
root_contents = os.listdir()



# One by one build the wasm directories
for game_dir in root_contents:

    functions_to_await = []
    all_converted_game_file_paths = []

    # Avoid non-game folders and files
    if game_dir != "Games" and game_dir != "lib" and game_dir != ".github" and game_dir != ".git" and isdir(game_dir):

        # Make sure the path is created
        try:
            os.makedirs("Games/" + game_dir)
        except:
            print("Games/" + game_dir + ": folder already exists, did not create again")
        

        # Copy over the rest of the files
        for file_name in os.listdir(game_dir):
            if isdir(game_dir + "/" + file_name) == False:
                # Only copy if not the file that will be made into main.py, not the .txt description for the arcade, and not a .webm video file
                if file_name != "arcade_description.txt" and ".webm" not in file_name and ".png" not in file_name and file_name != game_dir + ".py":
                    shutil.copyfile(game_dir + "/" + file_name, "Games/" + game_dir + "/" + file_name)

                    if ".py" in file_name:
                        f = open("Games/" + game_dir + "/" + file_name, "r")
                        structure = {"parent": None, "name": None, "defs": [], "calls": []}
                        get_functions_to_await(f.read(), functions_to_await, structure, file_name)
                        f.seek(0)
                        f_contents = f.readlines()
                        f.close()

                        f = open("Games/" + game_dir + "/" + file_name, "w")
                        all_converted_game_file_paths.append("Games/" + game_dir + "/" + file_name)
                        f.write(convert_file_contents(f_contents, functions_to_await, False))
                        f.close()


        # Copy over libs to a lib folder
        shutil.copytree("lib", "Games/" + game_dir + "/lib")

        # Read the game contents
        game_file = open(game_dir + "/" + game_dir + ".py", "r")
        structure = {"parent": None, "name": None, "defs": [], "calls": []}
        get_functions_to_await(game_file.read(), functions_to_await, structure, game_dir)
        game_file.seek(0)
                    
        # print(ast.parse(game_file.read()).body[0])
        game_contents = game_file.readlines()
        game_file.close()

        # Make the wasm output main file as required by pygbag: https://pypi.org/project/pygbag/
        wasm_file = open("Games/" + game_dir + "/main.py", "w")
        all_converted_game_file_paths.append("Games/" + game_dir + "/main.py")

        wasm_file.write("""
        
# Add common but missing functions to time module (from redefined/recreated micropython module)
import asyncio
import pygame
import os
import sys


# Re-define the open function to create a directory for a file if it doesn't already exist (mimic MicroPython)
def open(path, mode):
    import builtins
    from pathlib import Path
    
    filename = Path(path)
    filename.parent.mkdir(parents=True, exist_ok=True)

    return builtins.open(path, mode)


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
        # Change root directory
        wasm_file.write("os.chdir(sys.path[0])" + "\n\n\n")
        

        # Add main loop
        wasm_file.write("async def main():\n")
            
        
        wasm_file.write(convert_file_contents(game_contents, functions_to_await))
        
        wasm_file.write("\nasyncio.run(main())")

        wasm_file.close()


        # Now that all functions to await are collected and all files written, go through collected Python file paths and add async and await to those functions
        for file_path in all_converted_game_file_paths:
            f = open(file_path, "r")
            contents = f.read()
            f.close()

            for func in functions_to_await:
                contents = contents.replace("def " + func, "async def " + func, -1)
            
            f = open(file_path, "w")
            f.write(contents)
            f.close()
        

        for file_path in all_converted_game_file_paths:
            f = open(file_path, "r")
            lines = f.readlines()
            f.close()

            converted = ""
            for line in lines:
                for func in functions_to_await:
                    if func in line and "def " + func not in line:
                        start_col = line.find(func)
                        while start_col > 0 and line[start_col] != ' ' and line[start_col] != '\t':
                            start_col = start_col - 1

                        line = line[0:start_col+1] + "await " + line[start_col+1:]

                converted += line
            
            f = open(file_path, "w")
            f.write(converted)
            f.close()
        
        # Make the web build and apk
        os.system("pygbag --build --ume_block 0 Games/" + game_dir)