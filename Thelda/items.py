from thumby import Sprite

class Heart_Container:
    def __init__(self, x, y, identity):
        self.x = x
        self.y = y
        self.identity = identity
        self.item_type = "heartcontainer"
        self.item = bytearray([25,22,13,22,25])
        # self.item_mask = bytearray([6,15,30,15,6])
        self.sprite = Sprite(5, 5, self.item, self.x, self.y, key=1)