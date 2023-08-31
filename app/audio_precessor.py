# import requests
# from lxml import etree

# def scrape_samples(songName, artistName):
#     base_url = "https://www.whosampled.com"
#     url = f"{base_url}/{artistName}/{songName}/samples/"

#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
#     }

#     try:
#         response = requests.get(url, headers=headers)
#         if response.status_code == 200:
#             html = response.content
#             tree = etree.HTML(html)

#             # Use the provided XPath expression to find the section containing the samples
#             samples_container = tree.xpath('/html/body/div[1]/main/div[3]/div/div[1]/div[2]/section/div')

#             if samples_container:
#                 sample_details = []
#                 for sample in samples_container[0].xpath('.//div[@class="listEntry sampleEntry"]'):
#                     img_element = sample.find('.//img')
#                     name_element = sample.find('.//a[@class="trackName playIcon"]')
#                     artist_element = sample.find('.//span[@class="trackArtist"]/a')

#                     if img_element is not None and name_element is not None and artist_element is not None:
#                         domain = "https://www.whosampled.com"
#                         image_url = img_element.get('src')
#                         sample_name = name_element.text
#                         sample_artist = artist_element.text.strip()

#                         sample_details.append({"imageUrl": image_url, "sampleName": sample_name, "sampleArtist": sample_artist})
#                         print("Image URL:", domain+image_url)
#                         print("Sample Name:", sample_name)
#                         print("Sample Artist:", sample_artist)
#                         print("-------------------------------------")
#                 return sample_details
#             else:
#                 print("No samples found.")
#         else:
#             print(f"Failed to fetch page. Status Code: {response.status_code}")

#     except Exception as e:
#         print("Error fetching whosampled.com page:", e)

# # Call the function with your desired song and artist names
# scrape_samples("Ether", "Nas")


import requests
import shutil

def download_image(image_url, filename):
    try:
        response = requests.get(image_url, stream=True, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    })
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
        else:
            print(f"Failed to download image. Status Code: {response.status_code}")

    except Exception as e:
        print(f"Error downloading image: {e}")

# Example usage:
image_url = 'https://www.whosampled.com/static/images/media/track_images_100/mr3_20081229_19512953638.jpg'
download_image(image_url, 'img.png')