from pyradios import RadioBrowser
import vlc

class RadioEngine:
    def __init__(self):
        self.player = None

    def search_stations(self, tag, limit):
        rb = RadioBrowser()
        results = rb.search(tag=tag, limit=limit)
        return results

    def play_station(self, station_url):
        if self.player != None:
            self.player.stop()
        self.player = vlc.MediaPlayer(station_url)
        self.player.play()

    def stop_station(self):
        if self.player != None:
            self.player.stop()

    def set_volume(self, volume):
        if self.player != None:
            self.player.audio_set_volume(volume)