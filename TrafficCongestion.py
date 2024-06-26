# -*- coding: utf-8 -*-
"""traffic.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1W6WIYEefq-Lw8viI4dSBoCbkZUEN_mjh
"""

!pip install ultralytics
# 드라이브 마운트
from google.colab import drive

drive.mount('/content/drive')

!git clone http://github.com/ultralytics/ultralytics.git

cd /content/drive/MyDrive/ultralytics/

!pip install ultralytics
#=======================================================================

import warnings
warnings.filterwarnings('ignore')

#필요한 라이브러리 삽입
import os
import shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
import yaml
import torch
from PIL import Image
from ultralytics import YOLO
from IPython.display import Video

import shutil
shutil.rmtree('/content/drive/MyDrive/ultralytics/runs/detect/val')

# Seaborn은 matplotlib의 시각화툴의 격자는 어두운 색을 연보라색으로 지정
sns.set(rc={'axes.facecolor': '#eae8fa'}, style='darkgrid')
#===========================================================================

# ultalytics의 pre-trained 모델 호출
model = YOLO('yolov8n.pt')

#이미지 파일의 경로
image_path = '/content/drive/MyDrive/Top-View Vehicle Detection Image Dataset/Vehicle_Detection_Image_Dataset/sample_image.jpg'

#이미지 추론을 진행
results = model.predict(source=image_path,
                        imgsz=640,#이미지를 640x640으로 지정
                        verbose=False,#자세한 출력보단 요약정보만 출력
                        conf=0.5)   #객체감지 결과를 필터링할때 사용하는데 50%가 넘은 것만 결과에 포함하게 함

# 이미지에 result의 첫번째 결과를 넣고 이미지를 넘파일 배열로 변환하여 line_width를 통해 선의 넓이 결정
sample_image = results[0].plot(line_width=2)

# BGR을 plot시 정확한 결과 보기 위해 RGB로 변환
sample_image = cv2.cvtColor(sample_image, cv2.COLOR_BGR2RGB)

#image를 display
plt.figure(figsize=(20,15))
plt.imshow(sample_image)
plt.title('Detected Objects in Sample Image by the Pre-trained YOLOv8 Model on COCO Dataset', fontsize=20)
plt.axis('off')
plt.show()
#=============================================================================================


#데이터셋의 경로 지정
dataset_path = '/content/drive/MyDrive/Top-View Vehicle Detection Image Dataset/Vehicle_Detection_Image_Dataset'

# data.yaml파일의 경로 지정 -> data.yaml은 데이터셋의 구성정보를 담고 있음
yaml_file_path = os.path.join(dataset_path, 'data.yaml')

# yaml파일을 로드하고 데이터 파일의 내용을 읽고 출력
with open(yaml_file_path, 'r') as file:
    yaml_content =yaml.load(file, Loader = yaml.FullLoader)
    print(yaml.dump(yaml_content, default_flow_style=False))
#==============================================================================================

# training과 validation 이미지들의 경로를 정해줌
trian_image_path = os.path.join(dataset_path, 'train', 'images')
validation_image_path = os.path.join(dataset_path, 'valid', 'images')

# train, vailid의 초기값 설정
num_trian_images = 0
num_valid_images = 0

# 이미지의 고유한 크기를 유지하도록 세트 초기화
train_image_size = set()
valid_image_size = set()

# train 이미지 크기 및 카운트 확인
for filename in os.listdir(trian_image_path):
    if filename.endswith('.jpg'):
        num_trian_images += 1
        image_path = os.path.join(trian_image_path, filename)
        with Image.open(image_path) as img:
            train_image_size.add(img.size)

# validation 이미지 크기 및 개수 확인
for filename in os.listdir(validation_image_path):
    if filename.endswith('.jpg'):
        num_valid_images +=1
        image_path = os.path.join(validation_image_path, filename)
        with Image.open(image_path) as img:
            valid_image_size.add(img.size)


