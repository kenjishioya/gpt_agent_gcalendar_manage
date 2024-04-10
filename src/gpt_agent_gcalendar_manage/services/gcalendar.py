from datetime import datetime
import os
from typing import Optional
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from langchain.agents import tool
from langchain.pydantic_v1 import BaseModel, Field


# サービスアカウントキーファイルのパス
SERVICE_ACCOUNT_FILE = './cred/gcp_service_account.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"

class CalendarSearchInput(BaseModel):
    start_datetime: Optional[str] = Field(description='カレンダーを検索するときの条件の開始日時。YYYY-MM-DDTHH:MM:SS±HH:MMのフォーマットで引数に渡す。')
    end_datetime: Optional[str] = Field(description='カレンダーを検索するときの条件の終了日時。YYYY-MM-DDTHH:MM:SS±HH:MMのフォーマットで引数に渡す。')

class CalendarEvents(BaseModel):
    summary: str = Field(description='イベントの題名。')
    description: str = Field(description='詳細文。')
    start_time: str = Field(description="開始日時。YYYY-MM-DDTHH:MM:SS±HH:MMのフォーマットで引数に渡す。")
    end_time: str = Field(description='終了日時。YYYY-MM-DDTHH:MM:SS±HH:MMのフォーマットで引数に渡す。')

@tool
def get_now():
    """現在の日時をYYYY-MM-DDTHH:MM:SS±HH:MMのフォーマットで取得する。"""
    return datetime.now().strftime(DATETIME_FORMAT)

@tool('get_calendar_events', args_schema=CalendarSearchInput)
def get_calendar_events(start_datetime: Optional[str], end_datetime: Optional[str]):
    """グーグルカレンダーにアクセスして直近10件のイベントを取得する。"""
    service = _build_service()
    # イベントを取得したいカレンダーID
    calendar_id = os.getenv('CALENDAR_ID')
    param = dict(
        calendarId=calendar_id,
        maxResults=10,
        singleEvents=True,
        orderBy='startTime',
    )
    if start_datetime is not None:
        param['timeMin'] = start_datetime + 'Z'
    if end_datetime is not None:
        param['timeMax'] = end_datetime + 'Z'
    print(param)
    events_result = service.events().list(**param).execute()
    events = events_result.get('items', [])

    return events

@tool('regist_calendar_events', args_schema=CalendarEvents)
def regist_calendar_events(summary: str, description: str, start_time: str, end_time: str):
    """グーグルカレンダーにアクセスして入力された情報でイベントを登録する。成功したらオブジェクトを返す。もし引数が渡っていなかったらユーザーに聞いてほしい。"""
    service = _build_service()
    # イベントを取得したいカレンダーID
    calendar_id = os.getenv('CALENDAR_ID')
    event = {
    'summary': summary,
    'location': None,
    'description': description,
    'start': {
        'dateTime': start_time,
        'timeZone': 'Asia/Tokyo',
        },
    'end': {
        'dateTime': end_time,
        'timeZone': 'Asia/Tokyo',
        },
    }
    result = service.events().insert(calendarId=calendar_id, body=event).execute()
    return result

def _build_service():
    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('calendar', 'v3', credentials=credentials)
    return service