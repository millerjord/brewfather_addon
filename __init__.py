DOMAIN = "brewfather"

async def async_setup(hass, config):
    hass.data[DOMAIN] = {}
    return True

async def async_setup_entry(hass, entry):
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True

async def async_unload_entry(hass, entry):
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    return True

config_entry_flow.register_webhook_flow(
    DOMAIN,
    "Brewfather Webhook",
    {
        "docs_url": "https://github.com/millerjord/brewfather_addon",
    },
    BrewfatherConfigFlow,
)
