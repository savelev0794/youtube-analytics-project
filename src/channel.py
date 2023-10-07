import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YOUTUBE_APIKEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.url = f"https://www.youtube.com/{channel['items'][0]['snippet']['customUrl']}"
        self.subscriber_count = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.view_count = channel['items'][0]['statistics']['viewCount']

    def __str__(self):
        """Возвращает название и ссылку на канал"""
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        """Складывает количество подписчиков двух каналов"""
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        """Вычитает количество подписчиков второго канал из первого"""
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other):
        """На первом канале больше подписчиков?"""
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        """На первом канале больше подписчиков или столько же?"""
        return self.subscriber_count >= other.subscriber_count

    def __lt__(self, other):
        """На первом канале меньше подписчиков?"""
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        """На первом канале меньше подписчиков или столько же?"""
        return self.subscriber_count <= other.subscriber_count

    def __eq__(self, other):
        """На первом канале столько же подписчиков?"""
        return self.subscriber_count == other.subscriber_count

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        return cls.youtube

    def to_json(self, filename):
        """Сохраняет в файл значения атрибутов экземпляра `Channel`"""
        channel = {
            'channel_id': self.__channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriberCount': self.subscriber_count,
            'videoCount': self.video_count,
            'viewCount': self.view_count
        }

        with open(filename, 'w', encoding='UTF-8') as f:
            json.dump(channel, f, ensure_ascii=False)
