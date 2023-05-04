import math
import pygame

radius = 250

def toRadian(theta):
    return theta * math.pi / 180

def toDegrees(theta):
    return theta * 180 / math.pi

def getAngle(pos1, pos2):
    return pygame.math.Vector2(pos1[0] - pos2[0], pos1[1] - pos2[1]).angle_to((1, 0))

def getLineEndPos(theta, origin):
    theta = toRadian(-theta)
    x = origin[0] + radius * math.cos(theta)
    y = origin[1] + radius * math.sin(theta)
    return [x, y]

def getDistanceFromOrigin(pos1, pos2):
    return math.hypot(pos1[0] - pos2[0], pos1[1] - pos2[1])

def distanceInMeters(pos1, pos2):
    return math.sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)
