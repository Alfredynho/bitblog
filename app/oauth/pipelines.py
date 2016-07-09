# -*- encoding:utf-8 -*-

def get_avatar(backend, strategy, details, response, user=None, *args, **kwargs):

    url = None
    if backend.name == 'facebook':
        url = "http://graph.facebook.com/%s/picture?type=large" % response['id']
    elif backend.name == 'twitter':
        url = response.get('profile_image_url', '').replace('_normal', '')

    if url:
        # user.avatar = url
        # user.save()
        pass
