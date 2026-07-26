from pyradios import RadioBrowser
import vlc

class Engine:
    def __init__(self):
        self.player = None

    def search_stations_by_name(self, name, limit):
        rb = RadioBrowser()
        try:
            results = rb.search(name=name, limit=limit)
        except Exception as e:
            print(f"Error occurred while searching for stations by name: {e}")
            results = []
        return results

    def search_stations_by_tag(self, tag, limit):
        rb = RadioBrowser()
        try:
            results = rb.search(tag=tag, limit=limit)
        except Exception as e:
            print(f"Error occurred while searching for stations by tag: {e}")
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

    def radio_search_by_name_and_play(self, name, limit):
        results = self.search_stations_by_name(name, limit)
        if len(results) > 0:
            self.play_station(results[0]["url_resolved"])
            return results[0]
        else:
            return None