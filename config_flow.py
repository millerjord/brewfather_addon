class BrewfatherConfigFlow(config_entries.ConfigFlow, domain="brewfather"):
    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required("userid"): str,
                    vol.Required("apikey"): str,
                }),
                errors={},
            )

        return self.async_create_entry(title="Brewfather", data=user_input)
