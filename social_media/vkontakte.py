import requests


def post_vkontakte(image_path, access_token, group_id, message=''):
    params = {'v': 5.95,
              'access_token': access_token,
              'group_id': group_id
              }

    upload_url = get_upload_url(group_id, params)

    res_dict = upload_photo_to_server(image_path, upload_url)
    params.update(res_dict)

    params.update({'from_group': 1,
                   'message': message
                   })

    if image_path is not None:
        params['attachments'] = get_attachments(params)
        wall_post_to_group(group_id, params)
    elif message:
        wall_post_to_group(group_id, params)


def get_attachments(params):
    attachments_list = ['photo{}_{}'.format(photo_dict['owner_id'], photo_dict['id'])
                        for photo_dict in save_wall_photo(params)]

    return ','.join(attachments_list)


def wall_post_to_group(group_id, params: dict):
    ''' https://vk.com/dev/wall.post '''

    params = params.copy()
    params['owner_id'] = '-{}'.format(group_id)

    res = requests.post('https://api.vk.com/method/wall.post', params=params)
    raise_for_status(res)


def save_wall_photo(params):
    ''' https://vk.com/dev/photos.saveWallPhoto '''

    res = requests.post('https://api.vk.com/method/photos.saveWallPhoto', params=params)
    raise_for_status(res)

    return res.json()['response']


def get_upload_url(group_id, params: dict):
    ''' https://vk.com/dev/photos.getWallUploadServer '''

    params = params.copy()
    params['group_id'] = group_id

    res = requests.get('https://api.vk.com/method/photos.getWallUploadServer', params=params)
    raise_for_status(res)

    return res.json()['response']['upload_url']


def upload_photo_to_server(image_path, upload_url) -> dict:
    ''' https://vk.com/dev/upload_files '''

    with open(image_path, 'rb') as image_file_descriptor:
        files = {'photo': image_file_descriptor}

        res = requests.post(upload_url, files=files)
        raise_for_status(res)

    return res.json()


class VkError(Exception):
    def __init__(self, text):
        self.txt = text


def raise_for_status(response):
    response.raise_for_status()

    resp_dict = response.json()
    if 'error' in resp_dict:
        vk_error = VkError(resp_dict['error']['error_msg'])
        raise vk_error
