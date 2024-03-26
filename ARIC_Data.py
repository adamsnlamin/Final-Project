import requests
import pandas as pd

# Define the API endpoint
url = "https://api.artic.edu/api/v1/artworks?page=1&limit=100"

# Initialize a counter for the number of pages processed
pages_processed = 0

artworks = []

while pages_processed < 200:  # Limit the loop to 200 pages
    # Make a GET request to the API
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract the JSON data from the response
        data = response.json()
        
        # Extract relevant information from the response and create a DataFrame
        for artwork in data['data']:
            artwork_info = {
                'artwork_id': artwork['id'],
                'artist_name': artwork['artist_display'],
                'title': artwork['title'],
                'exhibition_history': artwork['exhibition_history'],
                'is_on_view': artwork['is_on_view'],
                'date': artwork['date_display'],
                'category_titles': artwork['category_titles'][0] if artwork['category_titles'] else None,
                'artwork_type_title': artwork['artwork_type_title']
            }
            artworks.append(artwork_info)
        
        # Increment the page counter
        pages_processed += 1
    else:
        print("Error:", response.status_code)
        break
    
    # Check if there's a next page
    page_info = data['pagination']
    if 'next_url' not in page_info:
        break
    else:
        url = data['pagination']['next_url']
        print(url)

# Convert the list of dictionaries into a DataFrame
artist_artwork_df = pd.DataFrame(artworks)

# Save the DataFrame to a CSV file
artist_artwork_df.to_csv('artwork.csv', index=False)

# Display the DataFrame
artist_artwork_df
