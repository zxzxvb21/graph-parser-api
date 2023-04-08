import os
import pdb
import subprocess

class Video:

    def __init__(self, url, user_want_time, start_time, end_time):
        self.url = url
        self.user_want_time = user_want_time
        self.start_time = start_time
        self.end_time = end_time
        self.video_id = url.split('=')[1]

    def convert_ms_to_hms(self, ms):
        seconds = int((ms / 1000) % 60)
        minutes = int((ms / (1000 * 60)) % 60)
        hours = int((ms / (1000 * 60 * 60)) % 24)
        return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)

    def getShortByTime(self, url: str, user_want_time: int, start_time: int, end_time: int):
        user_want_time = user_want_time * 1000
        file_name_list = []
        if not os.path.isfile(self.video_id):
            # os.remove(self.video_id+'.mp4')
            cmd = "ffmpeg -ss {} -i $(yt-dlp -f best -g '{}') -t {} -c copy {}.mp4"

            start_time = self.convert_ms_to_hms(int(start_time) - 5000)
            end_time = self.convert_ms_to_hms(int(end_time) + 5000)

            cmd = cmd.format(start_time, url, total_time, self.video_id)

            result = os.system(cmd)
            if result != 0:
                return {'msg': 'Download Fail'}

        tmp_time = self.convert_ms_to_hms(user_want_time + 5000)
        file_name = self.video_id + '_' + str(start_time)
        cmd = "ffmpeg -i {}.mp4 -ss 00:00:05 -to {} {}.mp4".format(self.video_id, tmp_time, file_name)
        if result != 0:
            return {'msg': 'Cut Fail'}
        file_name = self.video_id + '_' + str(start_time)

        # os.remove("{}.mp4".format(self.video_id))
        return file_name

        # FIXME not list -> only one
        #for idx, moment in enumerate(moments):
        #    if os.path.isfile(self.video_id):
        #        os.remove(self.video_id+'.mp4')
        #    cmd = "ffmpeg -ss {} -i $(yt-dlp -f best -g '{}') -t {} -c copy {}.mp4"
        #    start_time = int(moment) - (int(user_want_time)/2 + 5000)
        #    if start_time < 0:
        #        start_time = 0
        #    total_time = int(moment) + (int(user_want_time)/2 + 5000)
        #    start_time = self.convert_ms_to_hms(start_time)
        #    total_time = self.convert_ms_to_hms(total_time)
        #    
        #    cmd = cmd.format(start_time, url, total_time, self.video_id)
        #    
        #    result = os.system(cmd)
        #    if result != 0:
        #        return {'msg' : 'Download Fail'}
        #    
        #    tmp_time = self.convert_ms_to_hms(user_want_time + 5000)

        #    cmd = "ffmpeg -i {}.mp4 -ss 00:00:05 -to {} {}.mp4".format(self.video_id, tmp_time, self.video_id+'_'+str(idx))
        #    
        #    result = os.system(cmd)
        #    if result != 0:
        #        return {'msg' : 'Cut Fail'}
        #    file_name_list.append(self.video_id+ '_' + str(idx))
   # 
        #    os.remove("{}.mp4".format(self.video_id))

        #return {'file_name' : file_name_list}
