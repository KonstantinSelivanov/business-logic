from mailchimp3 import MailChimp

from django.http import JsonResponse
from django.conf import settings

from .models import CommonMailingList, CaseMailingList
from cases.models import Case


def add_to_common_list_view(request):
    """ A web service that adds email to the general mailing list """
    """ Веб-сервис, добавляющий email в общий лист рассылки """

    # Get email
    # Получение email
    email = request.GET.get('email')
    if not email:
        return JsonResponse({'success': False, 'message': 'Передайте email'})

    # Getting the client's mailchimp ID
    # Получение ID mailchimp клиента
    mailchimp_client = MailChimp(mc_api=settings.MAILCHIMP_API_KEY,
                                 mc_user=settings.MAILCHIMP_USERNAME)

    # Adding email to list
    # Добавление email в аудиторию (list)
    mailchimp_client.lists.members.create(settings.MAILCHIMP_COMMON_LIST_ID, {
        'email_address': email,
        'status': 'subscribed'
    })

    # Getting user hash
    # Получение хеша пользователя
    subsciber_hash = mailchimp_client \
        .search_members \
        .get(query=email, fields='exact_matches.members.id') \
        .get('exact_matches') \
        .get('members')[0] \
        .get('id')

    # Adding a tag for a user
    # Добавление тег для пользователя
    mailchimp_client.lists.members.tags.update(
        list_id=settings.MAILCHIMP_COMMON_LIST_ID,
        subsciber_hash=subsciber_hash,
        data={'tags': [{'name': 'COMMON TAG', 'status': 'active'}]})

    # Adding data to the database
    # Добавление данных в базу данных
    CommonMailingList.objects.get_or_create(email=email)

    return JsonResponse({'success': True})


def add_to_case_list_view(request):
    """
    A web service that adds email to a mailing list for some site material
    """
    """
    Веб-сервис, добавляющий email в лист рассылок по некоторому материалу сайта
    """

    # Get email
    # Получение email
    email = request.GET.get('email')
    if not email:
        return JsonResponse({'success': False, 'message': 'Передайте email'})

    # Get id case
    # Получение id материала
    case_id = request.GET.get('case_id')
    if not case_id:
        return JsonResponse({'success': False, 'message': 'Передайте case_id'})

    # Getting the client's mailchimp ID
    # Получение ID mailchimp клиента
    mailchimp_client = MailChimp(mc_api=settings.MAILCHIMP_API_KEY,
                                 mc_user=settings.MAILCHIMP_USERNAME)

    # Adding email to list
    # Добавление email в аудиторию (list)
    mailchimp_client.lists.members.create(settings.MAILCHIMP_CASE_LIST_ID, {
        'email_address': email,
        'status': 'subscribed'
    })

    # Getting user hash
    # Получение хеша пользователя
    subsciber_hash = mailchimp_client \
        .search_members \
        .get(query=email, fields='exact_matches.members.id') \
        .get('exact_matches') \
        .get('members')[0] \
        .get('id')

    # We get material from the database by its ID
    # Получаем материал из базы данных по его ID
    case = Case.objects.get(pk=case_id)
    case_tag = f'{case.name}'

    # Adding a tag for a user
    # Добавление тег для пользователя
    mailchimp_client.lists.members.tags.update(
        list_id=settings.MAILCHIMP_CASE_LIST_ID,
        subsciber_hash=subsciber_hash,
        data={'tags': [{'name': case_tag, 'status': 'active'}]})

    # Adding data to the database
    # Добавление данных в базу данных
    CaseMailingList.objects.get_or_create(email=email)

    return JsonResponse({'success': True})
