import cv2
from function import Object

player = Object('images/T_REX.png')
scr = cv2.imread('screen.png', 0)

player.match(scr)

location = player.location
print(location)

scr = cv2.cvtColor(scr, cv2.COLOR_GRAY2BGR)
cv2.rectangle(scr, location[0], location[1], (255, 0, 0), 2)

cv2.imshow('screen', scr)
cv2.waitKey(0)