import requests
import json
import base64
from datetime import datetime

from homeassistant.const import HTTP_NOT_FOUND, HTTP_BAD_REQUEST
from homeassistant.core import callback
from homeassistant.components import http
from homeassistant.components.http.data_validator import RequestDataValidator
from homeassistant.helpers import intent
import homeassistant.helpers.config_validation as cv
from homeassistant.util.json import load_json, save_json
from homeassistant.components import websocket_api
from homeassistant.const import (CONF_PASSWORD, CONF_USERNAME)


DOMAIN = "brewfather"


async def async_setup(hass, config):
    hass.states.async_set("brewfather.brewer", "Rune")

    # Return boolean to indicate that initialization was successful.
    return True
