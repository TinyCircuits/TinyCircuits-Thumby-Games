# To test run games locally: python3 -m pip install pygame                        

from cgi import print_arguments
from genericpath import isdir
import os
import shutil

# Delete the folder of previously built wasms
shutil.rmtree("Games")

# Get the list of game directories
root_contents = os.listdir()

prepend_file = open("lib/buildin_overrides.py")
prepend_contents = prepend_file.read()
prepend_file.close()



def convert_file_contents(file_contents, functions_to_await, is_main=True):
    converted_game_contents = ""
    for line in file_contents:

        if "global" in line and is_main:
            # Replace global keywords with nonlocal since functions are now defined in function main
            line = line.replace("global", "nonlocal")
        if "thumby.display.update()" in line:
            # Async sleep is defined in update but it needs awaited using async def main():
            line = line.replace("thumby.display.update()", "await thumby.display.update()")
        if "@micropython.native" in line:
            # Remove decorator (needs done for viper too but there are other things to remove, maybe look into how to define blank decorators with the same names)
            line = line.replace("@micropython.native", "")
        if "@micropython.viper" in line:
            line = line.replace("@micropython.viper", "")
        if ":int" in line:
            line = line.replace(":int", "")
        # if "def" in line and "__init__" not in line:
        #     line = line.replace("def", "async def")
        #     functions_to_await.append(line[line.find("def ")+len("def "):line.rfind("(")])
        
        if(is_main):
            converted_game_contents += "\t" + line
        else:
            converted_game_contents += line

    # file_contents = converted_game_contents.splitlines()

    # converted_game_contents = ""
    # for line in file_contents:
    #     for func in functions_to_await:
    #         if (func + "(" in line or func + " (" in line ) and ("async def " + func not in line) and ("await" not in line) and ("thumby.display." + func not in line):

    #             # Find the index of the function in the string and traverse left until likely not related to calling the function
    #             func_index = line.find(func) - 1
    #             while func_index > -1 and line[func_index] != ' ' and line[func_index] != '\t' and line[func_index] != '-' and line[func_index] != '(':
    #                 func_index = func_index - 1
                
    #             line = line[0:func_index+1] + "await " + line[func_index+1:]
    #     converted_game_contents += line
    
    return converted_game_contents



# One by one build the wasm directories
for game_dir in root_contents:

    functions_to_await = []

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
                        f_contents = f.readlines()
                        f.close()

                        f = open("Games/" + game_dir + "/" + file_name, "w")
                        f.write(convert_file_contents(f_contents, functions_to_await, False))
                        f.close()


        # Copy over libs to a lib folder
        shutil.copytree("lib", "Games/" + game_dir + "/lib")

        # Read the game contents
        game_file = open(game_dir + "/" + game_dir + ".py", "r")
        game_contents = game_file.readlines()
        game_file.close()

        # Make the wasm output main file as required by pygbag: https://pypi.org/project/pygbag/
        wasm_file = open("Games/" + game_dir + "/main.py", "w")

        # Start building the file by adding imports
        wasm_file.write("import asyncio\n")
        wasm_file.write("import pygame\n")
        wasm_file.write("import os\n")
        wasm_file.write("import sys\n\n")

        # Add path for custom thumby module
        wasm_file.write("sys.path.append(\"lib\")\n\n")

        # Add overrides/re-defines
        wasm_file.write(prepend_contents + "\n\n")

        # Change root directory
        wasm_file.write("os.chdir(sys.path[0])" + "\n\n\n")
        

        # Add main loop
        wasm_file.write("async def main():\n")
            
        
        wasm_file.write(convert_file_contents(game_contents, functions_to_await))
        
        wasm_file.write("\nasyncio.run(main())")

        wasm_file.close()
