
        
# Add common but missing functions to time module (from redefined/recreated micropython module)
import asyncio
import pygame
import os
import sys

sys.path.append("lib")

import time
import utime

time.ticks_ms = utime.ticks_ms
time.ticks_us = utime.ticks_us
time.ticks_diff = utime.ticks_diff
time.sleep_ms = utime.sleep_ms


# See thumbyGraphics.__init__() for set_mode() call
pygame.init()
pygame.display.set_caption("Thumby game")

# Common overrides to get scripts working in the browsers. This should be prepended to each file in the game

# Re-define the open function to create a directory for a file if it doesn't already exist (mimic MicroPython)
def open(path, mode):
    import builtins
    from pathlib import Path
    
    filename = Path(path)
    filename.parent.mkdir(parents=True, exist_ok=True)

    return builtins.open(path, mode)

os.chdir(sys.path[0])


async def main():
	# Simple Mandelbrot zoomer (fixed point integer 13 bits for fractions)
	# Daniel Spångberg 
	
	"""
	    This program is free software: you can redistribute it and/or modify
	    it under the terms of the GNU General Public License as published by
	    the Free Software Foundation, either version 3 of the License, or
	    (at your option) any later version.
	
	    This program is distributed in the hope that it will be useful,
	    but WITHOUT ANY WARRANTY; without even the implied warranty of
	    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	    GNU General Public License for more details.
	
	    You should have received a copy of the GNU General Public License
	    along with this program.  If not, see <https://www.gnu.org/licenses/>.
	"""
	
	import thumby
	
	
	
	def mandel(afix, bfix, niter) -> bool:
	    i=0
	    x0=0
	    y0=0
	    term=4*8192
	    while i<niter:
	        x0_2=(x0*x0)>>13
	        y0_2=(y0*y0)>>13
	        x0y0=(x0*y0)>>13
	        if x0_2+y0_2>term:
	            break
	        x0=x0_2-y0_2+afix
	        y0=x0y0+x0y0+bfix
	        i+=1
	    if i==niter:
	        return True
	    else:
	        return False
	        
	        
	w=thumby.display.width
	h=thumby.display.height
	
	thumby.display.setFPS(60)
	
	thumby.display.fill(0)
	await thumby.display.update()
	
	
	zoom=4.
	a=0
	b=0
	niter=500
	
	changed=True
	
	while True:
	    if changed:
	        thumby.display.fill(0)
	        await thumby.display.update()
	
	        dx=zoom/w
	        dy=zoom/h
	    
	        for y in range(h):
	            for x in range(w):
	                a0=-0.5*zoom+a+x*dx
	                b0=-0.5*zoom+b+y*dy
	                if mandel(int(a0*8192.),int(b0*8192.),int(niter)):
	                    thumby.display.setPixel(x,y,0)
	                else:
	                    thumby.display.setPixel(x,y,1)
	            await thumby.display.update()
	        changed=False
	        
	        
	    if thumby.buttonA.justPressed():
	        zoom*=0.25
	        changed=True
	    
	    if thumby.buttonB.justPressed():
	        zoom*=4.
	        changed=True
	        
	    if thumby.buttonL.justPressed():
	        a-=0.25*zoom
	        changed=True
	    
	    if thumby.buttonR.justPressed():
	        a+=0.25*zoom
	        changed=True
	    
	    if thumby.buttonU.justPressed():
	        b-=0.25*zoom
	        changed=True
	    
	    if thumby.buttonD.justPressed():
	        b+=0.25*zoom
	        changed=True
	    
	
	        
	

asyncio.run(main())