#
# command to run -> python3 main.py &
# url of openAPI -> http://15.165.149.51:5000/docs , http://15.165.149.51:5000/redoc
import pdb

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from scraping import Scrap
from video import Video

app = FastAPI()

@app.post("/scraping/")
def execScraping(url: str, count: int, time: int):

    if url is None:
        raise HTTPException(status_code = 400, detail = "URL Link is None")
    try:
        scrap = Scrap(url, count)
        scrap_info = scrap.get_all()
    except Exception:
        raise HTTPException(status_code = 404, detail = "Parse Info is None")

    video = Video(url, time, scrap_info['mr_info'])
    result = video.Download_cut(url, time, scrap_info['mr_info'])

    if 'msg' in result:
        return {'success' : False, 'result' : result}

    return {'success' : True, 'result' : result }

#@app.get("/download/")
#def execDownloadFile(video_id: str):
#	file_path, filename = Video.Upload(moment)
#    return FileResponse(file_path, media_type="application/octet-stream", filename=filename)

if __name__ == "__main__" :
    #uvicorn.run(app, host="172.31.3.9", port = 5000)
    uvicorn.run(app)

