#!/usr/bin/python

import sys
from argparse import ArgumentParser
from nitt_sw_login import (setup_session, login, persist, update_rem_time,
                           keep_alive, logout, new_credentials)


def main():
	arg_parser = ArgumentParser()
	arg_parser.add_argument('--reset-credentials', help='Reset your credentials', action='store_true')
	arg_parser.add_argument('--login-time', help='Limit your logged in session time (in minutes)', type=int, default=0)
	args = arg_parser.parse_args()

	if args.reset_credentials:
	    print("\n Enter your new credentials ...")
	    new_credentials()

	if (args.login_time < 0 and args.login_time > 180):
	    print(" Invalid login time limit. Ignoring.")
	    args.login_time = 0

	session = setup_session()
	if login(session):
	    try:
	        if args.login_time:
	            update_rem_time(session, args.login_time)
	            keep_alive(session)
	        else:
	            persist(session)
	    except KeyboardInterrupt:
	        logout(session)
	else:
	    print("\n\n Unable to login into DELL SonicWall !!")
        print(" 1) Please try again.")
	    print(" 2) Make sure that your Username and Password are correct.")
	    print("    To update your credentials, execute \"nitt-sw-login --reset-credentials\" ")
	    print("\n")

if __name__ == '__main__':
	main()
