from math import pi, cos, sin


class Robot:
    # the width of each wheel is 2 (ref. specification.pdf)
    width = 10
    height = 8
    d = 8  # the distance between the center of left and center of right wheel
    speed_coefficient = 0.7

    def __init__(self):
        self._l_power = 0  # power of the left engine (from -100 to 100)
        self._r_power = 0  # power of the right engine (from -100 to 100)
        self._left_top_pos = complex(0, self.height)
        self._angle = 0  # against the clock in degrees, range [0..359]

        self._distance_per_tick = 0

        # For not to count them every tick
        self._update_le_values = True
        self._update_re_values = True
        self._update_be_values = True

        # self._le_turning_radius = 0  # in case of left_engine_forward
        self._le_turning_angle = 0  # in case of left_engine_forward
        self._le_coords_delta = complex(0, 0)  # in case of left_engine_forward

        # self._re_turning_radius = 0  # in case of right_engine_forward
        self._re_turning_angle = 0  # in case of right_engine_forward
        self._re_coords_delta = complex(0, 0)   # in case of right_engine_forward

        # self._be_turning_radius = 0  # in case of both_engines_forward
        self._be_turning_angle = 0  # in case of both_engines_forward
        self._be_coords_delta = complex(0, 0)   # in case of both_engines_forward

    @staticmethod
    def _angle_to_defined_range(angle):
        while angle < 0:
            angle += 360
        while angle >= 360:
            angle -= 360
        return angle

    #  Returns top left and right bottom corners coords from top left coord and angle
    @staticmethod
    def coords_from_state(top_left, angle):
        dx = Robot.width*sin(angle)
        dy = Robot.width*cos(angle)
        bottom_right = complex(top_left[0], top_left[1]) + complex(dx, dy)
        bottom_right = bottom_right.real, bottom_right.imag
        return top_left, bottom_right

    def left_engine_forward(self):
        if self._update_le_values:
            turning_radius = self._get_turning_radius(self._l_power, 0)
            self._le_turning_angle = self._get_turning_angle(turning_radius)
            self._le_coords_delta = self._get_coords_delta(turning_radius, self._le_turning_angle)
        angle = self._angle_to_defined_range(self._angle - (90 - self._le_turning_angle))
        pos = self._left_top_pos + self._le_coords_delta
        pos = pos.real, pos.imag
        self._update_le_values = False
        return pos, angle

    def left_engine_backward(self):
        if self._update_le_values:
            turning_radius = self._get_turning_radius(self._l_power, 0)
            self._le_turning_angle = self._get_turning_angle(turning_radius)
            self._le_coords_delta = self._get_coords_delta(turning_radius, self._le_turning_angle)
        angle = self._angle_to_defined_range(self._angle + (90 - self._le_turning_angle))
        pos = self._left_top_pos - self._le_coords_delta
        pos = pos.real, pos.imag
        self._update_le_values = False
        return pos, angle

    def right_engine_forward(self):
        if self._update_re_values:
            turning_radius = self._get_turning_radius(0, self._r_power)
            self._re_turning_angle = self._get_turning_angle(turning_radius)
            self._re_coords_delta = self._get_coords_delta(turning_radius, self._re_turning_angle)
        angle = self._angle_to_defined_range(self._angle + (90 - self._le_turning_angle))
        pos = self._left_top_pos + self._re_coords_delta
        pos = pos.real, pos.imag
        self._update_re_values = False
        return pos, angle

    def right_engine_backward(self):
        if self._update_re_values:
            turning_radius = self._get_turning_radius(0, self._r_power)
            self._re_turning_angle = self._get_turning_angle(turning_radius)
            self._re_coords_delta = self._get_coords_delta(turning_radius, self._re_turning_angle)
        angle = self._angle_to_defined_range(self._angle - (90 - self._le_turning_angle))
        pos = self._left_top_pos - self._re_coords_delta
        pos = pos.real, pos.imag
        self._update_re_values = False
        return pos, angle

    def both_engines_forward(self):
        if self._update_re_values or self._update_le_values:
            turning_radius = self._get_turning_radius(self._l_power, self._r_power)
            self._be_turning_angle = self._get_turning_angle(turning_radius)
            self._be_coords_delta = self._get_coords_delta(turning_radius, self._be_turning_angle)
        angle = self._angle_to_defined_range(self._angle - (90 - self._be_turning_angle))
        pos = self._left_top_pos + self._be_coords_delta
        pos = pos.real, pos.imag
        self._update_be_values = False
        return pos, angle

    def both_engines_backward(self):
        if self._update_re_values or self._update_le_values:
            turning_radius = self._get_turning_radius(self._l_power, self._r_power)
            self._be_turning_angle = self._get_turning_angle(turning_radius)
            self._be_coords_delta = self._get_coords_delta(turning_radius, self._be_turning_angle)
        angle = self._angle_to_defined_range(self._angle + (90 - self._be_turning_angle))
        pos = self._left_top_pos - self._be_coords_delta
        pos = pos.real, pos.imag
        self._update_be_values = False
        return pos, angle

    def change_left_engine_power(self, value):
        value = int(value)
        if value > 100 or value < -100:
            raise ValueError("Incorrect engine power value")
        self._l_power = value
        # Changing distance per tick
        self._distance_per_tick = ((self._l_power + self._r_power) / 2) * self.speed_coefficient
        self._update_le_values = True

    def change_right_engine_power(self, value):
        value = int(value)
        if value > 100 or value < -100:
            raise ValueError("Incorrect engine power value")
        self._r_power = value
        # Changing distance per tick
        self._distance_per_tick = ((self._l_power + self._r_power) / 2) * self.speed_coefficient
        self._update_re_values = True

    @staticmethod
    def _get_coords_delta(radius, angle):
        x = radius - radius * cos(angle)
        y = radius * sin(angle)
        return x, y

    def _get_turning_radius(self, l_power, r_power):
        return (self.d ** 2 + r_power ** 2 - l_power ** 2) / 2 * self.d + 1

    # returns value in degrees
    def _get_turning_angle(self, radius):
        return (self._distance_per_tick * 180) / (pi * radius)

    def set_state(self, left_top_pos, angle):
        self._left_top_pos = complex(left_top_pos[0], left_top_pos[1])
        self._angle = angle

    def get_state(self):
        pos = self._left_top_pos.real, self._left_top_pos.imag
        return pos, self._angle
