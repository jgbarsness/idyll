from peck.peck import peck
import sys


'''
__main__ is pulled out into the parent directory
to allow for consistent import format in peck.
run this script as an entry point during development,
put note that peck.driver() is called directly when
peck is installed from pip
'''
if __name__ == '__main__':
    peck.peck.driver()
