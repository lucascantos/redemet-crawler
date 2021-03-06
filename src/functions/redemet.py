
from src.services.s3 import S3, MockS3
from src.helpers.response import send_request
from src.helpers.data import multi_threading
from src.configs.redemet_info import REDEMET_INFO
    
class RedemetImages:
    def __init__(self):
        self.bucket = S3()
        self.meta_file = 'redemet-images.json'
        try:
            self.radar_images = self.bucket.load(self.meta_file)
        except:
            self.radar_images = {}

    def get_image_list(self):
        '''
        Get radar image information from REDEMET Api
        '''
        params = {
            'api_key': REDEMET_INFO.get('api_key'),
            'anima': 8
        }
        url = REDEMET_INFO.get('url')
        last_image_id = params['anima']-1
        redemet_response = send_request(url, params)
        if redemet_response.status_code == 200:
            return redemet_response.json()['data']['radar'][last_image_id]
        else:
            raise AssertionError(redemet_response.content)
    
    def valid_images(self, image_list):
        '''
        Filter only valid images 
        :params image_list: Image data from radars
        '''
        for index, radar in enumerate(image_list):
            image_url = radar['path']
            if image_url:    
                radar_tag = radar['localidade']
                filepath = f"{radar_tag}/{image_url.split('/')[-1]}"
                self.radar_images.setdefault(radar_tag, radar)
                if self.bucket.check_exist_file(filepath):
                    self.radar_images[radar_tag]['s3'] = filepath
            yield radar_tag, self.radar_images[radar_tag]
    
    def download_images(self, valid_radars, debug=False):
        '''
        Download images which are not already on the bucket
        :params valid_radars: Radar image list with a path
        :params debug: Boolean in case you want to sabe localily or not
        '''
        def _grab_images(radar):
            response = send_request(radar['path'])
            return response

        new_images = [radar for radar in valid_radars if not radar.get('s3')]
        for image_response,radar in zip(multi_threading(_grab_images, new_images), new_images):
            image_url = radar['path']
            radar_tag = radar['localidade']
            filename = f"{radar_tag}/{image_url.split('/')[-1]}"
            if image_response is None:
                print(f"Location Code: {radar['localidade']}")
                continue
            #Upload image to bucket
            if debug:
                print(f"{radar_tag}_{image_url.split('/')[-1]}")
                with open(f"out/{radar_tag}_{image_url.split('/')[-1]}", 'wb') as f:
                    f.write(image_response.content)                
            else:
                self.bucket.upload(image_response.content, filename)
                self.radar_images[radar_tag]['s3'] = filename