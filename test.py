#!/usr/bin/env python
import sys
import os
import sites.mgtv
import sites.Acfun
import sys

"""write your code for test
"""
if __name__ == "__main__":
    site = sys.argv[1]
    url = sys.argv[2]
    if site == 'mgtv':
        mgtv_test = sites.mgtv.MGTV()
        print(mgtv_test.for_test(orig_url=url))
    if site == 'acfun':
        acfun = sites.Acfun.Acfun()
        item = acfun.get_info("http://www.acfun.tv/v/ac3011409")
        print(acfun.get_urls(item, 'default'))



