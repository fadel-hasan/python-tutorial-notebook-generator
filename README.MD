# PythonTutorial Notebook Generator

This Python script automates the process of converting Python tutorials from [PythonTutorial.net](https://www.pythontutorial.net) into Jupyter Notebooks. It scrapes lesson content, organizes it into structured notebooks, and saves them in categorized folders for easy access and learning.

## Features

- **Web Scraping**: Extracts lesson content (text, code blocks, and headings) from PythonTutorial.net.
- **Jupyter Notebook Creation**: Converts lessons into `.ipynb` files with Markdown cells for text and headings, and code cells for Python code.
- **Content Filtering**:
  - Excludes index pages (e.g., `https://www.pythontutorial.net/python-basics/`).
  - Skips non-Python code blocks and invalid code.
  - Treats code outputs (e.g., `Hello John`) as Markdown cells with "Output:" prefix.
  - Excludes "Summary" and "Quiz" sections from the end of each lesson.
- **Source Linking**: Adds a clickable link to the original lesson in each notebook.
- **Error Handling**: Robust handling of network issues, HTTP errors, and Mod_Security blocks with retries.
- **Organized Output**: Saves notebooks in categorized folders (`beginner`, `oop`, `advanced`).

## Requirements

- Python 3.10 or higher
- Required Python packages:
  ```bash
  pip install requests beautifulsoup4 nbformat
  ```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/fadel-hasan/python-tutorial-notebook-generator.git
   cd python-tutorial-notebook-generator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure an active internet connection to access [PythonTutorial.net](https://www.pythontutorial.net).

## Usage

1. Run the script:
   ```bash
   python create_all_notebooks_enhanced.py
   ```

2. The script will:
   - Collect lesson URLs from the Beginner, OOP, and Advanced sections.
   - Scrape each lesson and create a Jupyter Notebook.
   - Save notebooks in the `notebooks/` directory, organized by section:
     - `notebooks/beginner/`
     - `notebooks/oop/`
     - `notebooks/advanced/`

3. Open the generated `.ipynb` files in Jupyter Notebook or JupyterLab to view and run the content.

## Output Structure

```
python-tutorial-notebook-generator/
├── notebooks/
│   ├── beginner/
│   │   ├── python_default_parameters.ipynb
│   │   ├── python_variables.ipynb
│   │   └── ...
│   ├── oop/
│   │   ├── python_classes.ipynb
│   │   ├── python_inheritance.ipynb
│   │   └── ...
│   ├── advanced/
│   │   ├── python_decorators.ipynb
│   │   ├── python_generators.ipynb
│   │   └── ...
├── create_all_notebooks_enhanced.py
├── requirements.txt
└── README.md
```

Each notebook contains:
- A title cell (e.g., `# Python Default Parameters`).
- A source link (e.g., `[Source Lesson](https://www.pythontutorial.net/python-basics/python-default-parameters/)`).
- Lesson content as Markdown cells (text and headings).
- Python code in code cells.
- Outputs in Markdown cells with "Output:" prefix.

## Notes

- **Network Issues**: If you encounter "Not Acceptable!" errors, try using a VPN or different network, as the site may block certain requests due to Mod_Security.
- **Rate Limiting**: The script includes a 1-second delay between requests to avoid overwhelming the server. Adjust `time.sleep(1)` if needed.
- **Customization**: Modify the `output_dirs` dictionary or `collect_lesson_urls` function to include other sections or websites.
- **Testing**: To test on a few lessons, limit the URLs in the `main` function:


  ```python
  for section, urls in lesson_urls.items():
      for i, url in enumerate(urls[:3], 1):  # Process only 3 lessons per section
  ```


## Acknowledgments

- [PythonTutorial.net](https://www.pythontutorial.net) for providing excellent Python tutorials.
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing.
- [nbformat](https://nbformat.readthedocs.io/) for Jupyter Notebook creation.

---

Built with ❤️ by [fadel-hasan](https://github.com/fadel-hasan)