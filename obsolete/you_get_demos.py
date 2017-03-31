#!/usr/bin/env python
import common
import re
import json
import random
import time


def calcTimeKey(t):
    ror = lambda val, r_bits, : ((val & (2**32-1)) >> r_bits%32) |  (val << (32-(r_bits%32)) & (2**32-1))
    return ror(ror(t,773625421%13)^773625421,773625421%17)


def decode(data):
    version = data[0:5]
    if version.lower() == b'vc_01':
        #get real m3u8
        loc2 = data[5:]
        length = len(loc2)
        loc4 = [0]*(2*length)
        for i in range(length):
            loc4[2*i] = loc2[i] >> 4
            loc4[2*i+1]= loc2[i] & 15
        loc6 = loc4[len(loc4)-11:]+loc4[:len(loc4)-11]
        loc7 = [0]*length
        for i in range(length):
            loc7[i] = (loc6[2 * i] << 4) + loc6[2*i+1]
        return ''.join([chr(i) for i in loc7])
    else:
        # directly return
        return data


def video_info(vid,**kwargs):
    url = 'http://api.letv.com/mms/out/video/playJson?id={}&platid=1&splatid=101&format=1&tkey={}&domain=www.letv.com'.format(vid,calcTimeKey(int(time.time())))
    r = common.get_content(url, decoded=False)
    info = json.loads(str(r, "utf-8"))

    stream_id = None
    support_stream_id = info["playurl"]["dispatch"].keys()
    if "stream_id" in kwargs and kwargs["stream_id"].lower() in support_stream_id:
        stream_id = kwargs["stream_id"]
    else:
        print("Current Video Supports:")
        for i in support_stream_id:
            print("\t--format",i,"<URL>")
        if "1080p" in support_stream_id:
            stream_id = '1080p'
        elif "720p" in support_stream_id:
            stream_id = '720p'
        else:
            stream_id =sorted(support_stream_id,key= lambda i: int(i[1:]))[-1]

    url =info["playurl"]["domain"][0]+info["playurl"]["dispatch"][stream_id][0]
    ext = info["playurl"]["dispatch"][stream_id][1].split('.')[-1]
    url+="&ctv=pc&m3v=1&termid=1&format=1&hwtype=un&ostype=Linux&tag=letv&sign=letv&expect=3&tn={}&pay=0&iscpn=f9051&rateid={}".format(random.random(),stream_id)
    # print(url)
    r2=common.get_content(url, decoded=False)
    info2=json.loads(str(r2, "utf-8"))
    # hold on ! more things to do
    # to decode m3u8 (encoded)
    m3u8 = common.get_content(info2["location"],decoded=False)
    print(m3u8)
    m3u8_list = decode(m3u8)
    print(m3u8_list)
    urls = re.findall(r'^[^#][^\r]*',m3u8_list,re.MULTILINE)
    return ext,urls


if __name__ == "__main__":
    ext, urls = video_info(28404897)
    data = "b'vc_01'adfsadfas"
    print(data[5:])