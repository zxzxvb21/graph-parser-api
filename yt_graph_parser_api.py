import uvicorn
import requests
import json
import re

from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from typing import Optional
from bs4 import BeautifulSoup


app = FastAPI()
templates = Jinja2Templates(directory='./')


@app.get('/mr_scraping')
async def input_url_count(request: Request):
    return templates.TemplateResponse('ex.html', context={'request': request})


@app.post("/mr_scraping")
async def get_mr_scraping(url: str = Form(), count: Optional[int] = Form(None)):
    if count is None:
        count = 5
    try:
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        data = re.search(r"var ytInitialData = ({.*?});", soup.prettify()).group(1)
        markers_map = json.loads(data)['playerOverlays']['playerOverlayRenderer']['decoratedPlayerBarRenderer'][
            'decoratedPlayerBarRenderer']['playerBar']['multiMarkersPlayerBarRenderer']['markersMap']
        heat_seeker = []

        # 챕터가 나눠진 동영상 대응
        for d in markers_map:
            if d['key'] == 'HEATSEEKER':
                heat_seeker = d

        heatmap_array = \
            heat_seeker['value']['heatmap']['heatmapRenderer']['heatMarkers']
        heatmap_sorted_array = sorted(heatmap_array,
                                      key=(lambda x: x['heatMarkerRenderer']['heatMarkerIntensityScoreNormalized']),
                                      reverse=True)

        result = list(map(lambda x: x['heatMarkerRenderer']['timeRangeStartMillis'], heatmap_sorted_array[0:count]))
        return {'result': result}
    except (KeyError, TypeError):  # MostReplayed 정보가 없음
        return {'result': 'YT404'}
    except AttributeError:  # 요청한 URL이 올바르지 않음
        return {'result': 'YT400'}

if __name__ == "__main__":
    uvicorn.run(app)
