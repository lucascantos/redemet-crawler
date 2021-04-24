# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import json
from src.functions.redemet import RedemetImages

def redemet_crawler(event=None, context=None):
    '''
    Downloads images to bucket
    '''
    redemet = RedemetImages()
    radar_list = redemet.get_image_list()
    valid_images = dict(redemet.valid_images(radar_list))
    redemet.download_images(valid_images.values(), event.get('debug'))
    if event.get('debug'):
        print(redemet.radar_images)
    else:
        image_metadata = json.dumps(valid_images, sort_keys=True, default=str)
        redemet.bucket.upload(image_metadata, 'radares.json')
    print("Finished REDEMET image capture process.")
    return True

def check_redemet(event=None, context=None):
    '''
    Checks the lates redemet image
    '''
    from src.helpers.response import make_response
    redemet = RedemetImages()
    radar_list = redemet.get_image_list()
    valid_images = redemet.valid_images(radar_list)
    
    return make_response({'radars': dict(valid_images)})
