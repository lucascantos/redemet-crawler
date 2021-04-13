# -*- coding: utf-8 -*-
# !/usr/bin/env python3

def api_handler(event=None, context=None):
    import json
    from src.services.s3 import S3
    from src.services.metafiles import RadarImageMetadata
    from src.helpers.requests import send_request
    from src.helpers.data import multi_threading
    from src.configs.redemet_info import REDEMET_INFO
    print(event)

    bucket = S3()
    radars_meta = RadarImageMetadata()
    params = {
        'api_key': REDEMET_INFO['api_key'],
        'anima': 8
    }
    url = REDEMET_INFO.pop('url')
    last_image_id = params['anima']-1

    redemet_response = send_request(url, params)
    if redemet_response.status_code == 200:
        radar_list = redemet_response.json()['data']['radar'][last_image_id]
    else:
        raise AssertionError(redemet_response.content)

    for index, radar in enumerate(radar_list):
        image_url = radar['path']
        if image_url is None:
            continue        
        radar_tag = radar['localidade']
        file_name = f"{radar_tag}_{image_url.split('/')[-1]}"
        if bucket.check_exist_file(file_name):
            print(f"The file {file_name} already exists, we will continue without making the request to REDEMET.")
            radars_meta.add_radar(radar_tag, file_name)
            radar_list[index]['path'] = None
            continue

    # Download images and save them
    def _grab_images(radar):
        response = send_request(radar['path'])
        return response
    valid_radars = [radar for radar in radar_list if radar['path']] 

    for image_response, radar in zip(multi_threading(_grab_images, valid_radars), valid_radars):
        image_url = radar['path']
        radar_tag = radar['localidade']
        file_name = f"{radar_tag}_{image_url.split('/')[-1]}"
        if image_response is None:
            print(f"Location Code: {radar['localidade']}")
            continue

        #Upload image to bucket
        if event.get('debug'):
            print(file_name)
            with open(f"out/{file_name}", 'wb') as f:
                f.write(image_response.content)                
        else:
            bucket.upload(image_response.content, f"imagens/{file_name}")
            radars_meta.add_radar(radar_tag, file_name)

    if event.get('debug'):
        print(radars_meta)
    else:
        image_metadata = json.dumps(radars_meta.radar_images, sort_keys=True, default=str)
        bucket.upload(image_metadata, 'radares.json')
    print("Finished REDEMET image capture process.")