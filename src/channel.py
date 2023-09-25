import os
from googleapiclient.discovery import build
import json

api_key = os.getenv('YOUTUBE_APIKEY')


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.title = str()
        self.description = str()
        self.video_count = int()
        self.followers_count = int()
        self.views_count = int()
        self.url = str()
        self.youtube = build('youtube', 'v3', developerKey=api_key)

    @property
    def channel_id(self):
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, __channel_id):
        print(self.__channel_id)

    @classmethod
    def get_service(cls):
        """Возвращающем объект для работы с YouTube API"""
        return build('youtube', 'v3', developerKey=api_key)

    def print_info(self):
        """Выводит в консоль информацию о канале."""
        response = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(response, indent=2, ensure_ascii=False))

    def to_json(self, filename):
        """Сохраняем в файл значения атрибутов экземпляра Channel"""
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(channel)

        channel_data = {
            'id': self.__channel_id,
            'name': self.title,
            'link': self.url,
            'description': self.description,
            'view_count': self.views_count,
            'subscriber_count': self.followers_count
        }
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(channel_data, file, ensure_ascii=False)