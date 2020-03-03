'''
define all functions here that you want to run on maintenance start emails.
all functions are called with a copy of the email object and the maintenance
row.
Once a function is defined, add it to the FUNCS list. for example:

def custom_function(email, maintenance):
    subject = email['Subject']
    maint_id = maintenance.provider_maintenance_id
    to = email['To']
    return f'the maintenance {maint_id} was sent to {to} with subject {subject}'

FUNCS = [custom_function]

'''
from flask import current_app
from app import db, scheduler
import requests
import json


def post_to_slack(email, maintenance, **kwargs):
    url = current_app.config['SLACK_WEBHOOK_URL']
    channel = current_app.config['SLACK_CHANNEL']
    janitor_url = current_app.config['JANITOR_URL']
    if not (url and channel):
        return
    if janitor_url:
        text = f'Maintenance <{janitor_url}/maintenances/{maintenance.id}|{maintenance.provider_maintenance_id}> has STARTED!\n'
    else:
        text = f'Maintenance {maintenance.provider_maintenance_id} has STARTED!\n'
    text += f'*Location*: {maintenance.location}\n'
    text += f'*Start*: {maintenance.start}, *End*: {maintenance.end} (*Timezone*: {maintenance.timezone})\n'
    username = 'janitor'
    if not channel.startswith('#'):
        channel = '#' + channel

    data_dict = {'channel': channel, 'text': text, 'username': username}
    #'icon_url' : icon_url}

    js = json.dumps(data_dict)

    requests.post(url, data=js, headers={'Content-Type': 'application/json'})


def run_traffic_drain_cmd(email, maintenance, **kwargs):
    # salt execution module or ansible playbook here
    pass


FUNCS = [post_to_slack, run_traffic_drain_cmd]
