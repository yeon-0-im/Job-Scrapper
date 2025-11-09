import requests
from bs4 import BeautifulSoup
from typing import List, Dict

BASE_URL = "https://berlinstartupjobs.com/"

def combine_url(base, path):
    """'http'로 시작하거나 '/'로 시작하는 경로를 올바르게 조합합니다."""
    if path.startswith("http"):
        return path
    if path.startswith("/"):
        return base.rstrip("/") + path
    return base.rstrip("/") + "/" + path

def scrape_jobs(url: str) -> List[Dict[str, str]]:
    """
    주어진 URL(및 다음 페이지들)에서 직업 정보를 스크래핑합니다.
    """
    jobs = []
    
    while url:
        print(f"Scrapping: {url}") # 서버 로그
        try:
            resp = requests.get(url, headers={
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            })
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"URL 요청 실패: {url} (에러: {e})")
            break # URL 요청 실패 시 while 루프 중단

        soup = BeautifulSoup(resp.text, "html.parser")

        for job in soup.select("li.bjs-jlid"):
            title_tag = job.select_one(".bjs-jlid__h a")
            company_tag = job.select_one(".bjs-jlid__b")
            desc_tag = job.select_one(".bjs-jlid__description")
            stack_tags = job.select(".bjs-bl.bjs-bl-porcelain")

            title = title_tag.get_text(strip=True) if title_tag else None
            company = company_tag.get_text(strip=True) if company_tag else None
            desc = desc_tag.get_text(strip=True) if desc_tag else None
            stack_list = [tag.get_text(strip=True) for tag in stack_tags]
            stack_string = ", ".join(stack_list)
            stack = stack_string if stack_string else "N/A"
            link = title_tag["href"] if title_tag else None

            job_data = {
                "position": title,
                "company": company,
                "condition": stack,
                "link": link
            }
            jobs.append(job_data)

        next_page = soup.select_one("a.next.page-numbers")
        if next_page and next_page.get("href"):
            url = combine_url(BASE_URL, next_page["href"])
        else:
            url = None # 다음 페이지가 없으면 while 루프 종료

    return jobs

def extract_bs_jobs(keyword: str) -> List[Dict[str, str]]:

    skill_url = f"https://berlinstartupjobs.com/skill-areas/{keyword}"
    
    jobs_list = scrape_jobs(skill_url)
    
    print(f"\n--- [BSJ] {keyword} 스크래핑 완료 ---")
    print(f"총 {len(jobs_list)}개의 직업 정보를 수집했습니다.")
    
    return jobs_list


if __name__ == "__main__":
    jobs = extract_bs_jobs("python")
    print("\n--- [berlinstartupjobs.py] 테스트 실행 결과 (상위 3개) ---")
    print(jobs[:3])