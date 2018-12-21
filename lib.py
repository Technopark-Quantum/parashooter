from math import sin, cos, atan2, pi, sqrt
#внутренняя библиотека игры.
def get_angle(cord1,cord2):
    x1, y1 = cord1
    x2, y2 = cord2
    x = x1 - x2
    y = y1 - y2
    rads = atan2(-y,x)
    rads %= 2*pi
    return rads

def get_velocity(angle,speed):
    velocity = (
        speed * cos(angle),
        speed * sin(angle))
    return velocity