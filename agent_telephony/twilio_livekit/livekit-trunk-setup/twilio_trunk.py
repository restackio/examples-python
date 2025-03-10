import json
import logging
import os
import re
import subprocess

from dotenv import load_dotenv
from twilio.rest import Client


def get_env_var(var_name):
    value = os.getenv(var_name)
    if value is None:
        logging.error(f"Environment variable '{var_name}' not set.")
        exit(1)
    return value


def create_livekit_trunk(client, sip_uri, trunk_name):
    domain_name = f"livekit-trunk-{os.urandom(4).hex()}.pstn.twilio.com"
    trunk = client.trunking.v1.trunks.create(
        friendly_name=trunk_name,
        domain_name=domain_name,
    )
    trunk.origination_urls.create(
        sip_url=sip_uri,
        weight=1,
        priority=1,
        enabled=True,
        friendly_name=f"{trunk_name} SIP URI",
    )
    logging.info(f"Created new {trunk_name} trunk.")
    return trunk


def create_inbound_trunk(phone_number, trunk_name):
    trunk_data = {"trunk": {"name": f"Inbound {trunk_name}", "numbers": [phone_number]}}
    with open("inbound_trunk.json", "w") as f:
        json.dump(trunk_data, f, indent=4)

    result = subprocess.run(
        ["lk", "sip", "inbound", "create", "inbound_trunk.json"],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        logging.error(f"Error executing command: {result.stderr}")
        return None

    match = re.search(r"ST_\w+", result.stdout)
    if match:
        inbound_trunk_sid = match.group(0)
        logging.info(f"Created inbound trunk with SID: {inbound_trunk_sid}")
        return inbound_trunk_sid
    logging.error("Could not find inbound trunk SID in output.")
    return None


def create_dispatch_rule(trunk_sid, trunk_name):
    dispatch_rule_data = {
        "name": f"Inbound {trunk_name} Dispatch Rule",
        "trunk_ids": [trunk_sid],
        "rule": {"dispatchRuleIndividual": {"roomPrefix": "call-"}},
    }
    with open("dispatch_rule.json", "w") as f:
        json.dump(dispatch_rule_data, f, indent=4)

    result = subprocess.run(
        ["lk", "sip", "dispatch-rule", "create", "dispatch_rule.json"],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        logging.error(f"Error executing command: {result.stderr}")
        return

    logging.info(f"Dispatch rule created: {result.stdout}")


def main():
    load_dotenv()
    logging.basicConfig(level=logging.INFO)

    account_sid = get_env_var("TWILIO_ACCOUNT_SID")
    auth_token = get_env_var("TWILIO_AUTH_TOKEN")
    phone_number = get_env_var("TWILIO_PHONE_NUMBER")
    sip_uri = get_env_var("LIVEKIT_SIP_URI")
    trunk_name = get_env_var("TRUNK_NAME")

    client = Client(account_sid, auth_token)

    existing_trunks = client.trunking.v1.trunks.list()
    livekit_trunk = next(
        (trunk for trunk in existing_trunks if trunk.friendly_name == trunk_name),
        None,
    )

    if not livekit_trunk:
        livekit_trunk = create_livekit_trunk(client, sip_uri, trunk_name)
    else:
        logging.info(f"{trunk_name} already exists. Using the existing trunk.")

    inbound_trunk_sid = create_inbound_trunk(phone_number, trunk_name)
    if inbound_trunk_sid:
        create_dispatch_rule(inbound_trunk_sid, trunk_name)


if __name__ == "__main__":
    main()
