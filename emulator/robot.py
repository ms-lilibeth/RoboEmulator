from math import pi, cos, sin


class Robot:
    width = 10
    height = 8
    d = 8  # the distance between the center of left and center of right wheel
    speed_coefficient = 0.7

    def __init__(self):
        # depict_callback = depict_callback

        self._l_power = 0  # power of the left engine (from -100 to 100)
        self._r_power = 0  # power of the right engine (from -100 to 100)

        self._distance_per_tick = 0  # = max(l_power, r_power)*speed_coefficient
        # the width of each wheel is 2 (ref. specification.pdf)

        # For not to count them every tick
        self._le_power_changed = True
        self._re_power_changed = True

        self._le_turning_radius = 0  # in case of left_engine_forward
        self._le_turning_angle = 0  # in case of left_engine_forward
        self._le_coords_delta = 0  # in case of left_engine_forward

        self._re_turning_radius = 0  # in case of right_engine_forward
        self._re_turning_angle = 0  # in case of right_engine_forward
        self._re_coords_delta = 0  # in case of right_engine_forward

        self._be_turning_radius = 0  # in case of both_engines_forward
        self._be_turning_angle = 0  # in case of both_engines_forward
        self._be_coords_delta = 0  # in case of both_engines_forward

    def left_engine_forward(self, return4coords=True):
        if self._le_power_changed:
            self._le_turning_radius = self._get_turning_radius(self._l_power, 0)
            self._le_turning_angle = self._get_turning_angle(self._le_turning_radius)
            self._le_coords_delta = self._get_coords_delta(self._le_turning_radius, self._le_turning_angle)
        # return new position

    def left_engine_backward(self, return4coords=True):
        print("LE bwd")
        pass

    def right_engine_forward(self, return4coords=True):
        print("RE fwd")
        pass

    def right_engine_backward(self, return4coords=True):
        print("RE bwd")
        pass

    def both_engines_forward(self, return4coords=True):
        print("BE fwd")
        pass

    def both_engines_backward(self, return4coords=True):
        print("BE bwd")
        pass

    def change_left_engine_power(self, value):
        value = int(value)
        if value > 100 or value < -100:
            raise ValueError("Incorrect engine power value")
        self._l_power = value
        # Changing distance per tick
        self._distance_per_tick = max(self._l_power, self._r_power) * self.speed_coefficient

        self._le_power_changed = True

    def change_right_engine_power(self, value):
        value = int(value)
        if value > 100 or value < -100:
            raise ValueError("Incorrect engine power value")
        self._r_power = value
        # Changing distance per tick
        self._distance_per_tick = max(self._l_power, self._r_power) * self.speed_coefficient
        self._re_power_changed = True

    def _get_turning_radius(self, l_power, r_power):
        return (self.d ** 2 + r_power ** 2 - l_power ** 2) / 2 * self.d + 1

    # returns value in degrees
    def _get_turning_angle(self, radius):
        return (self._distance_per_tick * 180) / (pi * radius)

    @staticmethod
    def _get_coords_delta(radius, angle):
        x = radius - radius*cos(angle)
        y = radius*sin(angle)
        return x, y

    @staticmethod
    def _get4coords(pos, angle, rotation_point):
        pass

    def update_coords(self, left_top_pos, angle):
        pass
