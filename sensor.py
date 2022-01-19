async def async_setup_platform(
    hass: HomeAssistantType,
    config: ConfigType,
    async_add_entities: Callable,
    discovery_info: Optional[DiscoveryInfoType] = None,
) -> None:
    """Set up the sensor platform."""
    session = async_get_clientsession(hass)
    sensors = [GitHubRepoSensor(github, repo) for repo in config[CONF_REPOS]]
    async_add_entities(sensors, update_before_add=True)
