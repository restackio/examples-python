
# Twilio Trunking

https://docs.livekit.io/sip/quickstarts/configuring-twilio-trunk/


## Add envs

```
cp .env.example .env
```

## Start python shell

```bash
uv venv && source .venv/bin/activate
```


## Install dependencies

```bash
uv sync
```

## Run setup trunk script

```bash
uv run python twilio_trunk.py
```

# Outbound

## Step 1: Create a credential list

https://console.twilio.com/us1/develop/voice/manage/cls?frameUrl=/console/voice/sip/cls


## Step 2: Associate the credential list with your SIP trunk

https://console.twilio.com/us1/develop/sip-trunking/manage/trunks?frameUrl=%2Fconsole%2Fsip-trunking%2Ftrunks%3Fx-target-region%3Dus1

Select Elastic SIP Trunking » Manage » Trunks and select the outbound trunk created in the previous steps.
Select Termination » Authentication » Credential Lists and select the credential list you just created.
Select Save.