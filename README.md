# YOLOv8n_Traffic_congestion_Check
## Yolov8을 이용해서 객체를 탐지하여 교통 혼잡도 체크하기
---
![객체탐지이미지](이미지1.PNG)
![객체탐지이미지2](이미지2.PNG)

CCTV와 같은 차도 영상을 이용하여 교통 혼잡도를 측정하는 시스템, 교통카메라의 실시간 교통영상을 활용하여
차량 객체를 탐지하여 임계치를 설정하고 Low,Middle,High 범주로 화면 상단에 표시한다. 
이를 통해 내가 원하는 지역의 교통 혼잡도를 파악하여 혼잡도가 높은 지역을 피해 경로를 짜서 교통체증의 스트레스를 줄일 수 있다

**현 프로젝트의 문제점**
1.영상을 일일히 넣어 혼잡도를 파악하고자하는 곳의 좌표값을 찾아야함
2.작은 객체들은 탐지하기 힘듦
3.임계치값을 이미 정의하여 유동적 확인 불가
**추후개선사항**
1.앱이나 웹에 연결하여 실시간 영상을 통해 쉽게 교통혼잡도 파악 가능
2.영상 속 차선의 갯수를 통해 임계값 유동적 변경
3.작은 객체도 탐지 원할하게 개선

## <svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><title>9GAG</title><path d="m17.279 21.008 5.193-2.995V5.992l-5.193-2.996C14.423 1.348 12.048 0 12 0c-.048 0-2.423 1.348-5.279 2.996L1.528 5.992v2.354l5.193 2.996c2.856 1.648 5.232 2.996 5.28 2.996.048 0 1.469-.797 3.157-1.772a229.633 229.633 0 0 1 3.097-1.772c.016 0 .027 1.096.027 2.437l-.002 2.436-3.076 1.772c-1.692.975-3.115 1.783-3.163 1.795-.048.013-1.471-.776-3.162-1.752-1.69-.976-3.113-1.775-3.161-1.775-.155 0-4.036 2.274-4.011 2.35.031.093 10.136 5.937 10.276 5.943.057.002 2.44-1.344 5.296-2.992ZM9.847 8.391c-1.118-.65-2.033-1.2-2.033-1.222 0-.071 4.06-2.376 4.186-2.376.125 0 4.186 2.305 4.186 2.376 0 .063-4.047 2.375-4.184 2.39-.068.007-1.037-.519-2.155-1.168Z"/></svg>사용 라이브러리 및 기술
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/ultraytics-7952B3?style=for-the-badge&logo=ultraytics&logoColor=white"> <img src="https://img.shields.io/badge/roboflow-003545?style=for-the-badge&logo=roboflow&logoColor=white">
---
<img src="https://img.shields.io/badge/numpy-3776AB?style=for-the-badge&logo=python&logoColor=white">


**사용한 데이터셋**
rovoflow 내 데이터 셋 : 2개
<Vehicle_Detection_YOLOv8 Image Dataset>
https://universe.roboflow.com/farzad/vehicle_detection_yolov8/dataset/3

<Traffic Congestion Detection Computer Vision project>
https://universe.roboflow.com/sxc/traffic-congestion-detection/dataset/9/images

##모델 선정이유##---


## 사용 라이브러리
---
shutil


numpy


pandas


matplotlib


seaborn


cv2


pytorch


ultralytics import YOLO


## 구현 내용
---
### Yolov8로 Vehicle 객체 Detection하고 인식 범위 지정한 후 이미지 좌표를 이용하여 범위 지정하여 지정된 범위내에 있는 탐지된 객체 수 세어 교통 혼잡도 알려준다





