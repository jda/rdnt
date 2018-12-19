#!/usr/bin/env python3

import sys
import click

from merakihelper import MerakiHelper


@click.group()
@click.pass_context
def device(ctx):
    pass


@device.command()
@click.argument("serials", nargs=-1)
@click.pass_context
def find(ctx, serials):
    apikey = ctx.obj["API_KEY"]
    org = ctx.obj["ORG"]

    if len(serials) == 0:
        print("serial args required", file=sys.stderr)
        sys.exit(1)

    mh = MerakiHelper(apikey, org)
    for serial in serials:
        device = mh.search_networks_for_device(serial)
        if device:
            print(device)


@device.command()
@click.argument("serials", nargs=-1)
@click.pass_context
def unassign(ctx, serials):
    apikey = ctx.obj["API_KEY"]
    org = ctx.obj["ORG"]

    if len(serials) == 0:
        print("serial args required", file=sys.stderr)
        sys.exit(1)

    mh = MerakiHelper(apikey, org)
    for serial in serials:
        mh.remove_device_from_network(serial.upper())
