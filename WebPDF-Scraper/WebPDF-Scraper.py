import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote

# Function to download PDF files
def download_pdf_files(url, download_folder="pdf_downloads"):
    # Ensure the URL starts with http or https
    if not url.startswith(('http://', 'https://')):
        print("Invalid URL format. Please include http:// or https://")
        return

    # Create the folder if it doesn't exist
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    try:
        # Send a GET request to the webpage
        print(f"Fetching page: {url}")
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all links on the webpage
        pdf_links = []
        for link in soup.find_all("a", href=True):
            href = link['href']
            if href.endswith(".pdf"):
                pdf_url = urljoin(url, href)
                pdf_links.append(pdf_url)

        if pdf_links:
            print(f"Found {len(pdf_links)} PDF files.")
        else:
            print("No PDF files found.")

        # Download all PDFs found
        for pdf_url in pdf_links:
            # Decode the URL to get the original filename
            original_filename = os.path.basename(unquote(pdf_url))
            file_name = os.path.join(download_folder, original_filename)
            print(f"Downloading: {pdf_url}")
            pdf_response = requests.get(pdf_url)
            pdf_response.raise_for_status()  # Raise an error for bad responses
            with open(file_name, 'wb') as file:
                file.write(pdf_response.content)
            print(f"Downloaded: {file_name}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Example usage
website_url = "https://www.example.com"  # Replace with the actual website URL
download_pdf_files(website_url)
