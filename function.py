import numpy
import cv2
from PIL import ImageGrab

class Object:
    def __init__(self, path: str):
        # 이미지를 그레이스케일로 불러오기
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        self.img = img
        self.width = img.shape[1]  # 이미지 너비
        self.height = img.shape[0]  # 이미지 높이
        self.location = None  # 매칭된 위치 저장용

    def match(self, scr):
        # 템플릿 매칭 수행
        result = cv2.matchTemplate(scr, self.img, cv2.TM_CCOEFF_NORMED)
        # 최소값, 최대값 및 그 위치 가져오기
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        # 매칭된 영역의 좌상단과 우하단 좌표 계산
        top_left = max_loc
        bottom_right = (top_left[0] + self.width, top_left[1] + self.height)

        # 매칭 정도가 임계값 초과 시 위치 저장 후 True 반환
        if max_val > 0.6:
            self.location = (top_left, bottom_right)
            return True
        else:
            self.location = None  # 매칭 실패 시 None 설정
            return False

def grabScreen(bbox=None):
    img = ImageGrab.grab(bbox=bbox)  # 화면 영역 캡처
    img = numpy.array(img)  # PIL 이미지 -> NumPy 배열로 변환
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # 색상 포맷 변환 (RGB -> BGR)
    return img