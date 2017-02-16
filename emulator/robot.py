from math import pi, cos, sin, radians, degrees, asin, acos, atan, sqrt


# rotates vector against the clock
def rotate(v, angle, in_degrees=True, return_complex=True):
    if in_degrees:
        angle = radians(angle)
    if isinstance(v, complex):
        v = v.real, v.imag
    x, y = v
    x_new = x*cos(angle) - y*sin(angle)
    y_new = x*sin(angle) + y*cos(angle)
    if return_complex:
        return complex(x_new, y_new)
    return x_new, y_new


def translate(v, point):
    if isinstance(v, complex) and isinstance(point, complex):
        return v - point
    if isinstance(v, complex) and isinstance(point, tuple):
        return v - complex(point[0], point[1])
    if isinstance(v, tuple) and isinstance(point, tuple):
        return v[0]-point[0], v[1]-point[1]
    raise ValueError("translate: invalid argument type")


# angle in degrees
def rotate_about_point(v, rotation_point, angle):
    if isinstance(v, tuple):
        v = complex(v[0], v[1])
    if isinstance(rotation_point, tuple):
        rotation_point = complex(rotation_point[0], rotation_point[1])
    # translate to point
    v = translate(v, rotation_point)
    # rotate in new system of axes
    v = rotate(v, angle)
    # translate to initial system of axes
    v = translate(v, -rotation_point)
    return v


