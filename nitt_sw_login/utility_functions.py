#!/usr/bin/python

from __future__ import print_function

import sys
import os
import requests
import time
import random
import logging
import json
import getpass
import platform
import errno
from string import digits
from hashlib import md5
from argparse import ArgumentParser


logging.captureWarnings(True)
base_url = 'https://192.168.20.1/'


def new_credentials():
    print()
    file_path = get_credentials_path()
    username = input(" Enter Username :- ")
    password = getpass.getpass(prompt=" Enter Password :- ")
    creds = {'USERNAME': username, 'PASSWORD':password}
    with open(file_path, 'w') as file:
        json.dump(creds, file, indent=4)
    print()
    return creds


def get_credentials_path(file_name='credentials.txt'):

    home_dir = os.path.expanduser('~')
    dir_name = 'nitt_sw_login'
    if platform.system() in ['Linux', 'Darwin']:
        dir_name = '.' + dir_name
    file_dir = os.path.join(home_dir, dir_name)
    try:
        os.mkdir(file_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise e
    file_path = os.path.join(file_dir, file_name)
    return file_path


def read_credentials():
    print("\n Reading credentials ...")
    file_path = get_credentials_path()
    if os.path.isfile(file_path):
        try:
            t = json.load(open(file_path))
        except json.decoder.JSONDecodeError:
            print(" Your credentials file seems to be corrupted.\n Re-enter your credentials ...")
            t = new_credentials()
    else:
        print(" No credentials found. Please update your credentials.")
        t = new_credentials()

    creds = {}
    creds['uName'] = t['USERNAME']
    creds['pass'] = t['PASSWORD']
    return creds


def snooze(factor):
    ONE_MINUTE = 60
    time.sleep(ONE_MINUTE * factor)


def generate_cookie():
    seed = ''.join(random.choice(digits) for _ in range(16))
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
    print(" Authenticating with NITT SonicWall ...")
    login_attempt = 6

    while login_attempt > 0:
        t = session.get(base_url + 'auth1.html') 
        t = session.post(base_url+'auth.cgi', data=payload)
        session.get(base_url + "loginStatusTop(eng).html")
        t = session.post(base_url + "usrHeartbeat.cgi", verify=False)

        if is_logged_in(t):
            print(" Logged in successfully !!  :)")
            current_time = time.strftime("%H:%M:%S  %d-%m-%Y", time.localtime())
            print(" Login time :- %s " % current_time)
            print(" (Keep this window open for a persistent connection)")
            return True
        else:
            login_attempt -= 1

    print(" Login failed !!  :( \n")
    return False


def persist(session):
    logged_in = True
    while logged_in:
        try:
            t = session.post(base_url + "usrHeartbeat.cgi", verify=False)
            logged_in = is_logged_in(t)
            rem_time = remaining_time(t)
            if rem_time <= 30:
                print("\n Session will expire soon. Logging in again ...")
                set_cookies(session)
                logged_in = login(session)
            else:
                snooze(5)
        except (requests.exceptions.ConnectionError):
            snooze(1)

    print("Seems like something went wrogn !!")
    print("You have been logged out of DELL SonicWall.")  


def setup_session():
    s = requests.Session()
    http_adapter = requests.adapters.HTTPAdapter(max_retries=6)
    https_adapter = requests.adapters.HTTPAdapter(max_retries=6)
    s.mount('http://', http_adapter)
    s.mount('https://', https_adapter)
    s.verify = False
    set_cookies(s)
    return s


def keep_alive(session):
    logged_in = True
    while logged_in:
        try:
            t = session.post(base_url + "usrHeartbeat.cgi", verify=False)
            logged_in = is_logged_in(t)
            if logged_in:
                snooze(5)
        except (requests.exceptions.ConnectionError):
            snooze(1)
    print("You have been logged out of DELL SonicWall.") 


def update_rem_time(session, rem_time):
    if rem_time <= 0:
        rem_time = 1
    payload = {'maxSessionTime': rem_time}
    t = session.post(base_url + 'userSettings.cgi', data=payload)
    session.post(base_url + "usrHeartbeat.cgi", verify=False)
