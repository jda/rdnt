#!/usr/bin/env python

import functools

from typing import List

from meraki import meraki


class DeviceNotFound(Exception):
    pass


class NetworkNotFound(Exception):
    pass


class MerakiHelper:
    apikey = ""
    org = ""
    org_id = 0

    def __init__(self, apikey, org):
        self.apikey = apikey
        self.org = org

    def search_networks_for_device(self, serial):
        """
        searches all visible networks for device and returns device info if found
        """
        serial = serial.upper()

        # TODO refactor this?

        devices = self.get_devices()
        # get devices in network
        for device in devices:
            if device["serial"].upper() == serial:
                return device

        return None

    def remove_device_from_network(self, serial: str):
        """
        given a device serial number, remove from network
        """
        device = self.search_networks_for_device(serial)
        if not device:
            raise DeviceNotFound

        network_id = device["networkId"]
        if network_id is not None:
            meraki.removedevfromnet(self.apikey, network_id, serial)

    def move_device_to_network(self, serial: str, net_id: str):
        """
        move device from whatever network it is in to new network
        """
        pass

    def clone_net_with_devices(
        self, curr_net_id: str, new_net_name: str, devs: List[str], kind, timezone
    ):
        """
        create a new network by cloning network and adding/moving devices to it
        """

        org_id = self.get_my_org_id()
        res = meraki.addnetwork(
            self.apikey, org_id, new_net_name, kind, "", timezone, cloneid=curr_net_id
        )

        try:
            net_id = res.get("id", None)
        except AttributeError:
            # because error returns a list...
            raise NetworkNotFound(res[0])

        if not net_id:
            raise NetworkNotFound()
        for dev in devs:
            print(
                f"adding device {dev} to network {new_net_name} and removing from old network"
            )
            self.remove_device_from_network(dev)
            devaddstat = meraki.adddevtonet(self.apikey, net_id, dev)
            print(devaddstat)

        return res

    @functools.lru_cache(maxsize=None)
    def get_devices(self):
        """
        wrap get org inventory in lru cache
        """

        org_id = self.get_my_org_id()
        devices = meraki.getorginventory(self.apikey, org_id, suppressprint=True)
        return devices

    @functools.lru_cache(maxsize=None)
    def get_network_devices(self, net_id: str):
        """
        wrap getnetworkdevices with lru
        """

        devices = meraki.getnetworkdevices(self.apikey, net_id, suppressprint=True)
        return devices

    @functools.lru_cache(maxsize=None)
    def get_networks(self):
        """
        wrap getnetworklist with lru
        """

        org_id = self.get_my_org_id()

        networks = meraki.getnetworklist(self.apikey, org_id, suppressprint=True)
        return networks

    @functools.lru_cache(maxsize=None)
    def get_network_id_by_name(self, network_name: str) -> str:
        """
        given a network name, return network id or throw exception
        """

        networks = self.get_networks()
        for network in networks:
            if network["name"] == network_name:
                return network["id"]
        return ""

    def get_my_org_id(self) -> int:
        """
        returns our org ID, if we know it, and looks it up if we don't
        """

        if self.org_id == 0:
            orgs = meraki.myorgaccess(self.apikey, suppressprint=True)
            for org in orgs:
                if org["name"] == self.org:
                    self.org_id = org["id"]
                    break

        return self.org_id
