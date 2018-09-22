from django.db import models


class SearchKeyword(models.Model):
    """
    Модель SearchKeyword предназначена для хранения ключевых слов, по которым приложение
    производит периодический поиск в YouTube
    """
    key_word = models.CharField(verbose_name='слово', max_length=255, unique=True)

    def __str__(self):
        return self.word


class YTVideo(models.Model):
    """
    Модель YTVideo хранит данные о найденных по ключевым словам видео на YouTube
    """
    # YouTube позволяет давать видео названия не длиннее 100 символов
    # https://developers.google.com/youtube/v3/docs/videos#snippet.title
    title = models.CharField(verbose_name='заголовок', max_length=100)
    url = models.URLField(verbose_name='URL')
    date = models.DateField(verbose_name='дата загрузки')
    key_words = models.ManyToManyField(
        SearchKeyword,
        verbose_name='ключевые слова',
        related_name='videos',
    )

    def __str__(self):
        return '{} ({})'.format(self.title, self.url)
