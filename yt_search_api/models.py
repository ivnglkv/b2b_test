from django.db import models


class SearchKeyword(models.Model):
    """
    Модель SearchKeyword предназначена для хранения ключевых слов, по которым приложение
    производит периодический поиск в YouTube
    """
    word = models.CharField(verbose_name='слово', max_length=255, unique=True, editable=False)

    def __str__(self):
        return self.word
