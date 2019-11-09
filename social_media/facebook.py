import requests


def post_facebook(img_path, token, object_id, text=''):
    if img_path is not None:
        post_facebook_with_img(img_path, token, object_id, text)

    elif text:
        post_facebook_only_text(token, object_id, text)


def post_facebook_with_img(img_path, token, object_id, text=''):
    '''
    get_token - https://developers.facebook.com/tools/explorer
    API - https://developers.facebook.com/docs/graph-api/photo-uploads/#single
    '''

    params = {
        'caption': text,
        'access_token': token
    }

    with open(img_path, 'rb') as image_file_descriptor:
        files = {'photo': image_file_descriptor}

        response = requests.post('https://graph.facebook.com/{}/photos'.format(object_id), files=files, params=params)
        response.raise_for_status()


def post_facebook_only_text(token, object_id, text):
    '''https://developers.facebook.com/docs/graph-api/using-graph-api#publishing'''

    params = {
        'message': text,
        'access_token': token
    }

    response = requests.post('https://graph.facebook.com/{}/feed'.format(object_id), params=params)
    response.raise_for_status()
