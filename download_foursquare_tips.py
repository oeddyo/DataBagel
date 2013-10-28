"""
Download all the plazas metas for all the ids in plazas
"""


from lib.foursqure_wrapper import download_venue_tips
from lib.mysql_connect import connect_to_mysql
from lib.mysql_connect import drop_table_venue_tips
from lib.mysql_connect import add_table_venue_tips
from lib.storage_interface import save_venue_tip
from lib.multithread import do_multithread_job

#from venue_meta import VenueTipsCrawler

def do_work(paras):
    venue_id = paras[0]
    crawl_user_id = paras[1]
    drop_table_venue_tips(crawl_user_id)
    add_table_venue_tips(crawl_user_id)
    tips_gen = download_venue_tips(venue_id)
    for p in tips_gen:
        save_venue_tip(p, venue_id, crawl_user_id)


def main():
    do_work((14,1))

main()
