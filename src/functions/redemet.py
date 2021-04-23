
from src.services.s3 import S3, MockS3
from src.services.metafiles import RadarImageMetadata
from src.helpers.requests import send_request
from src.helpers.data import multi_threading
from src.configs.redemet_info import REDEMET_INFO

class RedemetImages:
    def __init__(self):
        self.bucket = S3()
        self.radars_meta = RadarImageMetadata()

    def get_image_list(self):
        params = {
            'api_key': REDEMET_INFO['api_key'],
            'anima': 8
        }
        url = REDEMET_INFO.pop('url')
        last_image_id = params['anima']-1
        redemet_response = send_request(url, params)
        if redemet_response.status_code == 200:
            return redemet_response.json()['data']['radar'][last_image_id]
        else:
            raise AssertionError(redemet_response.content)
    
    def valid_images(self, image_list):
        for index, radar in enumerate(image_list):
            image_url = radar['path']
            if image_url:    
                radar_tag = radar['localidade']
                file_name = f"{radar_tag}_{image_url.split('/')[-1]}"
                if self.bucket.check_exist_file(file_name):
                    print(f"The file {file_name} already exists, we will continue without making the request to REDEMET.")
                    self.radars_meta.add_radar(radar_tag, file_name)
                    image_list[index]['path'] = None
            yield image_url
    
    def download_images(self, valid_radars, debug=False):
        def _grab_images(radar):
            response = send_request(radar['path'])
            return response

        for image_response, radar in zip(multi_threading(_grab_images, valid_radars), valid_radars):
            image_url = radar['path']
            radar_tag = radar['localidade']
            file_name = f"{radar_tag}_{image_url.split('/')[-1]}"
            if image_response is None:
                print(f"Location Code: {radar['localidade']}")
                continue
            #Upload image to bucket
            if debug:
                print(file_name)
                with open(f"out/{file_name}", 'wb') as f:
                    f.write(image_response.content)                
            else:
                self.bucket.upload(image_response.content, f"imagens/{file_name}")
            self.radars_meta.add_radar(radar_tag, file_name)