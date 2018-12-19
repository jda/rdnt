# rdnt
Rapid Deployment Networks Tool

## Usage

You should set your meraki dashboard api key & org name as 
an environment variable. You can provide them as CLI args, but
you'll likely be using the same values for the duration of your
deployment and probably don't want them showing up on your screen
so that they don't get accidentally disclosed by a errant photo.

If you are using PowerShell on Windows, set env var like this:
```
$env:MERAKI_DASHBOARD_KEY = "secret_key_here"
$env:MERAKI_DASHBOARD_ORG = "MyOrg"
```
