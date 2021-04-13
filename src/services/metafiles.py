class RadarImageMetadata:
    def __init__(self):
        self.radar_images = {}
    
    def add_radar(self, code, filepath):
        self.radar_images[code]: filepath
    