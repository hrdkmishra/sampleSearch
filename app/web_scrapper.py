import requests
from lxml import etree

def extract_and_change_case(song_name, artist_name):
    # Extract song name and remove text within parentheses (if present)
    if '(' in song_name:
        start_index = song_name.find('(')
        end_index = song_name.find(')')
        # Check if there is a space before the opening parenthesis
        if start_index > 0 and song_name[start_index - 1] == ' ':
            song_name = song_name[:start_index - 1] + song_name[end_index + 1:]
        else:
            song_name = song_name[:start_index] + song_name[end_index + 1:]

    # Split the artist_name by the '&' character and take the first part
    artist_parts = artist_name.split('&')
    artist_name = artist_parts[0].strip()

    # Remove any trailing hyphens and replace spaces with dashes, then convert to lowercase
    song_name = song_name.replace(" ", "-")
    artist_name = artist_name.replace(" ", "-")
    return song_name, artist_name

def scrape_samples(songName, artistName):
    base_url = "https://www.whosampled.com"
    sample_url = f"{base_url}/{artistName}/{songName}/samples/"
    track_url = f"{base_url}/{artistName}/{songName}/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    try:
        response = requests.get(sample_url, headers=headers, allow_redirects=True)
        print(f"Response sample URL: {sample_url}")
        print(f"Response sample URL: {response.url}")
        
        if response.status_code == 404 or '<p>The page you requested cannot be found</p>' in response.text:
            response = requests.get(track_url, headers=headers, allow_redirects=True)
            print(f"Response track URL: {response.url}")
            print(f"Track URL: {track_url}")

        if response.status_code == 200:
            html = response.content
            tree = etree.HTML(html)

            # Check the scenario based on the response URL (ignoring the protocol)
            if response.url.lower() == sample_url.lower():
                samples_container = tree.xpath('/html/body/div[1]/main/div[3]/div/div[1]/div[2]/section/div')
            elif response.url.lower() == track_url.lower():
                samples_container = tree.xpath('/html/body/div/main/div[3]/div/div[1]/section[3]/div')
            else:
                print("URL doesn't exist")
                return []
                
            if samples_container:
                sample_details = []
                for sample in samples_container[0].xpath('.//div[@class="listEntry sampleEntry"]'):
                    img_element = sample.find('.//img')
                    name_element = sample.find('.//a[@class="trackName playIcon"]')
                    artist_element = sample.find('.//span[@class="trackArtist"]/a')

                    if img_element is not None and name_element is not None and artist_element is not None:
                        image_url = img_element.get('src')
                        sample_name = name_element.text
                        sample_artist = artist_element.text.strip()

                        sample_details.append({"image_url": base_url + image_url, "sample_name": sample_name, "sample_artist": sample_artist})
                return sample_details
            else:
                print("No samples found.")
                return []
        else:
            print(f"Failed to fetch page. Status Code: {response.status_code}")
            return []

    except Exception as e:
        print("Error fetching whosampled.com page:", e)
        return []


# # Test with an example
# song_name = "N.Y.-State-of-Mind"
# artist_name = "Nas"
# sample_details = scrape_samples(song_name, artist_name)
# print(sample_details)