"""
    For a venue id, grab all it's meta data
"""
from instagram.client import InstagramAPI
import config
import time
import os

def parse_id_from_url(url):
    if url.find("max_tag_id")==-1:
        return -1
    print url.find("max_tag_id")
    return url[url.find("max_tag_id")+11:]

def download_tag_photos(tag_name, max_tag_id = None, client = InstagramAPI(client_id = config.instagram_client_id, client_secret = config.instagram_client_secret)):
    max_id_file = os.path.dirname(os.path.realpath(__file__))+'/max_id.txt'
    try:
        id_file = open(max_id_file, 'r').read()
        max_id = id_file.strip()
    except:
        max_id = None

    cnt = 0
    instagen , next_url= client.tag_recent_media(count=100, max_id = max_tag_id, tag_name = tag_name, max_pages=None)
    for p in instagen:
        cnt += 1
    idx = parse_id_from_url(next_url)
    if idx == -1:
        sys.stderr.write('something wrong...\n')
        return -1
    
    while True:
        instagen, next_url = client.tag_recent_media(count=100, max_id = idx, tag_name = tag_name)
        for p in instagen:
            # do you staff here
            # e.g. print link of the photo would be
            # print p.link
            # options are: (replace link with the following... e.g. e.filter)
            #'caption', 'comment_count', 'comments', 'created_time', 'filter', 'get_standard_resolution_url', 'id', 'images', 'like_count', 'likes', 'link', 'object_from_dictionary', 'tags', 'user'
            print p.link
            cnt += 1
        idx = parse_id_from_url(next_url)
        if idx==-1:return -1
        print '%d photos downloaded'%(cnt)
        f = open(max_id_file, 'w')
        f.write(idx)
        f.close()
        time.sleep(15)

if __name__ == '__main__':
    # change your hashtag here: replace 'nyc' with whatever you want
    gen = download_tag_photos('nyc') 