# 결과 출력
print(f"Number of training images:, {num_trian_images}")
print(f"Number of validation images: {num_valid_images}")


# train 사이즈 모두 같은지 확인
if len(train_image_size) == 1:
    print(f"All training images have the same size: {train_image_size.pop()}")
else:
    print("Training images have verying sizes.")

# validation 사이즈 모두 같은지 확인
if len(valid_image_size) == 1:
    print(f"All validation images have the same size: {valid_image_size.pop()}")

else:
    print("Validation images have verying sizes")
#===============================================================================================

#image path
image_files = [file for file in os.listdir(trian_image_path) if file.endswith('.jpg')]

# 8개의 영상을 동일한 간격으로 선택합니다
num_images = len(image_files)
selected_images = [image_files[i] for i in range(0, num_images, num_images // 8)]

fig,axes = plt.subplots(2,4,figsize=(20,11))

#이미지 display
for ax, img_file in zip(axes.ravel(), selected_images):
    img_path =os.path.join(trian_image_path, img_file)
    image = Image.open(img_path)
    ax.imshow(image)
    ax.axis('off')

plt.suptitle('Sample Images from Training Dataset',fontsize=20)
plt.tight_layout()
plt.show()
#==================================================================================================

# dataset에 대한 Fine tunning
results = model.train(
    data = yaml_file_path,
    epochs = 100,
    imgsz=640,
    patience=50,
    batch = 32,
    optimizer = 'auto',
    lr0 = 0.0001,
    lrf = 0.1,
    dropout=0.1,
    )
#====================================================================================================

# train 파일 경로 지정
post_training_files_path ='/content/drive/MyDrive/ultralytics/runs/detect/train'

best_model_path = os.path.join(post_training_files_path, 'weights/best.pt')

best_model = YOLO(best_model_path)

metrics = best_model.val(split='val')
#=====================================================================================================

#손실값에 대한 학습 곡선
def plot_learning_curve(df, train_loss_col, val_loss_col, title):
    plt.figure(figsize=(12, 5))
    sns.lineplot(data=df, x='epoch', y=train_loss_col, label='Train Loss', color='#141140', linestyle='-', linewidth=2)
    sns.lineplot(data=df, x='epoch', y=val_loss_col, label='Validation Loss', color='orangered', linestyle='--', linewidth=2)
    plt.title(title)
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

#디렉토리와 파일 이름 사용하여 result.csv의 전체 파일 경로 생성
results_csv_path = os.path.join(post_training_files_path, 'results.csv')

# 구성한 csv파일을 panda Dataframe에 로드
df = pd.read_csv(results_csv_path)

# 공백제거
df.columns = df.columns.str.strip()

#손실에 대한 학습곡선 표시
plot_learning_curve(df, 'train/box_loss', 'val/box_loss', 'Box Loss Learning Curve')
plot_learning_curve(df, 'train/cls_loss', 'val/cls_loss', 'Classification Loss Learning Curve')
plot_learning_curve(df, 'train/dfl_loss', 'val/dfl_loss', 'Distribution Focal Loss Learning Curve')
#=======================================================================================================

# 유효성검사
valid_image_path = os.path.join(dataset_path, 'valid','images')

#디렉토리내 모든 JPG 나열
image_files = [file for file in os.listdir(valid_image_path) if file.endswith('.jpg')]

#동일한 간격으로 9장 영상 선택
num_images = len(image_files)
selected_images = [image_files[i] for i in range(0, num_images, num_images // 9)]

# Initailize the subplot
fig, axes = plt.subplots(3,3,figsize=(20,21))
plt.title('Validattion set inferences', fontsize=24)


#선택한 이미지에대한 enumerate 실행하고 표시
for i, ax, in enumerate(axes.flatten()):
    image_path = os.path.join(valid_image_path, selected_images[i])
    results = best_model.predict(source = image_path, imgsz = 640, conf=0.5)
    annotated_image = results[0].plot(line_width=1)
    annotated_image_rgb =cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
    ax.imshow(annotated_image_rgb)
    ax.axis('off')

plt.tight_layout()
plt.show()
#========================================================================================================

sample_image_path = '/content/drive/MyDrive/Top-View Vehicle Detection Image Dataset/Vehicle_Detection_Image_Dataset/sample_image.jpg'

#best.pt 모델을 사용하여 제공된 이미지에 대한 추론 수행
results = best_model.predict(source=sample_image_path, imgsz=640,conf=0.7)

# 이미지를 numpy 배열로 변환합니다
smaple_image = results[0].plot(line_width=2)

#BGR에서 RGB로 변환합니다
sample_image = cv2.cvtColor(sample_image, cv2.COLOR_BGR2RGB)

# Display annotated image
plt.figure(figsize=(20,15))
plt.imshow(sample_image)
plt.title('Detected Objects in Sample Image by the  Final-tune YOLOv8 Model', fontsize=20)
plt.axis('off')
plt.show()
#========================================================================================================

# 데이터셋에서 비디오 경로 정의
dataset_video_path = '/content/drive/MyDrive/Top-View Vehicle Detection Image Dataset/Vehicle_Detection_Image_Dataset/sample_video.mp4'

# 비디오 경로 지정
video_path = '/content/drive/MyDrive/ultralytics/working/sample_video4.mp4'

# 비디오 경로 복사 및 처리
shutil.copyfile(dataset_video_path, video_path)

# 비디오 샘플 이용하여 최고의 성능 발휘하는 모델 이용하여 결과저장
best_model.predict(source=video_path, save=True)
#========================================================================================================

import locale
locale.getpreferredencoding = lambda: "UTF-8"
#YOLOv8 예측으로 생성된 .avi 비디오를 .mp4 형식으로 변환하여 display
!ffmpeg -y -nostdin -loglevel panic -i /content/drive/MyDrive/ultralytics/runs/detect/predict2/sample_video3.avi processed_sample_video2.mp4


# Embed and display the processed sample video within the notebook
Video("processed_sample_video2.mp4", embed=True, width=960)
#=========================================================================================================

# 데이터셋에서 비디오 경로 정의
dataset_video_path = '/content/drive/MyDrive/Top-View Vehicle Detection Image Dataset/Vehicle_Detection_Image_Dataset/presentation_sample.mp4'

# 비디오 경로 지정
video_path = '/content/drive/MyDrive/ultralytics/working/check_Yolo.mp4'

# 비디오 경로 복사 및 처리
shutil.copyfile(dataset_video_path, video_path)

# 비디오 샘플 이용하여 최고의 성능 발휘하는 모델 이용하여 결과저장
best_model.predict(source=video_path, save=True)

import locale
locale.getpreferredencoding = lambda: "UTF-8"

# 동영상 변환을 위한 ffmpeg 명령어 실행
!ffmpeg -y -nostdin -loglevel panic -i /content/drive/MyDrive/ultralytics/runs/detect/predict2/check_Yolo.avi check_Yolo.mp4

# 코랩에서 동영상 재생을 위한 라이브러리 불러오기
from IPython.display import Video

# 변환된 동영상 재생
Video("check_Yolo.mp4", embed=True, width=960)
#=========================================================================================================
# 교통을 '중'으로 간주하는 임계값 정의
heavy_traffic_threshold = 8

vertices = np.array([
    (465, 350),  # vertices의 좌측 상단
    (2, 630),    # vertices의 우측 상단
    (1203, 630),   # vertices의 우측 하단
    (815, 350),    # vertices의 좌측 하단
], dtype=np.int32)

x1,x2 = 325,635
lane_threshold = 609
background_color = (255, 255, 255)

# 이미지에 텍스트 주석을 넣을 위치 정의
text_position_left_lane = (10, 50)
text_position_right_lane = (820, 50)
intensity_position_left_lane = (10, 100)
intensity_position_right_lane = (820, 100)


# 폰트, 스케일 및 주석 색상 정의
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_color = (0, 0, 0)    # 흰색 텍스트

#viedo 가져옴
cap = cv2.VideoCapture('/content/drive/MyDrive/Top-View Vehicle Detection Image Dataset/Vehicle_Detection_Image_Dataset/sample_video.mp4')
# 비디오 작성 객체 설정
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('/content/drive/MyDrive/Top-View Vehicle Detection Image Dataset/Vehicle_Detection_Image_Dataset/traffic_density_analysis.mp4', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))
while cap.isOpened():
    # 프레임 가져오기
    ret, frame = cap.read()
    if ret:
        # 원본 프레임 복사하여 수정
        detection_frame = frame.copy()

        # 지정된 수직 범위를 벗어난 영역을 차단
        detection_frame[:x1, :] = 0
        detection_frame[x2:, :] = 0

        # 프레임에서 추론 수행 (여기서는 가상의 모델 사용)
        results = best_model.predict(detection_frame, imgsz=640, conf=0.4)
        processed_frame = results[0].plot(line_width=1)

        # 프레임의 상단 및 하단 부분을 복원
        processed_frame[:x1, :] = frame[:x1, :].copy()
        processed_frame[x2:, :] = frame[x2:, :].copy()

        # 사각형 그리기
        cv2.polylines(processed_frame, [vertices], isClosed=True, color=(0, 255, 0), thickness=2)

        # 결과에서 바운딩 박스 가져오기
        bounding_boxes = results[0].boxes

        # 정해진 영역 내의 차량 수 초기화
        vehicles_in_left_lane = 0
        vehicles_in_right_lane = 0

        # 각 바운딩 박스를 확인하여 정해진 영역 내의 차량 수 계산
        for box in bounding_boxes.xyxy:
            if box[0] < lane_threshold:
                vehicles_in_left_lane += 1
            else:
                vehicles_in_right_lane += 1


        # 교통 혼잡도 결정
        if vehicles_in_left_lane > heavy_traffic_threshold:
            traffic_left_intensity = "high"
        elif vehicles_in_left_lane == heavy_traffic_threshold:
            traffic_left_intensity = "middle"
        else:
            traffic_left_intensity = "low"

        if vehicles_in_right_lane > heavy_traffic_threshold:
            traffic_right_intensity = "high"
        elif vehicles_in_right_lane == heavy_traffic_threshold:
            traffic_right_intensity = "middle"
        else:
            traffic_right_intensity = "low"


        # 배경박스 추가 (차량 수 텍스트)
        cv2.rectangle(processed_frame, (text_position_left_lane[0] - 10, text_position_left_lane[1] - 25),
              (text_position_left_lane[0] + 460, text_position_left_lane[1] + 10), background_color, -1)
        # 사각형 위에 차량 수 텍스트 추가
        cv2.putText(processed_frame, f'Left_lane_Vehicle Count: {vehicles_in_left_lane}', text_position_left_lane,
            font, font_scale, font_color, 2, cv2.LINE_AA)

        # 배경박스 추가 (교통 혼잡도 텍스트)
        cv2.rectangle(processed_frame, (intensity_position_left_lane[0] - 10, intensity_position_left_lane[1] - 25),
              (intensity_position_left_lane[0] + 460, intensity_position_left_lane[1] + 10), background_color, -1)
        # 사각형 위에 교통 혼잡도 텍스트 추가
        cv2.putText(processed_frame, f'Traffic Congestion: {traffic_left_intensity}', intensity_position_left_lane,
            font, font_scale, font_color, 2, cv2.LINE_AA)

        # 배경박스 추가 (차량 수 텍스트)
        cv2.rectangle(processed_frame, (text_position_right_lane[0] - 10, text_position_right_lane[1] - 25),
              (text_position_right_lane[0] + 460, text_position_right_lane[1] + 10), background_color, -1)
        # 사각형 위에 차량 수 텍스트 추가
        cv2.putText(processed_frame, f'Right_lane_Vehicle Count: {vehicles_in_right_lane}', text_position_right_lane,
            font, font_scale, font_color, 2, cv2.LINE_AA)

        # 배경박스 추가 (교통 혼잡도 텍스트)
        cv2.rectangle(processed_frame, (intensity_position_right_lane[0] - 10, intensity_position_right_lane[1] - 25),
              (intensity_position_right_lane[0] + 460, intensity_position_right_lane[1] + 10), background_color, -1)
        # 사각형 위에 교통 혼잡도 텍스트 추가
        cv2.putText(processed_frame, f'Traffic Congestion: {traffic_right_intensity}', intensity_position_right_lane,
            font, font_scale, font_color, 2, cv2.LINE_AA)

        # 처리된 프레임을 출력 비디오에 작성
        out.write(processed_frame)
    else:
        break

# 비디오 캡처 및 비디오 작성 객체 해제
cap.release()
out.release()
#==================================================================================================================
# 교통을 '중'으로 간주하는 임계값 정의
heavy_traffic_threshold = 8

vertices = np.array([
    (600, 400),  # vertices의 좌측 상단
    (4, 800),    # vertices의 우측 상단
    (1400, 800),   # vertices의 우측 하단
    (900, 400),    # vertices의 좌측 하단
], dtype=np.int32)

x1,x2 = 325,635
lane_threshold = 400
background_color = (255, 255, 255)

# 이미지에 텍스트 주석을 넣을 위치 정의
text_position_left_lane = (10, 50)
text_position_right_lane = (820, 50)
intensity_position_left_lane = (10, 100)
intensity_position_right_lane = (820, 100)


# 폰트, 스케일 및 주석 색상 정의
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_color = (0, 0, 0)    # 흰색 텍스트

#viedo 가져옴
cap = cv2.VideoCapture('/content/drive/MyDrive/Top-View Vehicle Detection Image Dataset/Vehicle_Detection_Image_Dataset/Heavy3.mp4')
# 비디오 작성 객체 설정
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('/content/drive/MyDrive/Top-View Vehicle Detection Image Dataset/Vehicle_Detection_Image_Dataset/Heavy3_out.mp4', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))
while cap.isOpened():
    # 프레임 가져오기
    ret, frame = cap.read()
    if ret:
        # 원본 프레임 복사하여 수정
        detection_frame = frame.copy()

        # 지정된 수직 범위를 벗어난 영역을 차단
        detection_frame[:x1, :] = 0
        detection_frame[x2:, :] = 0

        # 프레임에서 추론 수행 (여기서는 가상의 모델 사용)
        results = best_model.predict(detection_frame, imgsz=640, conf=0.4)
        processed_frame = results[0].plot(line_width=1)

        # 프레임의 상단 및 하단 부분을 복원
        processed_frame[:x1, :] = frame[:x1, :].copy()
        processed_frame[x2:, :] = frame[x2:, :].copy()

        # 사각형 그리기
        cv2.polylines(processed_frame, [vertices], isClosed=True, color=(0, 255, 0), thickness=2)

        # 결과에서 바운딩 박스 가져오기
        bounding_boxes = results[0].boxes

        # 정해진 영역 내의 차량 수 초기화
        vehicles_in_left_lane = 0
        vehicles_in_right_lane = 0

        # 각 바운딩 박스를 확인하여 정해진 영역 내의 차량 수 계산
        for box in bounding_boxes.xyxy:
            if box[0] < lane_threshold:
                vehicles_in_left_lane += 1
            else:
                vehicles_in_right_lane += 1


        # 교통 혼잡도 결정
        if vehicles_in_left_lane > heavy_traffic_threshold:
            traffic_left_intensity = "high"
        elif vehicles_in_left_lane == heavy_traffic_threshold:
            traffic_left_intensity = "middle"
        else:
            traffic_left_intensity = "low"

        if vehicles_in_right_lane > heavy_traffic_threshold:
            traffic_right_intensity = "high"
        elif vehicles_in_right_lane == heavy_traffic_threshold:
            traffic_right_intensity = "middle"
        else:
            traffic_right_intensity = "low"


        # 배경박스 추가 (차량 수 텍스트)
        cv2.rectangle(processed_frame, (text_position_left_lane[0] - 10, text_position_left_lane[1] - 25),
              (text_position_left_lane[0] + 460, text_position_left_lane[1] + 10), background_color, -1)
        # 사각형 위에 차량 수 텍스트 추가
        cv2.putText(processed_frame, f'Left_lane_Vehicle Count: {vehicles_in_left_lane}', text_position_left_lane,
            font, font_scale, font_color, 2, cv2.LINE_AA)

        # 배경박스 추가 (교통 혼잡도 텍스트)
        cv2.rectangle(processed_frame, (intensity_position_left_lane[0] - 10, intensity_position_left_lane[1] - 25),
              (intensity_position_left_lane[0] + 460, intensity_position_left_lane[1] + 10), background_color, -1)
        # 사각형 위에 교통 혼잡도 텍스트 추가
        cv2.putText(processed_frame, f'Traffic Congestion: {traffic_left_intensity}', intensity_position_left_lane,
            font, font_scale, font_color, 2, cv2.LINE_AA)

        # 배경박스 추가 (차량 수 텍스트)
        cv2.rectangle(processed_frame, (text_position_right_lane[0] - 10, text_position_right_lane[1] - 25),
              (text_position_right_lane[0] + 460, text_position_right_lane[1] + 10), background_color, -1)
        # 사각형 위에 차량 수 텍스트 추가
        cv2.putText(processed_frame, f'Right_lane_Vehicle Count: {vehicles_in_right_lane}', text_position_right_lane,
            font, font_scale, font_color, 2, cv2.LINE_AA)

        # 배경박스 추가 (교통 혼잡도 텍스트)
        cv2.rectangle(processed_frame, (intensity_position_right_lane[0] - 10, intensity_position_right_lane[1] - 25),
              (intensity_position_right_lane[0] + 460, intensity_position_right_lane[1] + 10), background_color, -1)
        # 사각형 위에 교통 혼잡도 텍스트 추가
        cv2.putText(processed_frame, f'Traffic Congestion: {traffic_right_intensity}', intensity_position_right_lane,
            font, font_scale, font_color, 2, cv2.LINE_AA)

        # 처리된 프레임을 출력 비디오에 작성
        out.write(processed_frame)
    else:
        break

# 비디오 캡처 및 비디오 작성 객체 해제
cap.release()
out.release()
#================================================================================================================================

# 교통을 '중'으로 간주하는 임계값 정의
heavy_traffic_threshold = 8

vertices = np.array([
    (600, 400),
    (4, 800),
    (1600, 800),
    (1100, 400),
], dtype=np.int32)

x1,x2 = 380,800
lane_threshold = 900
background_color = (255, 255, 255)

# 이미지에 텍스트 주석을 넣을 위치 정의
text_position_left_lane = (10, 50)
text_position_right_lane = (820, 50)
intensity_position_left_lane = (10, 100)
intensity_position_right_lane = (820, 100)


# 폰트, 스케일 및 주석 색상 정의
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_color = (0, 0, 0)    # 흰색 텍스트

#viedo 가져옴
cap = cv2.VideoCapture('/content/drive/MyDrive/Top-View Vehicle Detection Image Dataset/Vehicle_Detection_Image_Dataset/rain.mp4')
# 비디오 작성 객체 설정
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('/content/drive/MyDrive/Top-View Vehicle Detection Image Dataset/Vehicle_Detection_Image_Dataset/rain_out.mp4', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))
while cap.isOpened():
    # 프레임 가져오기
    ret, frame = cap.read()
    if ret:
        # 원본 프레임 복사하여 수정
        detection_frame = frame.copy()

        # 지정된 수직 범위를 벗어난 영역을 차단
        detection_frame[:x1, :] = 0
        detection_frame[x2:, :] = 0

        # 프레임에서 추론 수행 (여기서는 가상의 모델 사용)
        results = best_model.predict(detection_frame, imgsz=640, conf=0.4)
        processed_frame = results[0].plot(line_width=1)

        # 프레임의 상단 및 하단 부분을 복원
        processed_frame[:x1, :] = frame[:x1, :].copy()
        processed_frame[x2:, :] = frame[x2:, :].copy()

        # 사각형 그리기
        cv2.polylines(processed_frame, [vertices], isClosed=True, color=(0, 255, 0), thickness=2)

        # 결과에서 바운딩 박스 가져오기
        bounding_boxes = results[0].boxes

        # 정해진 영역 내의 차량 수 초기화
        vehicles_in_left_lane = 0
        vehicles_in_right_lane = 0

        # 각 바운딩 박스를 확인하여 정해진 영역 내의 차량 수 계산
        for box in bounding_boxes.xyxy:
            if box[0] < lane_threshold:
                vehicles_in_left_lane += 1
            else:
                vehicles_in_right_lane += 1


        # 교통 혼잡도 결정
        if vehicles_in_left_lane > heavy_traffic_threshold:
            traffic_left_intensity = "high"
        elif vehicles_in_left_lane == heavy_traffic_threshold:
            traffic_left_intensity = "middle"
        else:
            traffic_left_intensity = "low"

        if vehicles_in_right_lane > heavy_traffic_threshold:
            traffic_right_intensity = "high"
        elif vehicles_in_right_lane == heavy_traffic_threshold:
            traffic_right_intensity = "middle"
        else:
            traffic_right_intensity = "low"


        # 배경박스 추가 (차량 수 텍스트)
        cv2.rectangle(processed_frame, (text_position_left_lane[0] - 10, text_position_left_lane[1] - 25),
              (text_position_left_lane[0] + 460, text_position_left_lane[1] + 10), background_color, -1)
        # 사각형 위에 차량 수 텍스트 추가
        cv2.putText(processed_frame, f'Left_lane_Vehicle Count: {vehicles_in_left_lane}', text_position_left_lane,
            font, font_scale, font_color, 2, cv2.LINE_AA)

        # 배경박스 추가 (교통 혼잡도 텍스트)
        cv2.rectangle(processed_frame, (intensity_position_left_lane[0] - 10, intensity_position_left_lane[1] - 25),
              (intensity_position_left_lane[0] + 460, intensity_position_left_lane[1] + 10), background_color, -1)
        # 사각형 위에 교통 혼잡도 텍스트 추가
        cv2.putText(processed_frame, f'Traffic Congestion: {traffic_left_intensity}', intensity_position_left_lane,
            font, font_scale, font_color, 2, cv2.LINE_AA)

        # 배경박스 추가 (차량 수 텍스트)
        cv2.rectangle(processed_frame, (text_position_right_lane[0] - 10, text_position_right_lane[1] - 25),
              (text_position_right_lane[0] + 460, text_position_right_lane[1] + 10), background_color, -1)
        # 사각형 위에 차량 수 텍스트 추가
        cv2.putText(processed_frame, f'Right_lane_Vehicle Count: {vehicles_in_right_lane}', text_position_right_lane,
            font, font_scale, font_color, 2, cv2.LINE_AA)

        # 배경박스 추가 (교통 혼잡도 텍스트)
        cv2.rectangle(processed_frame, (intensity_position_right_lane[0] - 10, intensity_position_right_lane[1] - 25),
              (intensity_position_right_lane[0] + 460, intensity_position_right_lane[1] + 10), background_color, -1)
        # 사각형 위에 교통 혼잡도 텍스트 추가
        cv2.putText(processed_frame, f'Traffic Congestion: {traffic_right_intensity}', intensity_position_right_lane,
            font, font_scale, font_color, 2, cv2.LINE_AA)

        # 처리된 프레임을 출력 비디오에 작성
        out.write(processed_frame)
    else:
        break

# 비디오 캡처 및 비디오 작성 객체 해제
cap.release()
out.release()
