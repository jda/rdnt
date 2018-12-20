# rdnt

Rapid Deployment Networks Tool

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
python rdnt network gen-device-report Jade
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
