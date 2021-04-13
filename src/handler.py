# -*- coding: utf-8 -*-
# !/usr/bin/env python3

def add_image_name(name, tag, json):
    if json["imagens"].get(tag) is None:
        json["imagens"][tag] = []
    json["imagens"][tag] = [name]
    return json


def api_handler(event=None, context=None):
    print(event)
    import requests
    import json
    from src.services.bucket_s3 import BucketS3
    from src.config.radars_tag import radars_tag
    from src.helpers.data import multi_threading

    from src.config.config import API_KEY
    
    def send_request(url, params={}):
        try: 
            return requests.get(url, params, timeout=20)
        except TimeoutError:
            LOG.error(f"Timeout: {url}")


    # Get redemet payload
    params = {
        'api_key': API_KEY,
        'anima': 8
    }
    url = 'https://api.atd-1.com/produtos/radar/maxcappi'
    redemet_response = send_request(url, params)

    # Get locations image path
    last_image_id = params['anima']-1
    
    radar_list = redemet_response.json()['data']['radar'][last_image_id]

    for index, radar in enumerate(radar_list):
        image_url = radar['path']
        if image_url is None:
            continue        
        r_tag = radar['localidade']
        file_name = f"{r_tag}_{image_url.split('/')[-1]}"
        if BucketS3().check_exist_file(file_name) is True:
            LOG.error(f"The file {file_name} already exists, we will continue without making the request to REDEMET.")
            add_image_name(file_name, r_tag, radars_tag)
            radar_list[index]['path'] = None
            continue

    valid_radars = [radar for radar in radar_list if radar['path']] 
    def _grab_images(radar):
        response = send_request(radar['path'])
        return response

    for image_response, radar in zip(multi_threading(_grab_images, valid_radars), valid_radars):
        image_url = radar['path']
        r_tag = radar['localidade']
        file_name = f"{r_tag}_{image_url.split('/')[-1]}"
        if image_response is None:
            LOG.error(f"Location Code: {radar['localidade']}")
            continue

        #Upload image to bucket
        if event.get('debug'):
            response_bucket = True
            print(file_name)
            with open(f"out/{file_name}", 'wb') as f:
                f.write(image_response.content)                
        else:
            response_bucket = BucketS3().upload_file(image_response.content, f"imagens/{file_name}", force=True)
        if response_bucket is True:
            add_image_name(file_name, r_tag, radars_tag)

    if event.get('debug'):
        print(radars_tag)
    else:
        BucketS3().upload_file(
            json.dumps(radars_tag, sort_keys=True, default=str),
            'radares.json',
            force=True,
            content_type="application/json",
        )
    LOG.info("Finished REDEMET image capture process.")
    return True