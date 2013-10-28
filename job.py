from crawl import VenueMetaCrawler
from venue_meta import VenuePhotoCrawlerFoursquare
from threading import Thread
from time import sleep
from lib.mysql_connect import connect_to_mysql

from download_instagram import do_work as instagram_do_work
from download_meta import do_work as foursquare_do_work
from download_foursquare_tips import do_work as foursquare_tips_do_work
from download_foursquare_photos import do_work as foursquare_photos_do_work
from lib.multithread import do_multithread_job


class Job():
    def __init__(self, venue_ids, job_id):
        if type(venue_ids) is not list:
            raise TypeError
        self.status = "Wating"
        self.venue_count = 0
        self.venue_ids = venue_ids
        self.job_id = job_id 
    def submit(self, downloading_locker):
        paras = []
        for id in self.venue_ids:
            paras.append( (id, self.job_id) )
        do_multithread_job(instagram_do_work, paras, 10, './log/log_'+str(self.job_id)+'insta.txt')
        do_multithread_job(foursquare_do_work,paras, 10,'./log/log_'+str(self.job_id)+'_meta.txt')
        do_multithread_job(foursquare_tips_do_work, paras, 10, './log/log_'+str(self.job_id)+'_tips.txt')
        do_multithread_job(foursquare_photos_do_work, paras, 10, './log/log_'+str(self.job_id)+'_photos.txt')

        self.status = 'Finished'
        downloading_locker.clear() 
        #should export the csv file here
        meta_file_name = "metadata_user_"+str(self.job_id)+".csv"
        insta_file_name = "instagram_user_"+str(self.job_id)+".csv"
        tips_file_name = "tips_user_"+str(self.job_id)+".csv"
        foursquare_photo_file_name = "foursquare_photo_user_"+str(self.job_id)+".csv"
        sql = "SELECT * from venue_meta"+str(self.job_id)+"""
        INTO OUTFILE '/db/www/places-crawl/data/"""+meta_file_name+"""'
        FIELDS TERMINATED BY ','ENCLOSED BY '"'LINES TERMINATED BY '\n'
        """
        cursor = connect_to_mysql()
        try:
            cursor.execute(sql)
        except Exception as e:
            print 'OUTPUT TO DB FOLDER ERROR'

        sql = "SELECT * from venue_photo_instagram"+str(self.job_id)+"""
        INTO OUTFILE '/db/www/places-crawl/data/"""+insta_file_name+"""'
        FIELDS TERMINATED BY ','ENCLOSED BY '"'LINES TERMINATED BY '\n'
        """
        try:
            cursor = connect_to_mysql()
            cursor.execute(sql)
        except Exception as e:
            print "OUTPUT TO INSTAGRAM FOLDER ERROR"
        sql = "SELECT * from venue_tips"+str(self.job_id)+"""
        INTO OUTFILE '/db/www/places-crawl/data/"""+tips_file_name+"""'
        FIELDS TERMINATED BY ','ENCLOSED BY '"'LINES TERMINATED BY '\n'
        """
        try:
            cursor = connect_to_mysql()
            cursor.execute(sql)
        except Exception as e:
            print "OUTPUT TO FOURSQUARE_TIPS FOLDER ERROR"
        sql = "SELECT * from venue_photo_4sq"+str(self.job_id)+"""
        INTO OUTFILE '/db/www/places-crawl/data/"""+foursquare_photo_file_name+"""'
        FIELDS TERMINATED BY ','ENCLOSED BY '"'LINES TERMINATED BY '\n'
        """
        try:
            cursor = connect_to_mysql()
            cursor.execute(sql)
        except Exception as e:
            print "OUTPUT TO FOURSQUARE_PHOTO FOLDER ERROR"
        return "job done"
     
    def report(self):
        return {'job_id':self.job_id, 'status':self.status, 'venue_count':self.venue_count, 'instagram_url':'instagram_user_'+str(self.job_id)+".csv", 'foursquare_meta_url':'metadata_user_'+str(self.job_id)+'.csv'}
