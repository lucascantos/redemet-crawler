# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import json
from src.functions.redemet import RedemetImages

def redemet_crawler(event=None, context=None):
    redemet = RedemetImages()
    radar_list = redemet.get_image_list()
    updated_radar_list = redemet.valid_images(radar_list)
    valid_radars = [radar for radar in updated_radar_list if radar['path']] 
    redemet.download_images(valid_radars)
    if event.get('debug'):
        print(redemet.radars_meta.radar_images)
    else:
        image_metadata = json.dumps(redemet.radars_meta.radar_images, sort_keys=True, default=str)
        redemet.bucket.upload(image_metadata, 'radares.json')
    print("Finished REDEMET image capture process.")

def check_redemet(event=None, context=None):
    from src.helpers.response import make_response
    redemet = RedemetImages()
    radar_list = redemet.get_image_list()
    valid_images = redemet.valid_images(radar_list)
    
    return make_response({'radars': dict(valid_images)})
