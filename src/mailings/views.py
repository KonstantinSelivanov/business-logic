from django.http import JsonResponse

from .services import (add_email_to_case_mailchimp_list,
                       add_email_to_common_mailchimp_list)


def add_email_to_common_mailchimp_list_view(request):
    """ A web service that adds email to the general mailing list """
    """ Веб-сервис, добавляющий email в общий лист рассылки """

    # Get email
    # Получение email
    email = request.GET.get('email')
    if not email:
        return JsonResponse({'success': False, 'message': 'Передайте email'})
    add_email_to_common_mailchimp_list(email=email)
    return JsonResponse({'success': True})


def add_email_to_case_mailchimp_list_view(request):
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
    add_email_to_case_mailchimp_list(email=email, case_id=case_id)
    return JsonResponse({'success': True})
