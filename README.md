# TinyCircuits-Thumby-Games

Repository of TinyCircuits and community made Thumby games.

Games that live here can be seen in the web IDE (https://code.thumby.us/) using arcade (click "Arcade" in the top bar). 

Games can be downloaded directly to Thumby from the Arcade or opened in the IDE editors.

# Getting your game ready for the Arcade

[Extended documentation of below directions with pictures available here](https://thumby.us/Code-Editor/Submit-Game/) from the Thumby Docs site: [https://thumby.us/](https://thumby.us/)

* Some files in your game directory need to have a certain name and location
    * A Python file with the same name as the game root directory is required. For example, if a game is called `TinyBlocks` then the main game source file needs to be called `TinyBlocks.py`, this ensures the game shows up on the Thumby start screen
    * Two extra files are required for your game to show up on the arcade and should be located in the root of your game directory
        * A `.png` (image) or `.webm` (video) of gameplay. The filename does not matter, but arcade_title_video.webm or arcade_title_image.png is preferred. A file extension is required. If both files are present, the .webm will be used instead of the .png for display in the web IDE arcade. Please keep image and video resolution between anything from 8x (576x320px) to 16x (1152x640px).
        * A description file named exactly `arcade_description.txt`. Markdown files will not work. This description is displayed when a user hovers over the game in the Arcade.

Below is an example of how a game should be structured:
```
TinyBlocks
    - arcade_description.txt
    - arcade_title_video.webm
    - TinyBlocks.py
```
NOTE: Other files and directories are allowed in your game, the above shows the required items and locations.

# Getting your game on the Arcade
1. Submit a pull request to this repository with your game directory added ([GitHub making a pull request](https://www.google.com/search?q=github+making+a+pull+request&rlz=1C1GCEA_enUS850US850&oq=github+making+a+pull+request&aqs=chrome..69i57j0i22i30l9.918j0j9&sourceid=chrome&ie=UTF-8))
2. Wait for TinyCircuits to review and accept the PR
3. Wait for the URL builder GitHub action to build the new URL list (should take minutes)
4. Access the [web IDE](https://code.thumby.us/) and click the "Arcade" button to view and find you game (at this point if you can see it, anyone else can as well)
5. Refresh the arcade using F5 for the page or using the arcade refresh button if you do not see your game

# Editing or removing your game from the Arcade
The same process as adding a game, just submit a pull request with the edits.
