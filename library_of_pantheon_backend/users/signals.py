from django.db.models.signals import post_save
from library_of_pantheon_backend.users.models import UserSetting


def user_pre_init_create_hash(sender, instance=None, *args, **kwargs):
    if(instance):
        password = instance.password
        instance.set_password(password)
        print('user_pre_init_create_hash: ', instance.password)


def user_pre_save_create_hash(sender, instance=None, *args, **kwargs):
    password = instance.password
    instance.set_password(password)
    print('user_pre_save_create_hash: ', instance.password)


def user_post_save_handler(sender, **kwargs):
    ''' created an instance of User Setting when a new User is created '''
    instance = kwargs.get('instance')
    created = kwargs.get('created', False)
    if created:
        obj = UserSetting()
        obj.save()
        instance.setting = obj
        instance.save()
