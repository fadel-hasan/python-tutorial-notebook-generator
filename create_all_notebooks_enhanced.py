import requests
from bs4 import BeautifulSoup
import nbformat as nbf
import re
import time
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

base_url = "https://www.pythontutorial.net"

# Headers to avoid Mod_Security
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))

# Output directories
output_dirs = {
    'beginner': 'notebooks/beginner',
    'oop': 'notebooks/oop',
    'advanced': 'notebooks/advanced'
}

for dir_path in output_dirs.values():
    os.makedirs(dir_path, exist_ok=True)

def clean_filename(title):
    return re.sub(r'[^\w\-]', '_', title.lower().replace(' ', '_'))

def clean_code_block(code):
    # Remove "Code language: ..." text
    cleaned_code = re.sub(r'Code language:\s*\w+\s*\(\w+\)', '', code).strip()
    
    cleaned_code = re.sub(r'\n\s*\n', '\n', cleaned_code).strip()
    return cleaned_code

def is_python_code(code):
    python_indicators = ['def ', 'import ', 'print(', 'class ', 'return ', 'if ', 'for ', 'while ']
    return any(indicator in code for indicator in python_indicators)


def create_notebook(url, section):
    try:

        response = session.get(url, timeout=10, headers=headers)
        response.raise_for_status()


        soup = BeautifulSoup(response.content, 'html.parser')

        # Check for Mod_Security error
        if "Not Acceptable!" in soup.text:
            print(f"Error: Mod_Security blocked request for {url}")
            return False

        title = soup.find('h1').text.strip() if soup.find('h1') else "Untitled"


        content_div = soup.find('div', class_='entry-content')
        if not content_div:
            print(f"Error: No content div found for {url}")
            return False

        elements = content_div.find_all(['p', 'pre', 'h2', 'h3'])


        nb = nbf.v4.new_notebook()
        nb.cells.append(nbf.v4.new_markdown_cell(f"# {title}"))
        nb.cells.append(nbf.v4.new_markdown_cell(f"[Source Lesson]({url})"))


        
        stop_processing = False

        for element in elements:
            if element.name in ['h2', 'h3'] and re.search(r'\b(Summary|Quiz)\b', element.text.strip(), re.IGNORECASE):
                stop_processing = True
                break

            if stop_processing:
                continue
            
            if element.name == 'p':
                text = element.text.strip()
                if text:
                    nb.cells.append(nbf.v4.new_markdown_cell(text))
            elif element.name == 'pre':

                code_tag = element.find('code')
                code = code_tag.text.strip() if code_tag else element.text.strip()

                cleaned_code = clean_code_block(code)

                if cleaned_code:
                    nb.cells.append(nbf.v4.new_code_cell(cleaned_code))
                else:
                    print(f"Skipped non-Python or invalid code block in {url}")
            elif element.name in ['h2', 'h3']:
                nb.cells.append(nbf.v4.new_markdown_cell(f"## {element.text.strip()}"))


        filename = os.path.join(output_dirs[section], f"{clean_filename(title)}.ipynb")
        with open(filename, 'w', encoding='utf-8') as f:
            nbf.write(nb, f)
        print(f"Notebook saved as {filename}")
        return True

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error for {url}: {e}")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error for {url}: {e}")
        return False
    except requests.exceptions.Timeout:
        print(f"Timeout for {url}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"General error for {url}: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error for {url}: {e}")
        return False


def collect_lesson_urls():
    lesson_urls = {
        'beginner': [],
        'oop': [],
        'advanced': []
    }


    index_urls = [
        f"{base_url}/python-basics/",
        f"{base_url}/python-oop/",
        f"{base_url}/advanced-python/"
    ]

    for index_url in index_urls:
        try:
            response = session.get(index_url, timeout=10, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all links
            for a in soup.find_all('a', href=True):
                href = a['href']
                # Ensure full URL
                if href.startswith('/'):
                    href = base_url + href
                # Categorize by section, exclude index pages
                if '/python-basics/' in href and href not in lesson_urls['beginner']:
                    if href.rstrip('/') != f"{base_url}/python-basics":  
                        lesson_urls['beginner'].append(href)
                elif '/python-oop/' in href and href not in lesson_urls['oop']:
                    if href.rstrip('/') != f"{base_url}/python-oop":  
                        lesson_urls['oop'].append(href)
                elif '/advanced-python/' in href and href not in lesson_urls['advanced']:
                    if href.rstrip('/') != f"{base_url}/advanced-python":  
                        lesson_urls['advanced'].append(href)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching index {index_url}: {e}")

    return lesson_urls


def main():
    print("Collecting lesson URLs...")
    lesson_urls = collect_lesson_urls()

    for section, urls in lesson_urls.items():
        print(f"\nProcessing {section} lessons ({len(urls)} found):")
        for i, url in enumerate(urls, 1):
            print(f"[{i}/{len(urls)}] Processing {url}")
            create_notebook(url, section)
            time.sleep(1)  # Delay to avoid overwhelming the server

if __name__ == "__main__":
    main()