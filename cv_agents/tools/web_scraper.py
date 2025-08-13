import requests
from bs4 import BeautifulSoup
from typing import Optional
from crewai.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from ..models import JobPosting


class WebScraperInput(BaseModel):
    url: str = Field(description="URL of the job posting to scrape")


class JobPostingWebScraper(BaseTool):
    name: str = "job_posting_web_scraper"
    description: str = "Extract job posting information from a URL"
    args_schema: type[BaseModel] = WebScraperInput

    def _run(self, url: str) -> JobPosting:
        """
        Scrape job posting from URL and return structured JobPosting object
        """
        try:
            headers = {
                'User-Agent': 'CV-Optimizer/1.0 (Mozilla/5.0 compatible)'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract job posting information
            job_data = self._extract_job_data(soup, url)
            
            return JobPosting(**job_data)
            
        except Exception as e:
            raise Exception(f"Failed to scrape job posting from {url}: {str(e)}")
    
    def _extract_job_data(self, soup: BeautifulSoup, url: str) -> dict:
        """
        Extract job posting data from BeautifulSoup object
        This method handles different job board formats
        """
        # Try to extract title
        title = self._extract_title(soup)
        
        # Try to extract company
        company = self._extract_company(soup)
        
        # Extract description text
        description = self._extract_description(soup)
        
        # Extract requirements and skills from description
        requirements, skills = self._parse_requirements_and_skills(description)
        
        # Try to determine experience level
        experience_level = self._extract_experience_level(soup, description)
        
        # Try to determine industry
        industry = self._extract_industry(soup, description)
        
        return {
            "title": title or "Unknown Position",
            "company": company or "Unknown Company", 
            "requirements": requirements,
            "skills": skills,
            "experience_level": experience_level,
            "industry": industry,
            "description": description
        }
    
    def _extract_title(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract job title from various selectors"""
        selectors = [
            'h1',
            '[data-testid="job-title"]',
            '.job-title',
            '.position-title',
            'title'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text().strip()
                if text and len(text) > 3:  # Basic validation
                    return text
        
        return None
    
    def _extract_company(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract company name from various selectors"""
        selectors = [
            '[data-testid="company-name"]',
            '.company-name',
            '.employer-name',
            '.company',
            'h2'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text().strip()
                if text and len(text) > 1:
                    return text
        
        return None
    
    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract job description text"""
        # Look for job description containers
        selectors = [
            '[data-testid="job-description"]',
            '.job-description',
            '.description',
            '.job-content',
            'main',
            'article'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                # Get text and clean it up
                text = element.get_text(separator=' ', strip=True)
                if len(text) > 100:  # Ensure we got substantial content
                    return text
        
        # Fallback: get all text from body
        body = soup.find('body')
        if body:
            return body.get_text(separator=' ', strip=True)
        
        return soup.get_text(separator=' ', strip=True)
    
    def _parse_requirements_and_skills(self, description: str) -> tuple[list[str], list[str]]:
        """
        Parse requirements and skills from job description text
        This is a simple implementation - could be enhanced with NLP
        """
        description_lower = description.lower()
        
        # Common requirement keywords
        req_keywords = [
            "bachelor's degree", "master's degree", "phd", "certification",
            "years of experience", "experience with", "knowledge of",
            "proficiency in", "expertise in", "familiarity with"
        ]
        
        # Common skill keywords  
        skill_keywords = [
            "python", "javascript", "java", "c++", "sql", "html", "css",
            "react", "angular", "vue", "node.js", "django", "flask",
            "aws", "azure", "gcp", "docker", "kubernetes", "git",
            "machine learning", "data science", "ai", "ml"
        ]
        
        requirements = []
        skills = []
        
        # Simple keyword matching
        for req in req_keywords:
            if req in description_lower:
                # Find the sentence containing this requirement
                sentences = description.split('.')
                for sentence in sentences:
                    if req in sentence.lower():
                        requirements.append(sentence.strip())
                        break
        
        for skill in skill_keywords:
            if skill in description_lower:
                skills.append(skill.title())
        
        # Remove duplicates
        requirements = list(set(requirements))
        skills = list(set(skills))
        
        return requirements[:10], skills[:15]  # Limit list sizes
    
    def _extract_experience_level(self, soup: BeautifulSoup, description: str) -> str:
        """Determine experience level from posting"""
        description_lower = description.lower()
        
        if any(word in description_lower for word in ["entry level", "junior", "graduate", "0-2 years"]):
            return "Entry Level"
        elif any(word in description_lower for word in ["senior", "lead", "principal", "5+ years", "7+ years"]):
            return "Senior Level"
        elif any(word in description_lower for word in ["mid level", "intermediate", "3-5 years"]):
            return "Mid Level"
        else:
            return "Not Specified"
    
    def _extract_industry(self, soup: BeautifulSoup, description: str) -> str:
        """Determine industry from posting"""
        description_lower = description.lower()
        
        industries = {
            "Technology": ["software", "tech", "development", "programming", "data", "ai", "ml"],
            "Finance": ["finance", "banking", "fintech", "trading", "investment"],
            "Healthcare": ["healthcare", "medical", "hospital", "pharma"],
            "Consulting": ["consulting", "advisory", "strategy"],
            "Education": ["education", "university", "academic", "teaching"]
        }
        
        for industry, keywords in industries.items():
            if any(keyword in description_lower for keyword in keywords):
                return industry
        
        return "Other"


# Create tool instance
job_posting_scraper = JobPostingWebScraper()