import cv2
import pyautogui
import time
 
from function import Object, grabScreen

startTime = time.time()  

prevTime = time.time()
speedRate = 1.5 

player_index = 0 
enemy_index = 0 
distanceThreshold = 80

# 사용자 화면 크기에 맞게 다시 저장해야함 (개인마다 크기가  다르기 때문)
player = [
    Object('images/T_REX.png'),
    Object('images/T_REX_b.png')
    ]
 
enemies = [ 
        [
            Object('images/small_cactus.png'), 
            Object('images/cactus.png'), 
            Object('images/cactus_flip.png'),
            Object('images/bird_up.png'),
            Object('images/bird_down.png')
        ],
        [
            Object('images/small_cactus_b.png'), 
            Object('images/cactus_b.png'), 
            Object('images/cactus_flip_b.png'),
            Object('images/bird_up_b.png'),
            Object('images/bird_down_b.png')
        ] 
    ]

restart = Object('images/restart.png')

# 공룡의 초기 위치 탐지 및 감시 범위 설정
while True:
    img = grabScreen()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if player[0].match(img):
        # 이것도 사용자마다 크기가 달라서 개인적으로 설정해야함
        topleft_x = int(player[0].location[0][0] - player[0].width)
        topleft_y = int(player[0].location[0][1] - 3 *  player[0].height)
        bottomRight_x = int(player[0].location[1][0] + 14 * player[0].width)
        bottomRight_y = int(player[0].location[1][1] + 2 * player[0].height)
        screenStart = (topleft_x, topleft_y)
        screenEnd = (bottomRight_x, bottomRight_y)
        break

print("종료하려면 esc키를 누르세요.")
pyautogui.press('space')

# 장애물 감시 및 점프 판단
while True:
    img_0 = grabScreen(bbox=(*screenStart, *screenEnd))
    img = cv2.cvtColor(img_0, cv2.COLOR_BGR2GRAY)
 
    #  낮/밤 테마 판별
    if player[0].match(img):
        player_index = 0 
        enemy_index = 0

    elif player[1].match(img):
        player_index = 1
        enemy_index = 1

    # restart 되면 시간 초기화
    if restart.match(img):
        cv2.rectangle(img_0, restart.location[0], restart.location[1], (0, 255, 0), 2)
        startTime = time.time()
        prevTime = time.time() 
        distanceThreshold = 70
        pyautogui.press('space')
    
    # 거리 기준 조절 (속도 증가에 따라 점프 거리 앞당기기)
    # prevTime은 가장 최근에 이 로직이 실행된 시점을 저장
	# > 1이라는 조건은 "마지막 업데이트 이후 1초 이상이 지났는가?"를 판단하는 조건
    if time.time() - prevTime > 1:
        if time.time() - startTime < 180 and player[player_index].location:
            distanceThreshold += speedRate
        
        prevTime = time.time()
        
    # 공룡 위치 시각화
    if player[player_index].location: 
        cv2.rectangle(img_0, player[player_index].location[0], player[player_index].location[1], (255, 0, 0), 2)

    for enemy in enemies[enemy_index]:
        if enemy.match(img):
            cv2.rectangle(img_0, enemy.location[0], enemy.location[1], (0, 0, 255), 2)

            if player[player_index].location:
                horizontalDistance = enemy.location[0][0] - player[player_index].location[1][0]
                verticalDistance = player[player_index].location[0][1] - enemy.location[1][1]

                if horizontalDistance < distanceThreshold and verticalDistance < 2:
                    pyautogui.press('space')
                    break                     

    cv2.imshow('Screen', img_0)
       
    if cv2.waitKey(1) == 27:  # ESC key ASCII code는 27
        break 