"""
Download all the plazas metas for all the ids in plazas
"""

from lib.instagram_wrapper import download_instagram_photos
from lib.mysql_connect import connect_to_mysql
from lib.mysql_connect import add_table_venue_photo_instagram
from lib.mysql_connect import drop_table_venue_photo_instagram

from lib.storage_interface import save_photo_instagram
from lib.multithread import do_multithread_job
import time

def do_work(para):
    venue_id = para[0]
    crawl_user_id = para[1]
    drop_table_venue_photo_instagram(crawl_user_id)
    add_table_venue_photo_instagram(crawl_user_id)
    photos_gen = download_instagram_photos(venue_id, time.time()-24*3600*30, time.time()) 
    for p in photos_gen:
        (data, venue_id, instagram_id) = p
        save_photo_instagram(data, venue_id, instagram_id, crawl_user_id)

def main():

    already_in = set()
    sql = """ select distinct(foursquare_venue_id) as id from plazas_instaphoto """
    cursor = connect_to_mysql()
    cursor.execute(sql)
    for r in cursor.fetchall():
        already_in.add( r['id'] )

    sql = "select id from plazas_nyc"
    cursor = connect_to_mysql()
    cursor.execute(sql)
    
    ids = []
    for r in cursor.fetchall():
        #if r['id'] not in already_in:
        ids.append(r['id'])
    do_multithread_job(do_work, ids, 5, './log/download_instagram.log')
    print ids

#main()
