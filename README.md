# Rapid Deployment Network Tool (rdnt)

Helper utils for managing Meraki networks

## What can it do?

### Clone network and assign devices

Given a template network, clone it into a new network and assign gear so you are ready to deploy.

Run `rdnt network clone "Jade Home Lab" "Jade New Lab" QXXN-QXXL-WXX4` to create new network `Jade New Lab` with one device assigned. You can provide multiple devices so you can build the network with a single command.

### Unassign device from a network

Devices may not be unassigned from networks following 
previous deployments, so it's helpful to be able to quickly 
ensure that they are unassigned and ready to be added to a new network.

Run `rdnt device unassign QXXD-CXXZ-7XX8` to unassign device from any network in your org. 
Multiple serial numbers are permitted.

### Show inventory for devices in network

`rdnt network gen-device-report` to show all devices

`rdnt network gen-device-report Net` to show devices 
in network with name starting with "Net"


## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
python3 rdnt network gen-device-report Jade
"serial","mac","model","network_name","name"
"QXXD-CXXZ-7XX8","00:18:0a:xx:xx:xx","MR18","Jade Home Lab",""

```

## Build standalone

```bash
pip install pyinstaller
pyinstaller rdnt
pyinstaller --onefile rdnt/__main__.py -p rdnt -n rdnt
```

## Usage

You should set your meraki dashboard api key & org name as 
an environment variable. You can provide them as CLI args, but
you'll likely be using the same values for the duration of your
deployment and probably don't want them showing up on your screen
so that they don't get accidentally disclosed by a errant photo.

If you are using PowerShell on Windows, set env var like this:

```PowerShell
$env:MERAKI_DASHBOARD_KEY = "secret_key_here"
$env:MERAKI_DASHBOARD_ORG = "MyOrg"
```

On Linux:

```bash
 export MERAKI_DASHBOARD_KEY=api_key_goes_here
 export MERAKI_DASHBOARD_ORG=Jade
```
