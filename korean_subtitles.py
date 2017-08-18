#!/usr/bin/env python
# -*- coding: utf-8
""" A script to check whether shows listed on SBS have Korean subtitles.

"""

import argparse
import logging
import re

import bs4
import requests

# There are 10 pages with listings.
SBS_LISTING_URL = (
    "http://vod.sbs.co.kr/tv/tv_list.jsp"
    "?section=drama"
    "&index=ALL"
    "&order=DATE"
    "&listtype=img"
    "&cPage={pagenum}"
)
# Individual video page URL.
SBS_VIDEO_URL = (
    "http://vod.sbs.co.kr/sw13/vod/player/vod_player.jsp?vodid={vodid}"
)
# This is shown when there are no subtitles.
NO_SUBTITLES_AVAILABLE = u"해당 영상은 자막이 제공 되지 않습니다"

logger = logging.getLogger(__name__)


def get_listing(pagenum):
    resp = requests.get(SBS_LISTING_URL.format(pagenum=pagenum))
    resp.raise_for_status()
    pagetext = resp.text

    soup = bs4.BeautifulSoup(pagetext)
    # The listings are in a <div class="thum_list">. Each listing is an <a
    # href="oclick=goDetail('$VODID')><strong>$TITLE</strong>...</a>
    thum_list = soup.find('div', attrs={'class': 'thum_list'})
    shows = []
    for link in thum_list.find_all('a'):
        onclick = link['onclick']
        vodid = re.match("goDetail\('(V\d+)'\)", onclick).group(1)
        name = link.find('strong').text
        shows.append((name, vodid))
    return shows


def has_subtitles(vodid, text):
    soup = bs4.BeautifulSoup(text)
    # The indicator for subtitles is in a nested <div> block.
    indicator = soup.find('div', attrs={'class': 'infor2'})
    indicator_text = indicator.find('div').text.strip()

    logger.debug(u'Subtitle block for vodid {0}: {1}'.format(
        vodid, indicator))
    return not indicator_text.startswith(NO_SUBTITLES_AVAILABLE)


def check_one(vodid):
    logger.debug('Fetching vodid {0}'.format(vodid))
    resp = requests.get(SBS_VIDEO_URL.format(vodid=vodid))
    resp.raise_for_status()
    return has_subtitles(vodid, resp.text)


def main():
    parser = argparse.ArgumentParser(
        description="Check availability of Korean drama subtitles on SBS."
    )
    parser.add_argument('-s', '--only-subtitles', action='store_true',
                        help='Show only shows with subtitles.')
    parser.add_argument(
        'pagenum', type=int, nargs='?',
        help=('Listings page to crawl. If no page is specified, '
              'pages 1 through 10 are crawled.')
    )
    args = parser.parse_args()
    show_all = not args.only_subtitles

    if args.pagenum is None:
        pagenums = range(1, 11)
    else:
        pagenums = [args.pagenum]

    for pagenum in pagenums:
        shows = get_listing(pagenum)
        for name, vodid in shows:
            has_subtitles = check_one(vodid)
            if show_all or has_subtitles:
                print u'\N{CHECK MARK}' if has_subtitles else u'\N{BALLOT X}',
                print u'{} {}'.format(vodid, name)


if __name__ == '__main__':
    main()
