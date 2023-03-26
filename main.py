#
# command to run -> python3 main.py &
# url of openAPI -> http://15.165.149.51:5000/docs , http://15.165.149.51:5000/redoc
import pdb

import uvicorn
from fastapi import FastAPI
from scraping import Scrap
from video import Video

app = FastAPI()

@app.post("/scraping/")
async def execScraping(url: str, count: int, time: int):

    if url is None:
        return {'success': False, 'msg': 'not found url'}

    scrap = Scrap(url, count)
    scrap_info = scrap.get_all()
    if not scrap_info['result']:
        return {'success': False, 'err': scrap_info.result}
    video = Video(url, time, scrap_info['mr_info'])
    result = video.Download_cut(url, time, scrap_info['mr_info'])

    return {'success' : True, 'result' : result }

if __name__ == "__main__" :
    #uvicorn.run(app, host="172.31.3.9", port = 5000)
    uvicorn.run(app)
