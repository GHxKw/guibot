# Copyright 2013 Intranet AG / Thomas Jarosch
#
# guibender is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# guibender is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with guibender.  If not, see <http://www.gnu.org/licenses/>.
#
import autopy.screen
from image import Image

class Screen:
    def __init__(self):
        screen_size = autopy.screen.get_size()

        self.width = screen_size[0]
        self.height = screen_size[1]

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def capture(self, *args):
        if len(args) == 4:
            xpos = args[0]
            ypos = args[1]
            width = args[2]
            height = args[3]
        elif len(args) == 1:
            region = args[0]
            xpos = region.get_x()
            ypos = region.get_y()
            width = region.get_width()
            height = region.get_height()
        else:
            xpos = 0
            ypos =  0
            width = self.width
            height = self.height

        # clipping
        if xpos > self.width:
            xpos = self.width - 1
        if ypos > self.height:
            ypos = self.height - 1

        if xpos + width > self.width:
            width = self.width - xpos
        if ypos + height > self.height:
            height = self.height - ypos

        autopy_bmp = autopy.bitmap.capture_screen(((xpos, ypos), (width, height)))

        return Image(None, Image.DEFAULT_SIMILARITY, autopy_bmp)

# break circular dependency
from region import Region