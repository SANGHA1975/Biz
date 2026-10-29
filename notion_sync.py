import os
import requests
from datetime import datetime

NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
NOTION_DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")

def send_to_notion(title, content_markdown):
    url = "https://api.notion.com/v1/pages"
    
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    # 노션 페이지 본문 블록 형식으로 변환 (단순 문단 형태 예시)
    payload = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "제목": {
                "title": [{"text": {"content": title}}]
            },
            "날짜": {
                "date": {"start": datetime.now().strftime("%Y-%m-%d")}
            },
            "상태": {
                "select": {"name": "발행 대기"}
            }
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"text": {"content": content_markdown[:2000]}}] # 노션 블록 글자수 제한 대응
                }
            }
        ]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print("노션에 성공적으로 업로드되었습니다!")
    else:
        print(f"노션 업로드 실패: {response.text}")

if __name__ == "__main__":
    # 테스트용
    send_to_notion("[테스트] AI·IT 뉴스 브리핑", "오늘의 핵심 AI 동향 내용입니다.")
