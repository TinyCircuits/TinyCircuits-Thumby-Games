import ujson
from thumbyGraphics import display

class AnimationPlayer:
    def __init__(self, model_name, pos, file_path):
        self.model_name = model_name
        self.pos = pos
        self.frameIndex = 0
        self.counter = 0
        
        self.models = {}
        try:
            with open(file_path, "r") as file:
                self.models = ujson.load(file)
                print(f"Loaded models: {self.models}")
        except Exception as e:
            print(f"Error loading JSON file: {e}")
        
        if model_name not in self.models:
            raise KeyError(f"Model name '{model_name}' not found in models. Available models: {list(self.models.keys())}")
        self.bones = self.models[self.model_name]["bones"]
        self.animations = self.models[self.model_name]["animations"]
        self.last_frame_positions = [None] * len(self.bones)

    def drawCustomLine(self, x0, y0, x1, y1, color):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            display.setPixel(x0, y0, color)
            
            if x0 == x1 and y0 == y1:
                break
            
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def animate(self, thisAnimation, lastAnimAtion, player_pos, frameStep):
        if thisAnimation not in self.animations:
            raise KeyError(f"Animation '{thisAnimation}' not found in model '{self.model_name}'. Available animations: {list(self.animations.keys())}")
        
        if thisAnimation != lastAnimAtion:
            self.counter = 0
            self.frameIndex = 0
        
        animation = self.animations[thisAnimation]
        frameCount = len(animation)
        
        self.counter += 1
        if self.counter >= frameStep:
            self.counter = 0
            self.frameIndex = (self.frameIndex + 1) % frameCount
        
        currentFrame = animation[self.frameIndex]
    
        bone_positions = []
        for i in range(len(self.bones)):
            bone_base = self.bones[i]["offset"]
            bone_offset = currentFrame[i]
            pos_x = player_pos[0] + self.pos[0] + bone_base[0] + bone_offset[0]
            pos_y = player_pos[1] + self.pos[1] + bone_base[1] + bone_offset[1]
            bone_positions.append((pos_x, pos_y))
            display.setPixel(pos_x, pos_y, 1)
    
        for i in range(len(self.bones)):
            if self.bones[i].get("smearable", 0) == 1:
                if self.last_frame_positions[i] is not None:
                    last_pos_x, last_pos_y = self.last_frame_positions[i]
                    current_pos_x, current_pos_y = bone_positions[i]
                    
                    self.drawCustomLine(last_pos_x, last_pos_y, current_pos_x, current_pos_y, 1)
    
        self.last_frame_positions = bone_positions.copy()
    
        for bone in self.bones:
            bone_id = bone["id"]
            connects_to_id = bone["connects_to"]
    
            start_x, start_y = bone_positions[bone_id]
            end_x, end_y = bone_positions[connects_to_id]
            
            self.drawCustomLine(start_x, start_y, end_x, end_y, 1)
    
        display.drawText(f"Frame: {self.frameIndex}", 2, 2, 1)
        display.drawText(f"Counter: {self.counter}", 2, 10, 1)
