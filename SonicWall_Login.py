#!/usr/bin/python

from __future__ import print_function

import requests
import time
import random
import logging
import json
from string import digits
from hashlib import md5

logging.captureWarnings(True)
base_url = 'https://192.168.20.1/'


def read_credentials(file_path='credentials.txt'):
    print("\n Reading credentials ...")
    file = open(file_path, 'r')
    t = json.load(file)
    creds = {}
    creds['uName'] = t['USERNAME']
    creds['pass'] = t['PASSWORD']
    file.close()
    return creds

def snooze(factor):
    ONE_MINUTE = 60
    try:
        time.sleep(ONE_MINUTE * factor)
    except KeyboardInterrupt:
        print("\n Exiting !! \n")
        exit()

def generate_cookie():
    seed = ''.join(random.choice(digits) for _ in range(10))
    value = md5(seed.encode()).hexdigest()
    return value

def is_logged_in(response):
    if "refresh=true" in response.text:
        return False
    return True

def remaining_time(response):
    time = 0
    pos = response.text.find("remTime=")
    if pos != -1:
        time = response.text[pos+8:pos+11]
        time = time.split(';')[0]
        try:
            time = int(time)
        except ValueError:
            time = 0
    return time

def set_cookies(session):
    domain = '192.168.20.1'
    session.cookies.set(name='SessId', value=generate_cookie().upper(), domain=domain)
    session.cookies.set(name='PageSeed', value=generate_cookie(), domain=domain)

def login(session):
    payload = read_credentials()
    print(" Authenticating with NITT SonicWall .", end='')
    t = session.get(base_url + 'auth1.html') 
    print(".", end='')
    t = session.post(base_url+'auth.cgi', data=payload)
    print(".", end='')
    session.get(base_url + "loginStatusTop(eng).html")
    print(".", end='')
    t = session.post(base_url + "usrHeartbeat.cgi", verify=False)
    print(".", end='\n')

    if is_logged_in(t):
        print(" Logged in successfully !!  :D")
        current_time = time.strftime("%H:%M:%S  %d-%m-%Y", time.localtime())
        print(" Login time :- %s \n" % current_time)
        return True
    else:
        print(" Login failed !!  :'( \n")
        return False

def persist(session):
    logged_in = True
    while logged_in:
        try:
            t = session.post(base_url + "usrHeartbeat.cgi", verify=False)
            logged_in = is_logged_in(t)
            rem_time = remaining_time(t)
            if rem_time <= 25:
                print("\n Session will expire soon. Logging in again ...")
                set_cookies(session)
                logged_in = login(session)
            else:
                snooze(10)
        except (requests.exceptions.ConnectionError):
            snooze(1)
    print(" You have been logged out of DELL SonicWall !!")  


def setup_session():
    s = requests.Session()
    s.verify = False
    set_cookies(s)
    return s


session = setup_session()
if login(session):
    persist(session)

print(" Try logging in again !!\n")
