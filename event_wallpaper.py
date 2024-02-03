import os  # Operating system module for file operations
import ctypes  # Windows-specific module for system operations
import requests  # HTTP requests library
import pandas as pd  # Data manipulation library
import datetime  # Module for working with dates and times

class EventWallpaper:
    def __init__(self, csv_file_path, unsplash_client_id):
        """
        Initialize the EventWallpaper class with CSV file path and Unsplash API client ID.
        """
        self.csv_file_path = csv_file_path
        self.unsplash_client_id = unsplash_client_id

    def read_events_from_csv(self):
        """
        Read events from CSV file and store them in a DataFrame.
        """
        # Read CSV file into DataFrame
        self.events_df = pd.read_csv(self.csv_file_path)
        self.events_df.set_index('Date', inplace=True)

    def get_today_event(self):
        """
        Get today's event from the DataFrame.
        """
        today_date = str(datetime.date.today())
        today_event = self.events_df.get(today_date, "No events for today")
        return today_event.replace(' Day', '')

    def search_image_on_unsplash(self, query):
        """
        Search for an image related to the event query on Unsplash.
        """
        # Construct the URL for the Unsplash API
        url = f'https://api.unsplash.com/search/photos?query={query}&client_id={self.unsplash_client_id}'

        # Fetch data from the Unsplash API
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                return data['results'][0]['urls']['regular']
            else:
                return None
        else:
            return None

    def download_image(self, image_url, file_name):
        """
        Download the image from the given URL and save it to the file system.
        """
        img_response = requests.get(image_url)
        if img_response.status_code == 200:
            with open(file_name, 'wb') as file:
                file.write(img_response.content)
            return True
        else:
            return False

    def set_wallpaper(self, file_path):
        """
        Set the downloaded image as the desktop wallpaper.
        """
        ctypes.windll.user32.SystemParametersInfoW(20, 0, file_path, 0)

    def run(self):
        """
        Main method to orchestrate the process of fetching events, searching for images, downloading images, and setting wallpaper.
        """
        self.read_events_from_csv()
        today_event = self.get_today_event()
        query = today_event.replace(' ', '-')
        image_url = self.search_image_on_unsplash(query)
        if image_url:
            file_name = f"{query}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
            file_path = os.path.join(os.getcwd(), file_name)
            if self.download_image(image_url, file_name):
                self.set_wallpaper(file_path)
                print("Wallpaper set successfully!")
            else:
                print("Failed to download image.")
        else:
            print("No images found for the query.")

# Main function
def main():
    """
    Main function to prompt user for CSV file path and Unsplash API client ID, and execute the EventWallpaper class.
    """
    csv_file_path = input("Enter the path of the CSV file containing the events: ")
    unsplash_client_id = input("Enter your Unsplash API client ID: ")
    
    event_wallpaper = EventWallpaper(csv_file_path, unsplash_client_id)
    event_wallpaper.run()

if __name__ == "__main__":
    main()
