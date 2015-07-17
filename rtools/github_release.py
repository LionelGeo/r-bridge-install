from __future__ import unicode_literals
from __future__ import print_function

import arcpy
import json
import sys
import textwrap
try:
    import urllib.request as request
except ImportError:
    import urllib2 as request

from .utils import versiontuple

API_URL = "https://api.github.com"

# TODO use actual API instead of stub
# latest_url = '{API_URL}/repos/{org}/{project}/releases/latest'.format(
#            API_URL=API_URL, org=org, project=project)
latest_url = "https://4326.us/R/latest.json"


def save_url(url, output_path):
    """Save a URL to disk."""
    r = request.urlopen(url)
    if r.headers['content-type'] == 'application/zip' and r.code == 200:
        arcpy.AddMessage("Saving URL to '{}'".format(output_path))
        with open(output_path, 'wb') as f:
            f.write(r.read())
    else:
        arcpy.AddError("Failed to download '{}'".format(url))


def parse_json_url(url):
    """Parse and return a JSON response from a URL."""
    res = None
    r = request.urlopen(url)
    if r.code == 200:
        # urllib doesn't know bytestreams
        str_response = r.read().decode('utf-8')
        res = json.loads(str_response)
    else:
        print("Failed to download '{}'".format(url))
        sys.exit()
    return res


def release_info():
    """Get latest release version and download URL from
       the GitHub API.

    Returns:
        (download_url, tag_name) tuple.
    """
    download_url = None
    tag = None
    json_r = parse_json_url(latest_url)
    if 'assets' in json_r:
        assets = json_r['assets'][0]
        if 'browser_download_url' in assets and \
                'tag_name' in json_r:
            download_url = assets['browser_download_url']
            tag = json_r['tag_name']

    if tag is None or download_url is None:
        print("Invalid GitHub API response for URL '{}'".format(
            latest_url))

    return (download_url, tag)