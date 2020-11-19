from typing import Union

from cases.models import Case
from mailings.mailchimp_services import add_mailchimp_email_with_tag
from mailings.models import CommonMailingList, CaseMailingList


def add_email_to_common_mailchimp_list(email: str):
    """ Add email to general mailing list """
    """ Добавление email в общий лист рассылки """
    # Adds email to MailChimp audience with name audience_name
    # Добавляет в MailChimp email в аудиторию с названием audience_name
    add_mailchimp_email_with_tag(audience_name='COMMON',
                                 email=email,
                                 tag='COMMON TAG')
    # Adding data to the database
    # Добавление данных в базу данных
    CommonMailingList.objects.get_or_create(email=email)


def add_email_to_case_mailchimp_list(email: str, case_id: Union[int, str]):
    """ Adds email to mailing list for site material """
    """ Добавляет email в лист рассылки по материалу сайта """

    # We get material from the database by its ID
    # Получаем материал из базы данных по его ID
    case = Case.objects.get(pk=case_id)

    # Adds email to MailChimp audience with name audience_name
    # Добавляет в MailChimp email в аудиторию с названием audience_name
    add_mailchimp_email_with_tag(audience_name='CASES',
                                 email=email,
                                 tag=f'Case {case.name}')

    # Adding data to the database
    # Добавление данных в базу данных
    CaseMailingList.objects.get_or_create(email=email)
