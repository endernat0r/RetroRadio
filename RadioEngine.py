from pyradios import RadioBrowser
import vlc

class Engine:
    def __init__(self):
        self.player = None

    def search_stations_by_name(self, name, limit, offset=0):
        rb = RadioBrowser()
        try:
            results = rb.search(name=name, limit=limit, offset=offset, hidebroken=True)
        except Exception as e:
            print(f"Error occurred while searching for stations by name: {e}")
            results = []
        return results

    def search_stations_by_tag(self, tag, limit, offset=0):
        rb = RadioBrowser()
        try:
            results = rb.search(tag=tag, limit=limit, offset=offset, hidebroken=True)
        except Exception as e:
            print(f"Error occurred while searching for stations by tag: {e}")
            results = []
        return results

    def search_stations_by_country(self, country, limit, offset=0):
        rb = RadioBrowser()
        try:
            results = rb.search(country=country, limit=limit, offset=offset, hidebroken=True)
        except Exception as e:
            print(f"Error: {e}")
            results = []
        return results

    def search_stations_by_language(self, language, limit, offset=0):
        rb = RadioBrowser()
        try:
            results = rb.search(language=language, limit=limit, offset=offset, hidebroken=True)
        except Exception as e:
            print(f"Error: {e}")
            results = []
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