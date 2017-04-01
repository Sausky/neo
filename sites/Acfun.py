#!/usr/bin/env python
import common
import json
import base64
import sys


class Acfun:
    streams = {}
    stream_types = [
        {'id': 'mp4hd3', 'alias-of': 'hd3'},
        {'id': 'hd3', 'container': 'flv', 'video_profile': '1080P'},
        {'id': 'mp4hd2', 'alias-of': 'hd2'},
        {'id': 'hd2', 'container': 'flv', 'video_profile': '超清'},
        {'id': 'mp4hd', 'alias-of': 'mp4'},
        {'id': 'mp4', 'container': 'mp4', 'video_profile': '高清'},
        {'id': 'flvhd', 'container': 'flv', 'video_profile': '标清'},
        {'id': 'flv', 'container': 'flv', 'video_profile': '标清'},
        {'id': '3gphd', 'container': '3gp', 'video_profile': '标清（3GP）'},
    ]

    def rc4(self, a, c):
        """special function to decode secret data
        :param a, c:
        :return:result
        """
        f = h = 0
        b = list(range(256))
        result = ''
        while h < 256:
            f = (f + b[h] + ord(a[h % len(a)])) % 256
            b[h], b[f] = b[f], b[h]
            h += 1
        q = f = h = 0
        while q < len(c):
            h = (h + 1) % 256
            f = (f + b[h]) % 256
            b[h], b[f] = b[f], b[h]
            if isinstance(c[q], int):
                result += chr(c[q] ^ b[(b[h] + b[f]) % 256])
            else:
                result += chr(ord(c[q]) ^ b[(b[h] + b[f]) % 256])
            q += 1

        return result

    def get_info(self, orig_url):
        """Get information by orig_url
        :param orig_url:
        :return: info {}
        """
        # get vid
        version = 11.5
        vid = common.match_re(orig_url, '/v/ac(\d+)', 'ac=(\d+)')[0]
        if vid is None:
            return -3
        # get cid  TODO remove
        cid_url = "http://cdn.aixifan.com/acfun-H5/public/script/touch-youku.min.js?v="+str(version)
        content = common.get_content(url=cid_url)
        cid = common.match_re(content, 'client_id:"(.*?)"')
        if cid is None:
            return -3
        # get ids
        content_url = 'http://api.aixifan.com/contents/{}'.format(str(vid))
        print(content_url)
        header = {'deviceType': 2, 'Referer': orig_url}
        vids_content = json.loads(common.get_content(content_url, headers=header))
        for vids in vids_content['data']['videos']:
            smart_vid = vids['videoId']
            if smart_vid is not None:
                smart_url = "http://api.aixifan.com/plays/youku/{}".format(str(smart_vid))
                print(smart_url)
                header['Referer'] = 'http://m.acfun.cn/ykplayer?date=undefined'
                smart_content = json.loads(common.get_content(url=smart_url, headers=header))
                client_id = smart_content['data']['sourceId']
                embsig = smart_content['data']['embsig']
                return {'video_id': smart_vid, 'source_id': client_id, 'embsig': embsig}

    def get_urls(self, item, audio_lang):
        url = "http://aplay-vod.cn-beijing.aliyuncs.com/acfun/web?vid="+str(item['source_id'])+"&ct=85&ev=2&cid=908a5" \
                "19d032263f8&sign="+str(item['embsig'])
        content = json.loads(common.get_content(url=url))
        str_data = self.rc4('2da3ca9e', base64.b64decode(content['data']))
        data = json.loads(str_data)
        stream_types = dict([(i['id'], i) for i in self.stream_types])
        files = {}
        for stream in data['stream']:
            stream_id = stream['stream_type']
            if stream_id in stream_types and stream['audio_lang'] == audio_lang:
                if 'alias-of' in stream_types[stream_id]:
                    stream_id = stream_types[stream_id]['alias-of']

                if stream_id not in self.streams:
                    self.streams[stream_id] = {
                        'container': stream_types[stream_id]['container'],
                        'video_profile': stream_types[stream_id]['video_profile'],
                        'size': stream['size'],
                        'pieces': [{
                            'fileid': stream['stream_fileid'],
                            'segs': stream['segs']
                        }]
                    }
                else:
                    self.streams[stream_id]['size'] += stream['size']
                    self.streams[stream_id]['pieces'].append({
                        'fileid': stream['stream_fileid'],
                        'segs': stream['segs']
                    })

        return self.streams
if __name__ == "__main__":
    acfun = Acfun()
    item = acfun.get_info("http://www.acfun.tv/v/ac3011409")
    print(acfun.get_urls(item, 'default'))
