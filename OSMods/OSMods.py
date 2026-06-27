from machine import reset
from os import rmdir, remove

source_path = "/Games/OSMods/menu.py"
destination_path = "/menu.py"

with open(source_path, 'r') as src, open(destination_path, 'w') as dest:
    for line in src:
        dest.write(line)
remove('/Games/OSMods/OSMods.py')
remove('/Games/OSMods/menu.py')
rmdir('/Games/OSMods')
reset()