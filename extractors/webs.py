import requests
from bs4 import BeautifulSoup
from typing import List, Dict # 🎯 Flask와 데이터 형식을 맞추기 위해 import

# --- (헬퍼 함수: scrape_data_from_soup) ---
# 이 함수는 변경할 필요가 없습니다.
def scrape_data_from_soup(soup: BeautifulSoup) -> List[Dict[str, str]]:
    """해당 페이지의 직업 목록을 파싱."""
    
    page_jobs = [] 
    jobs = soup.find_all("tr", class_="table_row")
    
    for job in jobs:
        title_tag = job.find("h2", class_="my-primary")
        title = title_tag.get_text(strip=True) if title_tag else ""
    
        if not title:
            continue
    
        company_tag = job.find("h3")
        company = company_tag.get_text(strip=True) if company_tag else ""
    
        # 위치
        location_tds = job.find_all("td", class_="job-location-mobile")
        locations = []
        if len(location_tds) > 1:
            location_td = location_tds[1]
            for a_tag in location_td.find_all("a"):
                locations.append(a_tag.get_text(strip=True))
        location = ", ".join(locations)
    
        # 스택
        stack_spans = job.find_all("span", class_="my-badge my-badge-secondary")
        stack_list = [span.get_text(strip=True) for span in stack_spans]
        stack = ", ".join(stack_list)

        link_tag = title_tag.find("a", href=True) if title_tag else None
        link = "https://web3.career" + link_tag['href'] if link_tag and link_tag['href'].startswith("/") else "N/A"
    
        job_data = {
            "position": title,
            "company": company,
            "condition": location,
            "link": link,
        }
        page_jobs.append(job_data)
        
    return page_jobs

def extract_webs_jobs(keyword: str) -> List[Dict[str, str]]:
    """
    'keyword'를 받아 해당 직무의 모든 페이지를 스크래핑합니다.
    """
    
    all_jobs = []
    current_page = 1 # 1페이지부터 시작
    
    base_url = f"https://web3.career/{keyword}-jobs"

    while True:
        url = f"{base_url}?page={current_page}"
        # print(f"Scraping: {url}") # (서버 로그)
        
        try:
            response = requests.get(url)
            response.raise_for_status() 
        except requests.RequestException as e:
            print(f"URL 요청 실패: {url} (에러: {e}). 스크래핑을 중단합니다.")
            break
    
        soup = BeautifulSoup(response.content, "html.parser")
        
        jobs_on_this_page = scrape_data_from_soup(soup)
        
        if not jobs_on_this_page:
            print(f"페이지 {current_page}에서 데이터를 찾을 수 없어 중단합니다.")
            break
            
        all_jobs.extend(jobs_on_this_page)
        # print(f"--- {current_page} 페이지 완료, {len(jobs_on_this_page)}개 수집 (총 {len(all_jobs)}개) ---")
    
        next_disabled_button = soup.select_one("li.page-item.next.disabled")
        
        if next_disabled_button:
            # print("마지막 페이지에 도달했습니다. 스크래핑을 종료합니다.")
            break 
        
        current_page += 1

    print(f"\n--- [WEBS] {keyword} 스크래핑 완료 ---")
    print(f"총 {len(all_jobs)}개의 직업 정보를 수집했습니다.")
    
    return all_jobs


if __name__ == "__main__":
    # 'python webs.py'를 터미널에서 실행하면 이 부분이 동작합니다.
    jobs = extract_webs_jobs("python")
    print("\n--- [webs.py] 테스트 실행 결과 (상위 3개) ---")
    print(jobs[:3])