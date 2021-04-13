class RadarImageMetadata:
    def __init__(self):
        self.radar_images = {}
    
    def add_radar(self, radar_code, filepath):
        print(radar_code)
        self.radar_images[radar_code] = filepath
    