class DisplayInterface:
    def setFont(self, path, width, height, spacing):
        raise NotImplementedError

    def fill(self, color):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def drawLine(self, x0, y0, x1, y1, color):
        raise NotImplementedError

    def drawText(self, text, x, y, color):
        raise NotImplementedError

    def blit(self, data, x, y, width, height, key, flip_x, flip_y):
        raise NotImplementedError

    def setPixel(self, x, y, color):
        raise NotImplementedError


class ButtonInterface:
    def pressed(self):
        raise NotImplementedError

    def justPressed(self):
        raise NotImplementedError


class SaveDataInterface:
    def setName(self, name):
        raise NotImplementedError

    def hasItem(self, name):
        raise NotImplementedError

    def getItem(self, name):
        raise NotImplementedError

    def setItem(self, name, value):
        raise NotImplementedError

    def delItem(self, name):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError


class GameInterface:
    def __init__(
        self,
        display: DisplayInterface,
        save_data: SaveDataInterface,
        buttons: dict,
    ):
        self.display = display
        self.saveData = save_data
        self.buttonU = buttons["U"]
        self.buttonD = buttons["D"]
        self.buttonL = buttons["L"]
        self.buttonR = buttons["R"]
        self.buttonA = buttons["A"]
        self.buttonB = buttons["B"]


class ThumbyInterface(GameInterface):
    def __init__(self):
        import thumby

        super().__init__(
            display=thumby.display,
            save_data=thumby.saveData,
            buttons={
                "U": thumby.buttonU,
                "D": thumby.buttonD,
                "L": thumby.buttonL,
                "R": thumby.buttonR,
                "A": thumby.buttonA,
                "B": thumby.buttonB,
            },
        )


def get_interface(interface_id="thumby"):
    interface_id = interface_id.lower()
    interfaces = {
        "thumby": ThumbyInterface,
    }
    if interface_id not in interfaces:
        raise ValueError("Unknown interface: {}".format(interface_id))
    return interfaces[interface_id]()
