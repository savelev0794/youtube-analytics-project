import os
from googleapiclient.discovery import build
from datetime import timedelta
import isodate

api_key: str = os.getenv('YOUTUBE_APIKEY')


class PlayList:
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id) -> None:
        self.__playlist_id: str = playlist_id
        self.playlist = self.youtube.playlists().list(id=self.__playlist_id, part='snippet',).execute()
        self.title: str = self.playlist['items'][0]['snippet']['title']
        self.url: str = f'https://www.youtube.com/playlist?list={playlist_id}'

    @property
    def total_duration(self):
        """Возвращает объект класса datetime.timedelta с суммарной длительностью плейлиста"""
        videos = self.youtube.playlistItems().list(playlistId=self.__playlist_id, part='contentDetails').execute()
        total_duration_seconds = 0
        for video in videos['items']:
            video_id = video['contentDetails']['videoId']
            video_info = self.youtube.videos().list(part='contentDetails', id=video_id).execute()
            iso_8601_duration = video_info['items'][0]['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration_seconds += duration.total_seconds()

        total_duration = timedelta(seconds=total_duration_seconds)
        return total_duration

    def show_best_video(self):
        """Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""
        videos = self.youtube.playlistItems().list(playlistId=self.__playlist_id, part='contentDetails').execute()
        video_likes = {}
        for video in videos['items']:
            video_id = video['contentDetails']['videoId']
            video_info = self.youtube.videos().list(part='statistics', id=video_id).execute()
            likes = int(video_info['items'][0]['statistics']['likeCount'])
            video_likes[video_id] = likes

        max_key = max(video_likes, key=video_likes.get)
        return f'https://youtu.be/{max_key}'
