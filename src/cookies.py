"""
A relatively simple cookies library!
"""


import sys


debug_mode = False
import sqlite3
import winreg


# This class is used to raise an exception when an invalid browser is passed to the `get_browser`
# function
class InvalidBrowserException(Exception):
    """
    Used to raise an exception when an invalid browser is passed (not ff or chrome)
    """
    pass

import os
import win32crypt


class HTTPCookies:
    def __init__(self, browser_path=None):
        # Checking if the browser_path is None, if it is, it is checking if firefox or chrome is
        # installed, if it is, it is finding the cookies sql database, if it is not, it is raising an
        # exception.
        if browser_path is None:
            # Detecting if firefox or chrome is installed.
            if 'firefox' in sys.executable.lower():
                # Finding the cookies sql database.
                for root, dirs, files in os.walk(os.path.expanduser('~')):
                    for file in files:
                        if file == 'cookies.sqlite':
                            if debug_mode:
                                print(f'browser_path set to {self.browser_path}')
                            self.browser_path = os.path.join(root, file)
            elif 'chrome' in sys.executable.lower():
                # Finding the cookies sql database.
                for root, dirs, files in os.walk(os.path.expanduser('~')):
                    for file in files:
                        if file == 'Cookies':
                            self.browser_path = os.path.join(root, file)
                            if debug_mode:
                                print(f'browser_path set to {self.browser_path}')
            else:
                raise InvalidBrowserException('Firefox or Chrome is not installed!')
        else:
            self.browser_path = browser_path
            if debug_mode:
                print(f'browser_path set to {self.browser_path}')
            self.browser_path = browser_path

    def get_cookies(self, url):
        """
        It takes the url of the website you want to get the cookies from, connects to the sqlite
        database, and then returns a dictionary of the cookies
        
        :param url: The URL of the website you want to get the cookies from
        :return: A dictionary of cookies
        """
        cookies = {}
        conn = sqlite3.connect(self.browser_path)
        cursor = conn.cursor()
        # Selecting the host_key, name, path, value, and encrypted_value from the cookies table where
        # the host_key is like the url.
        cursor.execute(f'SELECT host_key, name, path, value, encrypted_value FROM cookies WHERE host_key like "%{url}%"')
        # Iterating through the results of the query and adding them to a dictionary.
        for host_key, name, path, value, encrypted_value in cursor.fetchall():
            if encrypted_value is not None:
                value = win32crypt.CryptUnprotectData(encrypted_value)[1].decode()
            cookies[name] = value
            if debug_mode:
                print(f'cookies set to {cookies}')
        return cookies


    def set_cookie(self, url, name, value, path='/', expires=None):
        """
        It takes the url, name, value, path, and expires as parameters and updates the value of the
        cookie in the cookies table in the browser's sqlite database.
        
        :param url: The url of the website you want to set the cookie for
        :param name: The name of the cookie
        :param value: The value of the cookie
        :param path: The path of the cookie, defaults to / (optional)
        :param expires: The date the cookie will expire. This can be a datetime object or a string in
        the format 'Wdy, DD-Mon-YYYY HH:MM:SS GMT'
        """
        conn = sqlite3.connect(self.browser_path)
        cursor = conn.cursor()
        # Selecting the host_key from the cookies table where the host_key is like the url.
        cursor.execute(f'SELECT host_key FROM cookies WHERE host_key like "%{url}%"')
        host_key = cursor.fetchone()[0]
        # Updating the value of the cookie in the cookies table in the browser's sqlite database.
        cursor.execute(f'UPDATE cookies SET value = "{value}" WHERE host_key = "{host_key}" AND name = "{name}"')
        if debug_mode:
            print(f'value set to {value}')
        conn.commit()
        conn.close()


    def get_cookie(self, url, name):
        """
        It takes the url and name of the cookie as parameters and returns the value of the cookie.
        
        :param url: The url of the website you want to get the cookie from
        :param name: The name of the cookie
        :return: The value of the cookie
        """
        conn = sqlite3.connect(self.browser_path)
        cursor = conn.cursor()
        # Selecting the value and encrypted_value from the cookies table where the host_key is like
        # the url and the name is the name of the cookie.
        cursor.execute(f'SELECT value, encrypted_value FROM cookies WHERE host_key like "%{url}%" AND name = "{name}"')
        value, encrypted_value = cursor.fetchone()
        if encrypted_value is not None:
            value = win32crypt.CryptUnprotectData(encrypted_value)[1].decode()
        if debug_mode:
            print(f'value set to {value}')
        return value


    def get_cookie_unknown_url(self, name):
        """
        It takes the name of the cookie as a parameter and returns the value of the cookie.
        
        :param name: The name of the cookie
        :return: The value of the cookie
        """
        conn = sqlite3.connect(self.browser_path)
        cursor = conn.cursor()
        # Selecting the value and encrypted_value from the cookies table where the name is the name
        # of the cookie.
        cursor.execute(f'SELECT value, encrypted_value FROM cookies WHERE name = "{name}"')
        values = []
        for value, encrypted_value in cursor.fetchall():
            if encrypted_value is not None:
                value = win32crypt.CryptUnprotectData(encrypted_value)[1].decode()
            values.append(value)
            if debug_mode:
                print(f'values set to {values}')
        return values


def toggle_debug_mode():
    """
    Toggles debug mode. Debug mode tells you when a variable is set.
    """
    global debug_mode
    debug_mode = not debug_mode
