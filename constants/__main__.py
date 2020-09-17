from entry_managers import run
import sys


if __name__ == '__main__':
    # check if a sys arguement is present
    try:
        run.main(sys.argv[1], sys.argv[2:])
    except IndexError:
        run.main()
