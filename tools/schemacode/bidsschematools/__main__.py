import argh

from .schema import export


def cli():
    argh.dispatch_commands([export])
