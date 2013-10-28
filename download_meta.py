"""
Download all the plazas metas for all the ids in plazas
"""

from lib.foursqure_wrapper import download_meta_data
from lib.mysql_connect import connect_to_mysql
from lib.mysql_connect import drop_table_venue_meta
from lib.mysql_connect import add_table_venue_meta
from lib.storage_interface import save_venue_meta
from lib.multithread import do_multithread_job
def do_work(paras):
    venue_id = paras[0]
    crawl_user_id = paras[1]
    meta_data = download_meta_data(venue_id)
    drop_table_venue_meta(crawl_user_id)
    add_table_venue_meta(crawl_user_id)
    save_venue_meta(meta_data, crawl_user_id)

def main():
    do_work((14,1))

#main()