class Robot:
    # the width of each wheel is 2 (ref. specification.pdf)
    width = 10
    height = 8
    d = 8  # the distance between the center of left and center of right wheel
    speed_coefficient = 0.07
    _angle_left2center_left_wheel = degrees(atan(1/6.5))
    _distance_top_left2center_left_wheel = sqrt(6.5**2 + 1)

    def __init__(self):
        self._l_power = 0  # power of the left engine (from -100 to 100)
        self._r_power = 0  # power of the right engine (from -100 to 100)
        self._top_left = complex(0, self.height)
        self._angle = 0  # against the clock in degrees, range [0..359]

        self._distance_per_tick = 0

        # # For not to count them every tick
        # self._update_le_values = True
        # self._update_re_values = True
        # self._update_be_values = True
        #
        # # self._le_turning_radius = 0  # in case of left_engine_forward
        # self._le_turning_angle = 0  # in case of left_engine_forward
        # self._le_coords_delta = complex(0, 0)  # in case of left_engine_forward
        #
        # # self._re_turning_radius = 0  # in case of right_engine_forward
        # self._re_turning_angle = 0  # in case of right_engine_forward
        # self._re_coords_delta = complex(0, 0)   # in case of right_engine_forward
        #
        # # self._be_turning_radius = 0  # in case of both_engines_forward
        # self._be_turning_angle = 0  # in case of both_engines_forward
        # self._be_coords_delta = complex(0, 0)   # in case of both_engines_forward

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
        dx = Robot.width*sin(radians(angle))
        dy = Robot.width*cos(radians(angle))
        bottom_right = complex(top_left[0], top_left[1]) + complex(dx, dy)
        bottom_right = bottom_right.real, bottom_right.imag
        return top_left, bottom_right

    def left_engine_forward(self):
        l_speed = self._get_distance_per_tick(self._l_power)
        cx, dphi = self._get_rotation_parameters(l_speed, 0)
        new_pos = rotate_about_point(self._top_left, cx,  -dphi)
        angle = self._angle_to_defined_range(self._angle - dphi)
        new_pos = new_pos.real, new_pos.imag
        return new_pos, angle

    def left_engine_backward(self):
        l_speed = self._get_distance_per_tick(self._l_power)
        cx, dphi = self._get_rotation_parameters(l_speed, 0)
        new_pos = rotate_about_point(self._top_left, cx, dphi)
        angle = self._angle_to_defined_range(self._angle + dphi)
        new_pos = new_pos.real, new_pos.imag
        return new_pos, angle

    def right_engine_forward(self):
        return self._top_left, self._angle
        r_speed = self._get_distance_per_tick(self._r_power)
        if self._update_le_values:
            pos, dphi = self._get_rotation_parameters(0, r_speed)
            self._re_turning_angle = dphi
            # self._re_coords_delta = self._top_left - pos
        angle = self._angle_to_defined_range(self._angle + (90 - self._le_turning_angle))
        # pos = self._top_left + self._re_coords_delta
        # pos = pos.real, pos.imag
        self._update_re_values = False
        return self._top_left, angle

    def right_engine_backward(self):
        return self._top_left, self._angle
        r_speed = self._get_distance_per_tick(self._r_power)
        if self._update_le_values:
            pos, dphi = self._get_rotation_parameters(0, r_speed)
            self._re_turning_angle = dphi
            # self._re_coords_delta = self._top_left - pos
        angle = self._angle_to_defined_range(self._angle - (90 - self._le_turning_angle))
        # pos = self._top_left - self._re_coords_delta
        # pos = pos.real, pos.imag
        return self._top_left, angle

    def both_engines_forward(self):
        if self._l_power == self._r_power:
            pos = self._top_left + self._get_coords_delta_no_rotation()
        else:
            # r_speed = self._get_distance_per_tick(self._r_power)
            # l_speed = self._get_distance_per_tick(self._l_power)
            # pos, dphi = self._get_rotation_parameters(l_speed, r_speed)
            return self._top_left, self._angle
        if self._l_power != self._r_power:
            # angle = self._angle_to_defined_range(self._angle + (90 - self._be_turning_angle))
            pass
        else:
            angle = self._angle
        pos = pos.real, pos.imag
        return pos, angle

    def both_engines_backward(self):
        if self._l_power == self._r_power:
            pos = self._top_left - self._get_coords_delta_no_rotation()
        else:
            # r_speed = self._get_distance_per_tick(self._r_power)
            # l_speed = self._get_distance_per_tick(self._l_power)
            # pos, dphi = self._get_rotation_parameters(l_speed, r_speed)
            return self._top_left, self._angle
        if self._l_power != self._r_power:
            # angle = self._angle_to_defined_range(self._angle - (90 - self._be_turning_angle))
            pass
        else:
            angle = self._angle
        pos = pos.real, pos.imag
        return pos, angle

    def change_left_engine_power(self, value):
        value = int(value)
        if value > 100 or value < -100:
            raise ValueError("Incorrect engine power value")
        self._l_power = value
        # Changing distance per tick
        self._distance_per_tick = self._get_distance_per_tick(self._l_power, self._r_power)

    def change_right_engine_power(self, value):
        value = int(value)
        if value > 100 or value < -100:
            raise ValueError("Incorrect engine power value")
        self._r_power = value
        # Changing distance per tick
        self._distance_per_tick = self._get_distance_per_tick(self._l_power, self._r_power)

    # Returns lines speed depending on one of both engine powers and speed coefficient
    # If both power values are supplied, returns the line speed of the pin center
    def _get_distance_per_tick(self, power1, power2=None):
        if power2 is not None:
            return ((power1 + power2) / 2) * self.speed_coefficient
        else:
            return power1 * self.speed_coefficient

    # Returns coordinates of rotation point and rotation angle
    def _get_rotation_parameters(self, l_speed, r_speed):
        dl = l_speed
        dr = r_speed
        cx = (dr * self.d)/(dl-dr) + self.d
        alpha = degrees(atan(dl / cx))

        lc = self._get_left_wheel_center()
        cx = translate((cx, 0), (-lc.real, -lc.imag))
        cx = rotate(cx, -self._angle)

        return cx, alpha

    def _get_left_wheel_center(self):
        c = complex(1, -6.5)
        c = translate(c, -self._top_left)
        c = rotate(c, -self._angle)
        return c

    def _get_coords_delta_no_rotation(self):
        if self._angle == 0 or self._angle == 180:
            dx = 0
            dy = self._distance_per_tick * cos(radians(self._angle))  # to multiply by -1 if necessary
        elif self._angle == 90 or self._angle == 270:
            dx = self._distance_per_tick * sin(radians(self._angle))  # to multiply by -1 if necessary
            dy = 0
        else:
            dx = self._distance_per_tick*sin(radians(self._angle))
            dy = self._distance_per_tick*cos(radians(self._angle))

        result = complex(dx*-1, dy)
        return result

    def make_step(self, top_left, angle):
        if isinstance(top_left, complex):
            self._top_left = top_left
        else:
            self._top_left = complex(top_left[0], top_left[1])

        self._angle = self._angle_to_defined_range(angle)
        # self._update_be_values = True
        # self._update_re_values = True
        # self._update_le_values = True

    def get_state(self):
        pos = self._top_left.real, self._top_left.imag
        return pos, self._angle
