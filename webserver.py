#!/usr/bin/python
# -*- coding: utf8 -*-
from venue_search import VenueSearch

import cherrypy
import foursquare
import config
import json
import Queue
from job import Job
import threading
from threading import Thread
import time
import os

class Root:
    def __init__(self):
        self.jobs = {}
        self.next_job_id = 0
        self.downloading_lock = threading.Event()
        t = Thread(target = self.infinit_consume)
        t.setDaemon(True)
        t.start()
        #Need to clear the data folder each time lauch the server
        cmd = "cd /db/www/places-crawl/data/ ; rm /db/www/places-crawl/data/*.csv;"
        os.popen(cmd)
    def infinit_consume(self):
        while True:
            print 'in infinite loop, try to consume'
            self.consume()
            time.sleep(5)
    def return_none(self):
        return None
    return_none.exposed = True
    
    def search_venue(self, **params):
        """The user would search venue and then the results show on front-end. After that, the user would choose which venues to fetch"""
        if 'near' not in params and ( 'lon' not in params or 'lat' not in params):
            raise cherrypy.HTTPError(404);
        _search = VenueSearch()
        _res = _search.do_search(params)
        return json.dumps(_res)
    search_venue.exposed = True
    
    def consume(self):
        print 'Try to consuming'
        if self.downloading_lock.isSet():
            print 'Busy, next time, and I quit'
        for job_id in sorted(self.jobs.keys()):
            if self.jobs[job_id].status=='Wating' and not self.downloading_lock.isSet():
                print 'free and now I could process ', job_id
                self.downloading_lock.set()
                job = self.jobs[job_id]
                t = Thread(target = job.submit, args=(self.downloading_lock,))
                t.start()
            else:
                print 'OK I do not know'
    def submit_job(self, ids_string):
        if type(ids_string) is not unicode:
            raise cherrypy.HTTPError(404);
        ids = ids_string.split(',')
        ids = [str(id) for id in ids]
        job = Job(ids, self.next_job_id ) 
        self.jobs[self.next_job_id] = job
        #add_table_venue_meta( self.next_job_id )
        self.next_job_id += 1
        return 'job submitted' 
    submit_job.exposed = True

    def get_jobs_status(self):
        reports = []
        for k in self.jobs.keys():
            reports.append(self.jobs[k].report())
        return json.dumps(reports)
    get_jobs_status.exposed = True
    
    def query_job(self, id):
        reports = []
        for k in self.jobs.keys():
            if str(k)==str(id):
                return json.dumps(self.jobs[k].report())
    query_job.exposed = True
    def download_results(self, job_id):
        try:
            job_id = int(job_id)
        except:
            raise cherrypy.HTTPError(404);
        if job_id not in self.jobs.keys():
            raise cherrypy.HTTPError(404);
        to_download_venue_ids = self.jobs[job_id].venue_ids
        return "http://fake_url_for_you_to_download.url"

        #return json.dumps(to_download_venue_ids)
    download_results.exposed = True

global_conf = {
        'global':{'server.environment': 'production',
            'engine.autoreload_on': True,
            'engine.autoreload_frequency':5,
            'server.socket_host': '0.0.0.0',
            'server.socket_port':8080,
            }
        }

cherrypy.config.update(global_conf)
cherrypy.quickstart(Root(), '/', global_conf)
