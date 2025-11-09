import time
from typing import List, Dict, Optional

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

BASE_URL = "https://weworkremotely.com"

def combine_url(base, path):
    """'http'로 시작하거나 '/'로 시작하는 경로를 올바르게 조합합니다."""
    if not path:
        return None
    if path.startswith("http"):
        return path
    if path.startswith("/"):
        return base.rstrip("/") + path
    return base.rstrip("/") + "/" + path

def setup_driver() -> webdriver.Chrome:
    """
    Selenium WebDriver(Chrome)를 설정하고 반환합니다. (Headless 모드)
    """
    # print("WebDriver를 설정하는 중입니다...") # (출력 비활성화)
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # print("WebDriver 설정 완료.") # (출력 비활성화)
    return driver

def fetch_page_soup_selenium(driver: webdriver.Chrome, url: str) -> Optional[BeautifulSoup]:
    """
    Selenium 드라이버로 URL에 접속하고, 'section.jobs'가 로드될 때까지 대기합니다.
    """
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "section.jobs"))
        )
        soup = BeautifulSoup(driver.page_source, "html.parser")
        return soup
    except Exception as e:
        print(f"Selenium으로 페이지 로드 실패: {url} (에러: {e})")
        return None

def scrape_jobs_from_soup(soup: BeautifulSoup) -> List[Dict[str, str]]:
    """
    요청하신 셀렉터 기준으로 직업 정보를 파싱합니다.
    """
    all_jobs = []
    
    job_lis = soup.select("li.new-listing-container ")
    
    for job_li in job_lis:
        
        title_tag = job_li.find("h3", class_="new-listing__header__title")
        title = title_tag.get_text(strip=True) if title_tag else "N/A"

        company_tag = job_li.find("p", class_="new-listing__company-name")
        company = company_tag.get_text(strip=True) if company_tag else "N/A"

        condition_tags = job_li.find_all("p", class_="new-listing__categories__category")
        conditions_list = [tag.get_text(strip=True) for tag in condition_tags]
        conditions = ", ".join(conditions_list)

        link_tag = job_li.select_one("a[href^='/remote-jobs/']") 
        relative_link = link_tag['href'] if link_tag and link_tag.get('href') else None
        link = combine_url(BASE_URL, relative_link)

        job_data = {
            "position": title,
            "company": company,
            "condition": conditions,
            "link" : link
        }
        all_jobs.append(job_data)
        
    return all_jobs

def extract_wwr_jobs(keyword: str):
    """
    단일 키워드를 받아 검색 결과를 스크래핑합니다.
    """
    driver = setup_driver()
    if driver is None:
        print("드라이버 초기화 실패. 프로그램을 종료합니다.")
        return

    all_jobs = [] 

    try:
        base_url = "https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term="
        url = f"{base_url}{keyword}"
        
        print(f"Scraping: {url}")
    
        soup = fetch_page_soup_selenium(driver, url)
        
        if soup is not None:
            # 파싱 함수를 호출하여 결과를 리스트에 저장
            jobs_on_this_page = scrape_jobs_from_soup(soup)
            all_jobs = jobs_on_this_page
            print(f"--- {keyword} : {len(all_jobs)}개 수집 ---")
        else:
            print(f"--- {keyword} 페이지 로드 실패 ---")
            
    finally:
        driver.quit()
        # print("\nWebDriver를 종료했습니다.")

    return all_jobs
        
# --- 실행 ---
if __name__ == "__main__":
    jobs = extract_wwr_jobs('python')