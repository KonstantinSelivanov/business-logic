from django.db import models


class CommonMailingList(models.Model):
    """ Mailing for general materials from the site """
    """ Рассылка на общие материалы с сайта """
    email = models.EmailField(verbose_name='Email подписчика')

    class Meta:
        db_table = 'common_mailing_list'


class CaseMailingList(models.Model):
    """ Newsletter for specific site material """
    """ Рассылка на конкретный материал сайта """
    email = models.EmailField(verbose_name='Email подписчика')
    case = models.ForeignKey(to='cases.Case', verbose_name='Материал',
                             on_delete=models.CASCADE)

    class Meta:
        db_table = 'case_mailing_list'
