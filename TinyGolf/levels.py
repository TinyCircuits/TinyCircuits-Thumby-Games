# TinyGolf
# Copyright Daniel Schroeder 2023
#
# This file is part of TinyGolf.
#
# TinyGolf is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# TinyGolf is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# TinyGolf. If not, see <https://www.gnu.org/licenses/>.

# - COMMENTS REMOVED TO SAVE SPACE -
# For commented version, see https://github.com/dan5sch/thumby-mini-golf-public

class LevelInfo:
    def __init__(self, offset_bytes, num_chunks, mask_layer_tee, par, xw_tee,
                 yw_tee, xw_hole, yw_hole):
        self.offset_bytes = offset_bytes
        self.num_chunks = num_chunks
        self.mask_layer_tee = mask_layer_tee
        self.par = par
        self.xw_tee = xw_tee
        self.yw_tee = yw_tee
        self.xw_hole = xw_hole
        self.yw_hole = yw_hole

levels = [
    LevelInfo(0, 80, 1, 3, 68, 129, 205, 88),
    LevelInfo(640, 72, 1, 3, 182, 92, 337, 61),
    LevelInfo(1216, 105, 5, 3, 105, 62, 275, 96),
    LevelInfo(2056, 85, 1, 2, 184, 82, 80, 103),
    LevelInfo(2736, 127, 5, 5, 74, 123, 217, 201),
    LevelInfo(3752, 99, 1, 4, 225, 189, 307, 170),
    LevelInfo(4544, 91, 1, 3, 103, 218, 306, 203),
    LevelInfo(5272, 145, 5, 3, 60, 76, 224, 76),
    LevelInfo(6432, 123, 1, 6, 133, 211, 250, 98),
]
