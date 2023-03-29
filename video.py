import os
import pdb
import subprocess

class Video:

    def __init__(self, url, user_want_time, moment):
        self.url = url
        self.user_want_time = user_want_time
        self.moment = moment

    def convert_ms_to_hms(self, ms):
        seconds = int((ms / 1000) % 60)
        minutes = int((ms / (1000 * 60)) % 60)
        hours = int((ms / (1000 * 60 * 60)) % 24)
        return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)

    def Download_cut(self, url: str, user_want_time: int, moments: list):
        user_want_time = user_want_time * 1000
        for idx, moment in enumerate(moments):
            cmd = "ffmpeg -ss {} -i $(yt-dlp -f best -g '{}') -t {} -c copy DOWNLOAD.mp4"
            start_time = int(moment) - (int(user_want_time)/2 + 5000)
            if start_time < 0:
                start_time = 0
            total_time = int(moment) + (int(user_want_time)/2 + 5000)
            start_time = self.convert_ms_to_hms(start_time)
            total_time = self.convert_ms_to_hms(total_time)

            cmd = cmd.format(start_time, url, total_time)
            os.system(cmd)

            tmp_time = self.convert_ms_to_hms(user_want_time + 5000)

            cmd = "ffmpeg -i DOWNLOAD.mp4 -ss 00:00:05 -to {} {}.mp4".format(tmp_time, moment)
            os.system(cmd)
            
            os.remove("DOWNLOAD.mp4")

        return {'success' : True}

    def Upload(self):
        return
