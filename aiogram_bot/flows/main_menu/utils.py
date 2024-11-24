from asgiref.sync import sync_to_async
from apps.clients.models import Client


@sync_to_async
def save_user_data(user_data):
    user, created = Client.objects.get_or_create(
        user_id=user_data.id,
        defaults={
            'first_name': user_data.first_name,
            'last_name': user_data.last_name,
            'username': user_data.username,
            'language_code': user_data.language_code,
        }
    )

    if not created:
        # Если пользователь уже существует, обновляем информацию
        user.first_name = user_data.first_name
        user.last_name = user_data.last_name
        user.username = user_data.username
        user.language_code = user_data.language_code
        user.save()

    return user