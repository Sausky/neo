#!/usr/bin/env python
import sys
import os
import sites.mgtv


if __name__ == "__main__":
    sys.path.append(os.path.dirname(sys.path[0]))
    print(mgtv.get_vid_from_url('http://www.hunantv.com/v/2/309238/f/3761306.html'))

