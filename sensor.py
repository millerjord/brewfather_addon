# custom_components/brewfather_addon/sensor.py

import requests
import json
import base64
from datetime import datetime
import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_NAME,
    CONF_UNIT_OF_MEASUREMENT,
    CONF_DEVICE_CLASS
)
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "Brewfather Sensor"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_UNIT_OF_MEASUREMENT): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_DEVICE_CLASS): cv.string,
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Brewfather sensor."""
    unit_of_measurement = config[CONF_UNIT_OF_MEASUREMENT]
    name = config[CONF_NAME]
    device_class = config.get(CONF_DEVICE_CLASS)

    userid = hass.data[DOMAIN]["userid"]
    apikey = hass.data[DOMAIN]["apikey"]
    url = 'https://api.brewfather.app/v2/batches/'
    readings = '/readings/last'
    params_arg = {'include': 'readings', 'status':'Fermenting'}

    authkey = userid + ":" + apikey
    authkey_bytes = authkey.encode('ascii')
    base64_bytes = base64.b64encode(authkey_bytes)
    base64_authkey = base64_bytes.decode('ascii')

    headers = {'Authorization': 'Basic ' + base64_authkey}

    def get_readings(batch_id):
        data_request = requests.get(url+batch_id+readings, headers=headers)
        batch_values = json.loads(data_request.text)
        sg = batch_values['sg']
        temp = batch_values['temp']
        timestamp = datetime.fromtimestamp(batch_values['time']/1000.0)
        return sg, temp, timestamp

    r = requests.get(url, headers=headers, params=params_arg)

    batch_json = json.loads(r.text)

    entities = []

    for item in batch_json:
        batch_id = item['_id']
        batch_no = item['batchNo']
        beer_name = item['recipe']['name']
        brewdate = datetime.fromtimestamp(item['brewDate']/1000).date()
        vitals = get_readings(batch_id)

        sensor_name = f"{name}_{batch_id}"

        entity = BrewfatherSensor(
            sensor_name, unit_of_measurement, device_class, batch_no, beer_name, brewdate, vitals[1], vitals[2]
        )

        entities.append(entity)

    add_entities(entities)


class BrewfatherSensor(Entity):

    def __init__(self, name, unit_of_measurement, device_class, batch_no, beer_name, brewdate, temp, timestamp):
        self._name = name
       
