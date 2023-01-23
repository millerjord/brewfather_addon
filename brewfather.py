import requests
import json
from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import Entity

class BrewfatherSensor(Entity):
    def __init__(self, api_key, brew_id):
        self._api_key = api_key
        self._brew_id = brew_id
        self._state = None

    @property
    def name(self):
        return f'Brewfather {self._brew_id}'

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return TEMP_CELSIUS

    def update(self):
        url = f'https://brewfather.net/api/v2/brew/{self._brew_id}'
        headers = {'Authorization': f'Bearer {self._api_key}'}
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        self._state = data['current_temp']


