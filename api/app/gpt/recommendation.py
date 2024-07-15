from app.gpt.weather import get_weather_info
import random
import base64
import json
import logging
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Menu, StoresWithinRange, Image
from app.gpt.weather import get_weather_info
import openai
from app.config import get_settings
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

settings = get_settings()
openai.api_key = settings.openai_api_key

def fetch_all_menus():
    db = SessionLocal()
    try:
        menus = db.query(Menu).all()
        store_menus = {}
        for menu in menus:
            if menu.store_id not in store_menus:
                store_menus[menu.store_id] = []
            store_menus[menu.store_id].append(menu.menu)
        return store_menus
    finally:
        db.close()

def recommend_menu_based_on_weather(store_menus, weather_info):
    from openai import OpenAI
    system_prompt = (
        "당신은 메뉴를 추천하는 메뉴 추천 전문가입니다.\n"
        "다음은 식당의 메뉴 목록과 가격 정보입니다.\n"
        "랜덤하게 한가지 메뉴를 선택하고, 그 메뉴를 보유하고 있는 식당 ID와 추천한 이유를 날씨와 연관지어서 부탁해\n"
        "추천 형식은 (식당ID)-_-(선택한 이유)입니다."
    )

    weather_prompt = f"현재 날씨 정보: {weather_info}\n"
    print(weather_info)
    menu_prompt = f"메뉴 목록: {json.dumps(store_menus, ensure_ascii=False)}\n"
    print(menu_prompt)

    user_prompt = weather_prompt + menu_prompt + "날씨에 적절한 한가지 메뉴를 랜덤하게 고르고, 해당 메뉴를 보유한 식당 ID와 고른 이유를 유쾌한 농담과 함께 알려줘."
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=2048
    )

    return response.choices[0].message.content

def fetch_random_ai_summarize_with_image():
    db = SessionLocal()
    try:
        # 모든 store_id 가져오기
        store_ids = db.query(StoresWithinRange.id).all()
        random_id = random.choice(store_ids)[0]

        # 랜덤하게 선택된 store_id의 ai_summarize 가져오기
        store_info = db.query(StoresWithinRange).filter(StoresWithinRange.id == random_id).first()

        # 랜덤하게 선택된 store_id의 이미지 가져오기
        image_record = db.query(Image).filter(Image.store_id == random_id).first()
        image_data = base64.b64encode(image_record.image).decode('utf-8') if image_record else None

        ai_summarize = store_info.ai_summarize
        ai_summarize = re.sub(r'\n\n', ' ', ai_summarize)
        ai_summarize = re.sub(r'\n', ' ', ai_summarize)    
        print(ai_summarize)
        return {
            "business_name": store_info.business_name,
            "business_type": store_info.business_type,
            "ai_summarize": ai_summarize,
            "image_data": f"![image](data:image/png;base64,{image_data})" if image_data else None,
        }
    finally:
        db.close()

def main():
    # weather_info = get_weather_info()
    # store_menus = fetch_all_menus()
    # recommendations = recommend_menu_based_on_weather(store_menus, weather_info)
    # print("추천 결과:", recommendations)
    random_ai_summarize = fetch_random_ai_summarize_with_image()
    print("랜덤 AI 요약:", random_ai_summarize)

if __name__ == "__main__":
    main()
