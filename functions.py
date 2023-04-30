import math

import pygame

radius = 250

def toRadian(theta):
    return theta * math.pi / 180

def toDegrees(theta):
    return theta * 180 / math.pi

def angle_of_vector(x, y):
    return pygame.math.Vector2(x, y).angle_to((1, 0))

def getAngle(pos1, pos2):
    return angle_of_vector(pos1[0]-pos2[0], pos1[1]-pos2[1])

def getPosOnCircumeference(theta, origin):
    theta = toRadian(theta)
    x = origin[0] + radius * math.cos(-theta)
    y = origin[1] + radius * math.sin(-theta)
    return (x, y)

def getDistanceFromOrigin(startPoint, endPoint):
    distance = math.hypot(endPoint[1] - startPoint[1],(endPoint[0] - startPoint[0]))
    return distance
