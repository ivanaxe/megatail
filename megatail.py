#!/usr/bin/python

import os
import time
import yaml
import shutil

# sensor_path = "/home/uploader/nginx_access_log/access.log"
sensor_path = "/tmp/file"
data_path = "/tmp/megatail"
init_run = True
infinite_run = False

class reader:
    def __init__(self, sensor_path, last_digest=None, last_read=None):
        self.sensor_path = sensor_path
        if last_digest == None or last_read == None:
            try:
                self.load_state(data_path)
            except:
                if init_run:
                    self.last_digest = ""
                    self.last_read = 0
                else:
                    # print "error reading stored configuration"
                    exit(1)
        else:
            self.last_digest = last_digest
            self.last_read = last_read

    def save_state(self, path):
        f = open(path+"/state.tmp", "w")
        f.write(yaml.dump((self.last_digest, self.last_read)))
        f.close()
        shutil.move(path+"/state.tmp",path+"/state")

    def load_state(self, path):
        (self.last_digest, self.last_read) = yaml.load(open(path+"/state"))
        
    def continue_reading(self):

        sensor_file = open(self.sensor_path, "r")

        first_line = sensor_file.readline()
        digest = first_line
        current_line = first_line

        if digest == self.last_digest:
            for _ in range(self.last_read):
                current_line = sensor_file.readline()
        else:
            self.last_digest = digest
            self.last_read = 0
        
        while current_line:
            yield current_line
            self.last_read += 1
            self.save_state(data_path)
            current_line = sensor_file.readline()

if __name__ == "__main__":

    if not os.path.exists(data_path):
        os.mkdir(data_path)

    r = reader(sensor_path)
    for i in range(100):
        for s in r.continue_reading():
            print s.rstrip()
        
        time.sleep(1)
