#!/usr/bin/env python
import re
import socket
import logging
from urllib import request, parse, error
from http import cookiejar


fake_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'UTF-8,*;q=0.5',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'
}

cookies = None


def match_re(text, *patterns):
    """ Scans through a string for substring matched some patterns (first-subgroups only)
    :param text: A string to be scanned
    :param patterns: arbitrary number of regex patterns
    :return:
            When only one pattern is given, returns a string (None if no match found)
            When more than one pattern are given, returns a list of strings ([] if no match found)
    """

    if len(patterns) == 1:
        pattern = patterns[0]
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        else:
            return None
    else:
        ret = []
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                ret.append(match.group(1))
        return ret


def get_location(url):
    try:
        response = request.urlopen(url)
        # urllib will follow redirections and it's too much code to tell urllib
        # not to do that
        return response.geturl()
    except socket.timeout:
        print('request timeout')
        exit()
    except request.HTTPError as e:
        print(e.code)
    except request.URLError as e:
        print(e.reason)
        exit()

    return "fail"


def get_content(url, headers={}, decoded=True):
    """Gets the content of a URL via sending a HTTP GET request.

    Args:
        url: A URL.
        headers: Request headers used by the client.
        decoded: Whether decode the response body using UTF-8 or the charset specified in Content-Type.

    Returns:
        The content as a string.
    """

    logging.debug('get_content: %s' % url)

    req = request.Request(url, headers=headers)
    if cookies:
        cookies.add_cookie_header(req)
        req.headers.update(req.unredirected_hdrs)

    # try ten times
    for i in range(10):
        try:
            response = request.urlopen(req)
            break
        except socket.timeout:
            logging.debug('request attempt %s timeout' % str(i + 1))

    data = response.read()

    # Handle HTTP compression for gzip and deflate (zlib)
    content_encoding = response.getheader('Content-Encoding')
    if content_encoding == 'gzip':
        data = ungzip(data)
    elif content_encoding == 'deflate':
        data = undeflate(data)

    # Decode the response body
    if decoded:
        charset = match_re(response.getheader('Content-Type'), r'charset=([\w-]+)')
        if charset is not None:
            data = data.decode(charset)
        else:
            data = data.decode('utf-8', 'ignore')

    return data


def undeflate(data):
    """Decompresses data for Content-Encoding: deflate.
    (the zlib compression is used.)
    """
    import zlib
    decompressobj = zlib.decompressobj(-zlib.MAX_WBITS)
    return decompressobj.decompress(data)+decompressobj.flush()


def ungzip(data):
    """Decompresses data for Content-Encoding: gzip.
    """
    from io import BytesIO
    import gzip
    buffer = BytesIO(data)
    f = gzip.GzipFile(fileobj=buffer)
    return f.read()


def is_json(text):
    """Check the text if it is json
    :param text:
    :return:
            if text is json , return True
            else, return False
    """