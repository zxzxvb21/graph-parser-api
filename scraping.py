import pdb

import traceback
import requests
import json
import re
from bs4 import BeautifulSoup
from exception import UnicornException


class Scrap:

    def __init__(self, url, count, time):
        self.url = url
        self.count = count
        self.time = time
        try:
            soup = BeautifulSoup(requests.get(url).text, "html.parser")
            data = re.search(r"var ytInitialData = ({.*?});", soup.prettify()).group(1)
        except (KeyError, TypeError):  # MostReplayed 정보가 없음
            error_msg = traceback.format_exc()
            raise UnicornException(error_msg)
        except AttributeError:  # 요청한 URL이 올바르지 않음
            error_msg = traceback.format_exc()
            raise UnicornException(error_msg)

        self.mr_info, self.replayed_ratio, self.video_length = self.get_yt_mr(data, count)
        self.title = self.get_yt_title(data)
        self.owner = self.get_yt_owner(data)
        self.upload_date = self.get_yt_upload_date(data)
        self.tags = self.get_yt_tags(data)
        self.view_count = self.get_yt_view_count(data)
        self.video_id = self.get_video_id(data)

    def get_yt_mr(self, data, count):
        markers_map = json.loads(data)['playerOverlays']['playerOverlayRenderer']['decoratedPlayerBarRenderer'][
            'decoratedPlayerBarRenderer']['playerBar']['multiMarkersPlayerBarRenderer']['markersMap']
        heat_seeker = []

        # 챕터가 나눠진 동영상 대응
        for d in markers_map:
            if d['key'] == 'HEATSEEKER':
                heat_seeker = d
        heatmap_array = heat_seeker['value']['heatmap']['heatmapRenderer']['heatMarkers']
        heatmap_sorted_array = sorted(heatmap_array,
                                      key=(lambda x: x['heatMarkerRenderer']['heatMarkerIntensityScoreNormalized']),
                                      reverse=True)
        result = list(filter(lambda x: x['timeRangeStartMillis'] != 0, map(lambda x: x['heatMarkerRenderer'], heatmap_sorted_array)))[0:count]
        mr_list = [mr['timeRangeStartMillis'] for mr in result]
        ratio = [round(mr['heatMarkerIntensityScoreNormalized'] * 100, 2) for mr in result]
        video_length = heatmap_array[-1]['heatMarkerRenderer']['markerDurationMillis'] * 100
        return mr_list, ratio, video_length

    def get_yt_title(self, data):
        return json.loads(data)['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0][
            'videoPrimaryInfoRenderer']['title']['runs'][0]['text']

    def get_yt_owner(self, data):
        owner_info = json.loads(data)['contents']['twoColumnWatchNextResults']['results']['results']['contents'][1][
            'videoSecondaryInfoRenderer']['owner']['videoOwnerRenderer']
        owner = owner_info['title']['runs'][0]['text']
        owner_url = owner_info['navigationEndpoint']['browseEndpoint']['canonicalBaseUrl']
        owner_subscribers = owner_info['subscriberCountText']['simpleText']
        return {
            'owner': owner,
            'owner_url': owner_url,
            'owner_subscribers': owner_subscribers
        }

    def get_yt_upload_date(self, data):
        return json.loads(data)['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0][
            'videoPrimaryInfoRenderer']['dateText']['simpleText']

    def get_yt_tags(self, data):
        try:
            tags_data = json.loads(data)['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0][
                'videoPrimaryInfoRenderer']['superTitleLink']['runs']
            return list(filter(lambda x: x != ' ', map(lambda x: x['text'], tags_data)))
        except KeyError:
            return []

    def get_yt_view_count(self, data):
        return json.loads(data)['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0][
            'videoPrimaryInfoRenderer']['viewCount']['videoViewCountRenderer']['viewCount']['simpleText']
    
    def reform_mr_info(self, mr_info, time, ratio):
        mr_list = []
        time = time * 1000
        for mr, rat in zip(mr_info, ratio):
            start_time = int(mr) - int(time)/2
            end_time = int(mr) + int(time)/2
            if start_time < 0:
                start_time = 0
                end_time = time
                mr_list.append({'start_time' : start_time, 'end_time' : end_time, 'ratio' : rat})
            elif end_time > self.video_length:
                end_time = self.video_length
                mr_list.append({'start_time' : start_time, 'end_time' : end_time, 'ratio' : rat})
            else:
                mr_list.append({'start_time' : start_time, 'end_time' : end_time, 'ratio' : rat})
        return mr_list

    def get_video_id(self, data):
        return json.loads(data)['currentVideoEndpoint']['watchEndpoint']['videoId']

    def get_all(self):
        scrap_info = {
            'url': self.url,
            'mr_info': self.reform_mr_info(self.mr_info, self.time, self.replayed_ratio),
            'title': self.title,
            'owner': self.owner,
            'upload_date': self.upload_date,
            'tags': self.tags,
            'view_count': self.view_count,
            'video_length': self.video_length,
            'video_id': self.video_id,
        }
        return scrap_info
