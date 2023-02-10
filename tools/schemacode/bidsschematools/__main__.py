import argh
import logging
import os

from .schema import export


def cli():
    argh.dispatch_commands([export])

if __name__ == '__main__':
    main()
