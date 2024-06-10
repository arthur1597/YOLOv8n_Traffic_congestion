# YOLOv8n_Traffic_congestion_Check
---
## Yolov8을 이용해서 객체를 탐지하여 교통 혼잡도 체크하기
---
![객체탐지이미지](이미지1.PNG)
![객체탐지이미지2](이미지2.PNG)

CCTV와 같은 차도 영상을 이용하여 교통 혼잡도를 측정하는 시스템, 교통카메라의 실시간 교통영상을 활용하여
차량 객체를 탐지하여 임계치를 설정하고 Low,Middle,High 범주로 화면 상단에 표시한다. 


## 기술 스택
---
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/ultraytics-7952B3?style=for-the-badge&logo=ultraytics&logoColor=white"> <img src="https://img.shields.io/badge/roboflow-003545?style=for-the-badge&logo=roboflow&logoColor=white">

## installation
---
!pip install ultralytics

import numpy as np


import pandas as pd


import cv2

## 구현 내용
---
### Yolov8로 Vehicle 객체 Detection하고 인식 범위 지정한 후 이미지 좌표를 이용하여 범위 지정하여 지정된 범위내에 있는 탐지된 객체 수 세어 교통 혼잡도 알려준다





