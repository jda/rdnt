#!/usr/bin/env python
"""Rapid Deployment Network Tool

Helps you quickly provision ephemeral or csisis response networks.
"""

import os
import sys

from commands.device import device
from commands.network import network

import click


@click.group()
@click.option(
    "--apikey", prompt=False, default=lambda: os.environ.get("MERAKI_DASHBOARD_KEY", "")
)
@click.option(
    "--org", prompt=False, default=lambda: os.environ.get("MERAKI_DASHBOARD_ORG", "")
)
@click.pass_context
def cli(ctx, apikey, org):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below
    ctx.ensure_object(dict)

    if apikey == "":
        print("apikey is required", file=sys.stderr)
        sys.exit(1)

    ctx.obj["API_KEY"] = apikey
    ctx.obj["ORG"] = org


cli.add_command(device)
cli.add_command(network)
