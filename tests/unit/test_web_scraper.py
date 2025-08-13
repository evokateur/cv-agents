from cv_agents.tools.web_scraper import JobPostingWebScraper
from cv_agents.models import JobPosting


def test_web_scraper():
    scraper = JobPostingWebScraper()
    test_url = "https://app.welcometothejungle.com/dashboard/jobs/oA1SArxV"

    result = scraper._run(test_url)

    # Basic validation
    assert isinstance(result, JobPosting)
    assert result.title == "Experienced Software Engineer"
    assert result.company == "Automattic"
    assert len(result.description) > 100
