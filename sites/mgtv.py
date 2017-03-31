#!/usr/bin/env python
# -*- coding: utf-8 -*-
import common
import json

class MGTV:
    stream_type = [{'video_profile': '标清', 'id': 1},
                   {'video_profile': '高清', 'id': 2},
                   {'video_profile': '超清', 'id': 3},
                   {'video_profile': '蓝光', 'id': 4}]

    id_dic = {i['video_profile']: (i['id']) for i in stream_type}

    urls = [
        {'info_url': 'http://pcweb.api.mgtv.com/player/video?retry=1&video_id={video_id}'},
        {'m3u_url': 'http://mobile.api.hunantv.com/v3/video/getSource?appVersion=4.5.3&device=iPhone&mac=%s&osType=ios'
                    '&osVersion=8.400000&ticket=&videoId={video_id}'},
        {'mp4_url': 'http://mobile.api.hunantv.com/v2/video/getDownloadList?pageCount={page_count}&appVersion=4.5.1'
                    '&osVersion=5.0.1&ticket=&osType=android&channel=anzhi&videoId={video_id}&device=MX4+Pro&userId='
                    '&mac={mac}'}
    ]

    @staticmethod
    def get_vid_from_url(url):
        """Extracts Video ID from URL
        """
        return common.match_re(url, 'v.*?/(\d+).html')

    @staticmethod
    def get_location_from_request(text):
        """Extracts new location from http response
        """
        return common.match_re(text, 'location = "(.*?)"')

    @staticmethod
    def get_mgtv_real_url(url):
        """Give real url by orig url
        """
        return common.get_location(url)

    def get_info_by_vid(self, vid):
        """Extracts contents from api
        """
        result = {}
        index = 0
        url = self.urls[0]['info_url'].format(video_id=vid)
        info = json.loads(common.get_content(url))

        # check offline
        if len(info) == 0:
            result['msg'] = 'offline'
            return result

        # check vip
        if int(info['data']['info']['paymark']) != 0:
            result['msg'] = 'vip'
            return result

        result['file'] = []
        for stream in info['data']['stream']:
            if stream['url'] != "":
                result['file'].append({str(self.id_dic[stream['name']])+':'+stream['url']})
                index += index
        result['msg'] = 'success'
        return result

    def for_test(self, orig_url):
        url = self.get_mgtv_real_url(orig_url)
        vid = self.get_vid_from_url(url)
        if vid is None:
            print("vid not found")
        html = self.get_info_by_vid(vid)
        print(html)







