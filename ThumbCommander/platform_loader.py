# platform_loader.py - Updated with memory-efficient imports using try/except
import sys
import gc
import micropython
from thumbyButton import ButtonClass

# Platform detection
IS_THUMBY_COLOR = False

try:
    import engine_io
    IS_THUMBY_COLOR = True
except ImportError:
    from thumbyHardware import swL, swR, swU, swD, swA, swB

# Get platform constants
from platform_constants import get_constants
PC = get_constants(IS_THUMBY_COLOR)

# Initialize all variables to None first
display = None
Sprite = None
rumble = None
audio_load = None
audio_play = None
audio_stop = None
audio_set_volume = None
audio_set_loop = None
audio_get_position = None
audio_set_end_callback = None
audio_clear_end_callback = None
audio_open_id = None
audio_play_id = None
audio_close_ids = None
play_cutscene_animation = None
create_cancel_callback = None
create_sprite = None

# Platform-specific imports using try/except
if IS_THUMBY_COLOR:
    buttonA = ButtonClass(engine_io.A)
    buttonB = ButtonClass(engine_io.B)
    buttonU = ButtonClass(engine_io.UP)
    buttonD = ButtonClass(engine_io.DOWN)
    buttonL = ButtonClass(engine_io.LEFT)
    buttonR = ButtonClass(engine_io.RIGHT)
    buttonLB = ButtonClass(engine_io.LB)
    buttonRB = ButtonClass(engine_io.RB)
    buttonMENU = ButtonClass(engine_io.MENU)
    # Try to import ThumbyColor display and sprite classes
    try:
        from thumbycolor_native import ColorDisplay, ColorSprite, _rumble, create_sprite as _create_sprite
        display = ColorDisplay()
        Sprite = ColorSprite
        rumble = _rumble
        create_sprite = _create_sprite
        print(f"ThumbyColor display initialized. Free memory: {gc.mem_free()}")
    except ImportError as e:
        print(f"Warning: Could not import thumbycolor_native: {e}")
    
    try:
        from audio import (load, play, stop, set_volume, set_loop, get_position, set_end_callback, clear_end_callback, open_id, play_id, close_ids)        
        audio_load = load
        audio_play = play
        audio_stop = stop
        audio_set_volume = set_volume
        audio_set_loop = set_loop
        audio_get_position = get_position
        audio_set_end_callback = set_end_callback
        audio_clear_end_callback = clear_end_callback
        audio_open_id = open_id
        audio_play_id = play_id
        audio_close_ids = close_ids
        from cutscene_utils import init_cutscene_utils, play_cutscene_animation as _play_cutscene, create_cancel_callback as _create_cancel
        play_cutscene_animation = _play_cutscene
        create_cancel_callback = _create_cancel
        init_cutscene_utils(display, PC, audio_load, audio_play, audio_stop, buttonMENU)
        print(f"Audio and Color Cutscene initialized. Free memory: {gc.mem_free()}")
    except ImportError as e:
        print(f"Warning: Could not import audio module or color_cutscene: {e}")
  
# original Thumby
else:
    from grayscale import display as _display, Sprite as _Sprite, create_sprite as _create_sprite  
    display = _display
    Sprite = _Sprite
    create_sprite = _create_sprite
    buttonA = ButtonClass(swA) # Left (A) button
    buttonB = ButtonClass(swB) # Right (B) button
    buttonU = ButtonClass(swU) # D-pad up
    buttonD = ButtonClass(swD) # D-pad down
    buttonL = ButtonClass(swL) # D-pad left
    buttonR = ButtonClass(swR) # D-pad right
    buttonLB = buttonL
    buttonRB = buttonR
    buttonMENU = buttonB
    
    from os import stat
    class CancelCallback:
        __slots__ = ('counter',)
        def __init__(self):
            self.counter = 0
        def __call__(self, _):
            self.counter += 1
            if self.counter >= 6:
                self.counter = 0
                if buttonB and buttonB.justPressed():
                    return False
            return True
    
    def create_cancel_callback():
        return CancelCallback()
    
    def play_cutscene_animation(filename, fps=20, frame_callback=None):
        """Play grayscale sprite animation for Thumby (no audio support)"""
        from gc import collect
        
        # Use the global display instance
        global display
        
        # Set FPS
        display.setFPS(fps)
        
        # Check if .SHD file exists (required for grayscale)
        shd_filename = filename.replace('.BIT.bin', '.SHD.bin')
        
        try:
            # Parse dimensions from filename
            parts = filename.split('_')
            if len(parts) >= 3:
                try:
                    width = int(parts[-2])
                    height = int(parts[-1].replace('.BIT.bin', ''))
                except ValueError:
                    # Default dimensions if parsing fails
                    width, height = 74, 30
            else:
                width, height = 74, 30
            
            # Center the animation
            x = (PC.WIDTH - width) // 2
            y = (PC.HEIGHT - height) // 2
            
            # Calculate buffer size for grayscale bitmap
            bitmap_byte_count = width * ((height + 7) // 8)
            
            with open(filename, 'rb') as bit_file, open(shd_filename, 'rb') as shd_file:
                # Calculate frame count from file size
                file_size = stat(filename)[6]
                frame_count = file_size // bitmap_byte_count
                
                print(f"Playing grayscale cutscene: {width}x{height}, {frame_count} frames")
                
                # Create reusable buffers
                bit_buffer = bytearray(bitmap_byte_count)
                shd_buffer = bytearray(bitmap_byte_count)
                
                # Play each frame
                for frame_idx in range(frame_count):
                    display.fill(0)
                    
                    # Read frame data
                    bit_file.readinto(bit_buffer)
                    shd_file.readinto(shd_buffer)
                    
                    # Use display's native blit for grayscale
                    display.blit((bit_buffer, shd_buffer), x, y, width, height, -1, 0, 0)
                    display.update()
                    # Handle frame callback for cancellation
                    if frame_callback:
                        if not frame_callback(frame_idx):
                            break
                # Clean up
                del bit_buffer, shd_buffer
                collect()
                
        except Exception as e:
            print(f"Error playing grayscale cutscene\n{filename}:\n{e}")
        
    print(f"Thumby display initialized. Free memory: {gc.mem_free()}")

# Helper functions
@micropython.native
def dpadPressed():
    """Returns true if any dpad buttons are currently pressed on the thumby."""
    return (buttonU.pressed() or buttonD.pressed() or buttonL.pressed() or buttonR.pressed())
  
@micropython.native
def inputJustPressed():
    """Returns true if any buttons were just pressed on the thumby."""
    return (buttonA.justPressed() or buttonB.justPressed() or buttonU.justPressed() or 
            buttonD.justPressed() or buttonL.justPressed() or buttonR.justPressed() or 
            buttonLB.justPressed() or buttonRB.justPressed() or buttonMENU.justPressed())