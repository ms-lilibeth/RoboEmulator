class Robot:
    _angle = 0
    _lu_position = None  # position of the left upper corner
    _l_power = 0  # power of the left engine (from -100 to 100)
    _r_power = 0  # power of the right engine (from -100 to 100)

    def __init__(self):
        pass

    def left_engine_forward(self):
        pass

    def left_engine_backward(self):
        pass

    def right_engine_forward(self):
        pass

    def right_engine_backward(self):
        pass

    def both_engines_forward(self):
        pass

    def both_engines_backward(self):
        pass

    def change_left_engine_power(self, value):
        value = int(value)
        if value > 100 or value < -100:
            raise ValueError("Incorrect engine power value")
        self._l_power = value

    def change_right_engine_power(self, value):
        value = int(value)
        if value > 100 or value < -100:
            raise ValueError("Incorrect engine power value")
        self._r_power = value
