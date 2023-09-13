import pandas as pd
import requests

# The URL containing the table
url = "https://www.gamergeeks.net/apps/minecraft/list-of/colored-blocks"

# Spoof the User-Agent to act like a web browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Fetch the page content
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Read the table into a pandas DataFrame
    tables = pd.read_html(response.text)

    # Assuming the first table is the one you want
    df = tables[0]

    # Save to CSV
    df.to_csv("minecraft_blocks_color.csv", index=False)
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
