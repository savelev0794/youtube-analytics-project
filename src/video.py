import os
from googleapiclient.discovery import build
#
api_key: str = os.getenv('YOUTUBE_APIKEY')


class Video:
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id) -> None:
        """Инициализация класса Video"""
        try:
            self.video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                             id=video_id).execute()
            self.video_id: str = video_id
            self.title: str = self.video_response['items'][0]['snippet']['title']
            self.url: str = f'https://www.youtube.com/watch?v={self.video_id}'
            self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
            self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']
        except IndexError:
            self.video_id = video_id
            self.title = None
            self.url = None
            self.like_count = None
            self.view_count = None

    def __str__(self):
        """Возвращает название видео"""
        return f"{self.title}"

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        return cls.youtube


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str) -> None:
        """Инициализация класса PLVideo - наследника класса Video с добавлением новго атрибута"""
        super().__init__(video_id)
        self.playlist_id = playlist_id
        self.video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                         id=self.video_id).execute()
        self.title = self.video_response['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/watch?v={self.video_id}'
        self.view_count = self.video_response['items'][0]['statistics']['viewCount']
        self.like_count = self.video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        """Возвращает название видео"""
        return f"{self.title}"

