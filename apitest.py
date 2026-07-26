from pyradios import RadioBrowser, RadioFacets
import vlc

rb = RadioBrowser()

rj = rb.search(tag="jazz")

print(len(rj))

print(rj[0])

print(rj[0]["url_resolved"])

vlc = vlc.MediaPlayer(rj[0]["url_resolved"])

vlc.play()

close = input("Press Enter to close the player...")