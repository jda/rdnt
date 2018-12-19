#!/usr/bin/env python3

import csv
import sys
import click
from collections import OrderedDict

from typing import Dict, List

from merakihelper import MerakiHelper


@click.group()
@click.pass_context
def network(ctx):
    pass


@network.command()
@click.argument("clone_net_name")
@click.argument("new_net_name")
@click.argument("serials", nargs=-1)
@click.option("--kind", default="wireless,appliance")
@click.option("--timezone", default="America/Bogota")
@click.pass_context
def clone(ctx, clone_net_name, new_net_name, serials, kind, timezone):
    """
    clone creates a new name from a template and
    adds devices by serial to the new network
    """

    apikey = ctx.obj["API_KEY"]
    org = ctx.obj["ORG"]

    kinds = " ".join(kind.split(","))

    # TODO verify that clone net name is valid

    mh = MerakiHelper(apikey, org)
    network_id = mh.get_network_id_by_name(clone_net_name)
    print(f"cloning from network id {network_id}")
    new_net = mh.clone_net_with_devices(
        network_id, new_net_name, serials, kinds, timezone
    )
    print(f"new net info: {new_net}")


@network.command()
@click.argument("net_name")
@click.pass_context
def conform_device_names(ctx, net_name):
    """
    rename devices to follow pattern of network name - sequential device name
    """
    pass


@network.command()
@click.argument("net_name_prefix")
@click.pass_context
def gen_device_report(ctx, net_name_prefix):
    """
    generate device/inventory report for all sites that match net_name_prefix
    """

    apikey = ctx.obj["API_KEY"]
    org = ctx.obj["ORG"]

    mh = MerakiHelper(apikey, org)

    # get networks that match prefix
    matched_networks: Dict[str, Dict] = {}
    matched_network_ids: List[str] = []
    for net in mh.get_networks():
        net_name = net.get("name", "")

        if net_name.startswith(net_name_prefix):
            net_id = net["id"]
            matched_networks[net_id] = net
            matched_network_ids.append(net_id)

    # get devices in those networks
    our_devices: List[Dict] = []
    for device in mh.get_devices():
        net_id = device.get("networkId")
        if net_id in matched_network_ids:
            device["network_name"] = matched_networks[net_id].get("name")
            our_devices.append(device)

    our_devices = sorted(our_devices, key=lambda x: x["network_name"])

    # show it!
    fieldnames = OrderedDict(
        [
            ("serial", None),
            ("mac", None),
            ("model", None),
            ("network_name", None),
            ("name", None),
        ]
    )
    csv_out = csv.DictWriter(
        sys.stdout,
        delimiter=",",
        quotechar='"',
        fieldnames=fieldnames,
        extrasaction="ignore",
        quoting=csv.QUOTE_ALL,
        lineterminator="\n",
    )
    csv_out.writeheader()
    for device in our_devices:
        csv_out.writerow(device)
