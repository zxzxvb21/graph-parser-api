#
# command to run -> python3 main.py &
# url of openAPI -> http://15.165.149.51:5000/docs , http://15.165.149.51:5000/redoc
import pdb

import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from scraping import Scrap
from video import Video
from io import BytesIO

app = FastAPI()

@app.post("/scraping/")
def execScraping(url: str, count: int, time: int):
    if url is None:
        raise HTTPException(status_code = 400, detail = "URL Link is None")
    try:
        scrap = Scrap(url, count, time)
        scrap_info = scrap.get_all()
    except Exception:
        raise HTTPException(status_code = 404, detail = "Parse Info is None")

    return {'success': True, 'result': scrap_info}

@app.post("/yt_download/")
def execDownload(url: str, user_want_time: int, start_time: int, end_time: int):
    video = Video(url, user_want_time, start_time, end_time)
    # download video to server
    result = video.getShortByTime(url, user_want_time, start_time, end_time)
    # upload video to user
    if result['msg'] is not None:
        return {'success': False, 'msg': result['msg']}
    
    with open(f"./"+result['file_name']+".mp4", "rb") as video_file:
        video_contents = video_file.read()
        return StreamingResponse(BytesIO(video_contents), media_type="video/mp4")


if __name__ == "__main__" :
    #uvicorn.run(app, host="172.31.3.9", port = 5000)
    uvicorn.run(app)

