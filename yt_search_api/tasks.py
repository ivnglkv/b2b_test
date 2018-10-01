from datetime import datetime

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max
from django.utils import timezone

from apiclient.discovery import build
from celery import shared_task

from .models import SearchKeyword, YTVideo


@shared_task
def gather_new_videos():
    """
    Задача производит поиск и сохранение в БД новых видео по ключевым словам,
    сохраненным в системе.
    Для новых слов сохраняются последние 50 загруженных на Youtube видео
    Для слов, по которым ранее были найдены видео, загружаются данные всех роликов,
    выложенных от настоящего момента до даты публикации последнего из сохраненных
    """
    youtube = build('youtube', 'v3', developerKey=settings.GOOGLE_API_KEY)

    # Описание параметров:
    # https://developers.google.com/youtube/v3/docs/search/list#parameters
    base_search_args = {
        'part': 'snippet',
        'q': None,
        'order': 'date',
        'type': 'video',
        'maxResults': 50,
    }

    for keyword in SearchKeyword.objects.all():
        search_args = base_search_args.copy()
        search_args['q'] = keyword.key_word

        keyword_has_videos = len(keyword.videos.all()) > 0

        # Если по данному ключевому слову уже были найдены видео, то можно начать поиск новых
        # только среди загруженных после последнего из сохраненных видео
        if keyword_has_videos:
            last_published_at = YTVideo.objects.filter(
                key_words=keyword).aggregate(
                Max('published_at')
            )['published_at__max']

            # Формат даты для параметра publishedAfter:
            # RFC3339, 1970-01-01T00:00:00Z, без таймзоны
            # При USE_TZ = True в настройках, DateTimeField хранит данные таймзоны,
            # поэтому их необходимо удалить
            last_published_at = timezone.make_naive(last_published_at, timezone=timezone.utc)
            search_args['publishedAfter'] = '{}Z'.format(last_published_at.isoformat())

        while True:
            response = youtube.search().list(**search_args).execute()
            next_page_token = response.get('nextPageToken', None)

            _update_videos(keyword, response['items'])

            if keyword_has_videos and next_page_token:
                search_args['pageToken'] = response['nextPageToken']
            else:
                break


def _update_videos(keyword, json_videos):
    """
    Привязывает найденные видео к ключевым словам, создавая или обновляя объекты
    YTVideo в БД

    :param keyword: объект SearchKeyword, с которым будут ассоциироваться видео
    :param json_videos: перечень видео в формате JSON
    """
    for json_video in json_videos:
        snippet = json_video['snippet']

        title = snippet['title']
        url = 'https://www.youtube.com/watch?v={}'.format(json_video['id']['videoId'])

        # Для сохранения в БД необходимо добавить сведения о таймзоне
        published_at_naive = datetime.strptime(
            snippet['publishedAt'],
            '%Y-%m-%dT%H:%M:%S.%fZ'
        )
        published_at_aware = timezone.make_aware(published_at_naive, timezone.utc)

        # Не используется метод get_or_create так как название ролика
        # могло измениться после загрузки
        try:
            video = YTVideo.objects.get(url=url)
        except ObjectDoesNotExist:
            video = YTVideo(title=title, url=url, published_at=published_at_aware)
            video.save()

        video.key_words.add(keyword)
