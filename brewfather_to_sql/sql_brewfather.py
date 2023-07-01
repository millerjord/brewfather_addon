import requests
import base64
import datetime

# Replace 'YOUR_API_KEY' with your actual Brewfather API key
userid = "U9MU3zRY3NfZh0z4Hhrh3EAp8L02"
apikey = "N9JDS34TBBrAM4FvtpFwPhzzijkJHoDQwJCko4ya0iYtslrthsc1FUkigm9tcwxf"

authkey = userid + ":" + apikey
authkey_bytes = authkey.encode('ascii')
base64_bytes = base64.b64encode(authkey_bytes)
base64_authkey = base64_bytes.decode('ascii')

# print(base64_authkey)

# api_key = 'YOUR_API_KEY'
base_url = 'https://api.brewfather.app/v2'

def get_batches(api_key):
    headers = {'Authorization': 'Basic ' + api_key}
 #   headers = {'Authorization': f'Bearer {api_key}'}
    url = f'{base_url}/batches?limit=50'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        batches = data
        return batches
    else:
        print('Error retrieving batches:', response.text)
        return []

# Replace 'YOUR_API_KEY' with your actual Brewfather API key
batches = get_batches(base64_authkey)
headers = {'Authorization': 'Basic ' + base64_authkey}

for batch in batches:
    batch_id = batch['_id']
    # Make a separate API call for each batch using the batch_id
    batch_url = f'{base_url}/batches/{batch_id}'
    batch_response = requests.get(batch_url, headers=headers)

    if batch_response.status_code == 200:
        batch_data = batch_response.json()
        # Access the desired fields from the batch_data
        batch_no = batch_data['batchNo']
        brew_date = batch_data['brewDate']
        brewer = batch_data['brewer']
        recipe_name = batch_data['recipe']['name']
        color = batch_data['recipe']['color']
        ibu = batch_data['recipe']['ibu']
        style = batch_data['recipe']['style']['name']
        measured_abv = batch_data['measuredAbv']
        brew_date_datetime = datetime.datetime.fromtimestamp(brew_date / 1000)  # Divide by 1000 to convert from milliseconds to seconds
        formatted_brew_date = brew_date_datetime.strftime('%Y-%m-%d')
        
        # Print or process the retrieved data as needed
 #       print('Batch ID:', batch_id)
 #       print('Batch No:', batch_no)
 #       print('Brew Date:', formatted_brew_date)
 #       print('Brewer:', brewer)
 #       print('Recipe Name:', recipe_name)
 #       print('Color:', color)
 #       print('ABV:', measured_abv)
 #       print('IBU:', ibu)
 #       print('Style:', style)

#        print('---')
        print('INSERT INTO beers (batchNo, batchID, Name, BrewDate, Style, IBU, EBC, ABV) VALUES (',batch_no,', "',batch_id,'","',recipe_name,'",',formatted_brew_date,',"',style,'",',ibu,',',color,',',measured_abv,')')
    else:
        print(f'Error retrieving batch {batch_id}:', batch_response.text)


