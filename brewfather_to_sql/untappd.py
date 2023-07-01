import requests

# Untappd API credentials
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
access_token = "YOUR_ACCESS_TOKEN"

# Function to retrieve beers created by your account
def get_user_beers():
    url = f"https://api.untappd.com/v4/user/beers?access_token={access_token}"
    response = requests.get(url)
    if response.status_code == 200:
        beers = response.json()["response"]["beers"]["items"]
        for beer in beers:
            beer_name = beer["beer"]["beer_name"]
            brewery_name = beer["brewery"]["brewery_name"]
            print(f"Beer Name: {beer_name}\nBrewery: {brewery_name}\n")
    else:
        print("Failed to retrieve user beers.")

# Function to create a new beer
def create_new_beer():
    beer_name = input("Enter the name of the beer: ")
    brewery_name = input("Enter the name of the brewery: ")
    beer_style = input("Enter the beer style: ")

    url = "https://api.untappd.com/v4/beer/new"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    payload = {
        "name": beer_name,
        "brewery": brewery_name,
        "style": beer_style
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("Beer created successfully!")
    else:
        print("Failed to create beer.")

# Main program
while True:
    print("--- Untappd API Menu ---")
    print("1. View user beers")
    print("2. Create new beer")
    print("3. Exit")
    choice = input("Enter your choice (1-3): ")

    if choice == "1":
        get_user_beers()
    elif choice == "2":
        create_new_beer()
    elif choice == "3":
        break
    else:
        print("Invalid choice. Please try again.")
