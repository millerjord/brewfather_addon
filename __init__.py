DOMAIN = "brewfather"

import asyncio
from datetime import timedelta

async def async_setup(hass, config):
    hass.data[DOMAIN] = {}
    return True

async def async_setup_entry(hass, entry):
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )

    # start a background task to poll the Brewfather API every 60 minutes
    async def poll_brewfather():
        # get the user ID and API key from the configuration data
        userid = entry.data["userid"]
        apikey = entry.data["apikey"]

        # make API requests and update the sensor states here

    # start the background task
    interval = timedelta(minutes=60)
    hass.data[DOMAIN]["polling_task"] = hass.loop.create_task(
        asyncio.create_task(poll_brewfather(), interval=interval)
    )

    return True

async def async_unload_entry(hass, entry):
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    return True

async def poll_brewfather():
    userid = entry.data["userid"]
    apikey = entry.data["apikey"]
    url = "https://api.brewfather.app/v2/batches"
    
    authkey = userid + ":" + apikey
    authkey_bytes = authkey.encode('ascii')
    base64_bytes = base64.b64encode(authkey_bytes)
    base64_authkey = base64_bytes.decode('ascii')

    headers = {"Authorization": f"Basic {base64_authkey}"}
    params_arg = {"include": "readings", "status": "Fermenting"}


    while True:
        # make an API request to get the latest batch data
        response = await hass.async_add_executor_job(
            requests.get, url, headers=headers, params=params_arg
        )
        batch_data = response.json()

        # update the Home Assistant sensors with the latest data
        update_sensors(hass, batch_data)

        # wait for the next polling interval before making another request
        await asyncio.sleep(interval.total_seconds())


config_entry_flow.register_webhook_flow(
    DOMAIN,
    "Brewfather Webhook",
    {
        "docs_url": "https://github.com/millerjord/brewfather_addon",
    },
    BrewfatherConfigFlow,
)
