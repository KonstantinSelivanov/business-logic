from typing import Optional
from mailchimp3 import MailChimp

from django.conf import settings


def add_mailchimp_email_with_tag(audience_name: str,
                                 email: str,
                                 tag: str) -> None:
    """ Adds email to MailChimp audience with name audience_id """
    """ Добавляет в MailChimp email в аудиторию с названием audience_name """

    # Adding email to list
    # Добавление email в аудиторию (list)
    _add_email_to_mailchimp_audience(
        audience_name=settings.MAILCHIMP_AUDIENCE.get(audience_name),
        email=email)

    # Getting user hash
    # Получение хеша пользователя
    subsciber_hash = _get_mailchimp_subscriber_hash(email=email)

    # Adding a tag for a user
    # Добавление тег для пользователя
    _add_mailchimp_tag(audience_id=audience_name,
                       subsciber_hash=subsciber_hash,
                       tag=tag)


def _get_mailchimp_client() -> MailChimp:
    """ Returns an API client for working with MailChimp """
    """ Возвращает клиент API для работы с MailChimp """
    return MailChimp(
        mc_api=settings.MAILCHIMP_API_KEY,
        mc_user=settings.MAILCHIMP_USERNAME)


def _add_email_to_mailchimp_audience(audience_id: str, email: str) -> None:
    """ Adds email to MailChimp audience with audience_id """
    """ Добавляет email в MailChimp аудиторию с идентификатором audience_id """
    _get_mailchimp_client.lists.members.create(audience_id, {
        'email_address': email,
        'status': 'subscribed'
    })


def _get_mailchimp_subscriber_hash(email: str) -> Optional[str, None]:
    """ Returns email ID in MainChamp or None if email is not found """
    """ Возвращает ID email`а в MainChamp или None, если email не найден """
    members = _get_mailchimp_client().search_members \
        .get(query=email, fields='exact_matches.members.id') \
        .get('exact_matches')
    if not members:
        return None
    return members[0].get('id')


def _add_mailchimp_tag(audience_id: str,
                       subsciber_hash: str,
                       tag: str) -> None:
    """ Adds a tag for email with ID suscriber_hash in audience audience_id """
    """ Добавляет тег tag для email`а с ID suscriber_hash
    в аудитории audience_id """

    _get_mailchimp_client.lists.members.tags.update(
        list_id=audience_id,
        subsciber_hash=subsciber_hash,
        data={'tags': [{'name': 'COMMON TAG', 'status': 'active'}]})
