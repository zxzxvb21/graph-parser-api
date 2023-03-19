import os
import pdb
import sys
from datetime import timedelta

def exec(url, user_time, moment):
    cmd = "ffmpeg -ss {} -i $(yt-dlp -f best -g '{}') -t {} -c copy DOWNLOAD_NAME.mp4"
    start_time = moment - (user_time/2 + 5)
    if start_time < 0:
        start_time = 0
    total_time = moment + (user_time/2 + 5)

    start_time = timedelta(seconds=start_time)
    total_time = timedelta(seconds=total_time)

    cmd = cmd.format(start_time, url, total_time)
    os.system(cmd)
    user_time = timedelta(seconds=user_time+5)
    cmd = "ffmpeg -i DOWNLOAD_NAME.mp4 -ss 00:00:05 -to {} output.mp4".format(user_time)
    os.system(cmd)
    os.remove('DOWNLOAD_NAME.mp4')

if __name__=="__main__":
    video_url = sys.argv[1]
    if video_url == '-u':
        target_url = sys.argv[2]
    user_want_time = sys.argv[3]
    moment = sys.argv[4]
    if target_url:
        exec(target_url, int(user_want_time), int(moment))
    else:
        print(f'no Video url.')
