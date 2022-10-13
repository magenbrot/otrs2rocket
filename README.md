# otrs2rocket

Post new OTRS tickets to Rocket.Chat (written in python).

view on Github <https://github.com/magenbrot/otrs2rocket>

## PREREQUISITES

Debian OS:

```bash
sudo apt install python3-pymysql python3-psycopg2 python3-requests python3-dotenv
```

## CLONE THE REPO

Clone the repo to a folder on your OTRS host, e.g.:

```bash
cd /opt
git clone https://github.com/magenbrot/otrs2rocket.git
```

## SETUP Rocket.Chat

Go to Rocket.Chat Administration panel. Open the Integrations menu and create a new integration "incoming webhook".

Activate the Webhook, the following information is sufficient (examples):

* Name: OTRS2Rocket
* Channel: #notifications

Remember the generated webhook URL for the next step.

## SETUP otrs2rocket

Copy .env.example to .env file, open it in an editor and setup the URLs and MySQL connection.

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
  * CMD: `/opt/otrs2rocket/otrs2rocket.py`
