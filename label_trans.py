import os

def change_labels_to_zero(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # 각 라인을 리스트로 변환하여 첫 번째 값을 0으로 바꿈
    new_lines = []
    for line in lines:
        values = line.split()  # 공백을 기준으로 값들을 분리하여 리스트로 변환
        values[0] = '0'  # 첫 번째 값 변경
        new_line = ' '.join(values) + '\n'  # 변경된 값을 다시 문자열로 변환하여 new_line에 추가
        new_lines.append(new_line)

    with open(file_path, 'w') as file:
        file.writelines(new_lines)

# 변경할 라벨 파일들이 있는 디렉토리 경로를 지정하세요.
label_directory = 'C:\\Users\\dhkim\\Downloads\\Venom.v8i.yolov8\\valid\\labels'

for filename in os.listdir(label_directory):
    if filename.endswith('.txt'):
        file_path = os.path.join(label_directory, filename)
        change_labels_to_zero(file_path)
