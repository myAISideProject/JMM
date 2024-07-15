import json

# JSON 파일 경로
file_path = '/Users/igeon/Desktop/Projects/JMM/sample.json'

# JSON 파일 읽기
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# ID 값 추출 및 개수 세기
id_list = [item['place_url'] for item in data]
id_count = len(id_list)

# 결과 출력
print(f"ID의 개수: {id_count}")
