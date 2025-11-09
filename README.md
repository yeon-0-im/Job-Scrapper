# ⌨ Job Scrapper 

A simple and lightweight web application built with Flask that aggregates job postings from multiple sources.
Users can search for jobs by keyword (like `python`) and view the results in a clean, unified table.


---

## 🚀 Features

* **Keyword-Based Search:** Allows users to search for job postings using specific technologies or terms (e.g., `python`, `javascript`, `java`).
* **Multi-Site Aggregation:** Scrapes and combines job listings from three different platforms:
    * [Weworkremotely.com](https://weworkremotely.com/)
    * [Web3.career](https://web3.career/)
    * [Berlinstartupjobs.com](https://berlinstartupjobs.com/)
* **Result Caching:** The first search for a specific keyword triggers the scrapers. Subsequent searches for the same keyword retrieve results instantly from an in-memory cache (`db = {}`), minimizing wait times and reducing server load.
* **Dynamic Scraping:** Uses both `requests` for static sites and `Selenium` for dynamic, JavaScript-heavy sites (like `weworkremotely.com`) that require browser automation.
* **Unified & Clean UI:** A minimalist front-end built with Flask and **Pico.css** for a clean, responsive table layout. The table clearly displays four key pieces of information for each job:
    * Position
    * Company
    * Condition (This may include location, required skills, or other tags)
    * Link (A direct "Apply" link to the original posting)

---

## 🛠️ Technologies Used

### Backend & Scraping
* **Python:** The core programming language.
* **Flask:** A micro web framework used to build the front-end, serve pages, and handle routing.
* **BeautifulSoup4 (`bs4`):** A library for parsing HTML and XML documents, used to extract job data from the raw HTML.
* **Requests:** A simple HTTP library for fetching static HTML from `web3.career` and `berlinstartupjobs.com`.
* **Selenium:** A browser automation framework used to scrape `weworkremotely.com`, which requires JavaScript execution to load content.
* **Webdriver Manager:** A library to automatically manage the `chromedriver` binary required by Selenium.

### Frontend
* **HTML5:** For the basic structure of the web pages.
* **[Pico.css](https://picocss.com/):** A lightweight, semantic CSS framework for styling the application without custom CSS.

---

## 📂 Project Structure

Here is a simplified overview of the project's file structure:
```bash
Job-Scrapper/
├── Main.py                  # Main Flask application (routing, caching)
├── File.py                  # Save result
│
├── extractors/
│   ├── wwr.py                # Scraper for Weworkremotely (uses Selenium)
│   ├── webs.py               # Scraper for Web3.career (uses Requests)
│   └── berlinstartupjobs.py  # Scraper for Berlin Startup Jobs (uses Requests)
│
└── templates/
    ├── home.html             # The main landing page with the search bar
    └── search.html           # The page that displays the job results table
```

---
#### And this all started and ended with a lecture at 💻 https://nomadcoders.co/ 💻 Thank you so much NICO!
