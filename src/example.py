import cookies
import os
import sys


def get_browser_path():
    """
    Ask the user for the path to their browser.
    """
    browser_path = input("Enter the path to your browser: ")
    if not os.path.exists(browser_path):
        print("That path does not exist.")
        sys.exit(1)
    return browser_path


def main():
    browser_path = get_browser_path()
    cookie_class = cookies.HTTPCookies(browser_path)
    cookie_class.get_cookies("http://google.com")



if __name__ == "__main__":
    main()
