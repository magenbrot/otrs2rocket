# otrs2rocket

Post new OTRS tickets to Rocket.Chat (written in python).

## PREREQUISITES

Debian OS:
```
sudo apt install python3-pymysql python3-requests
```

## CLONE THE REPO

Clone the repo to a folder on your OTRS host, e.g.:
```
cd /opt
git clone https://github.com/magenbrot/otrs2rocket.git
```

## SETUP OTRS

Goto Admin -> Generic Agent -> Add Job

Settings:
* Job name: OTRS to Rocket.Chat

* Event Based Execution:
  * Event Trigger:
  * Type: Ticket
  * Event: TicketCreate

* Select Tickets:
  * ie. Queue "Support" only

* Execute Ticket Commands:
  * CMD: `. /opt/otrs2rocket/.secrets && /opt/otrs2rocket/otrs2rocket.py`

## SETUP Rocket.Chat

Go to Rocket.Chat Administration panel. Open the Integrations menu and create a new integration "incoming webhook".

Activate the Webhook, the following information is sufficient (examples):
 * Name: OTRS2Rocket
 * Channel: #notifications

Remember the generated webhook URL for the next step.

## SETUP otrs2rocket

Copy .secrets.dist to .secrets file, open it in an editor and setup the URLs and MySQL connection.
