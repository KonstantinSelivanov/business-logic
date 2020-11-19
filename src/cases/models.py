from django.db import models


class Case(models.Model):
    """ A set of materials on the site on a specific case """
    """ Набор материалов на сате по конкретному делу """
    name = models.CharField(verbose_name='Название дела', max_length=255)

    class Meta:
        db_table = 'case'
