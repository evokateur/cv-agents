import pytest
import os
from unittest.mock import Mock, patch
from cv_agents.models import JobPosting


@pytest.fixture
def mock_job_posting():
    """Mock JobPosting object for testing"""
    return JobPosting(
        title="Software Engineer",
        company="Test Company",
        requirements=["Bachelor's degree", "3+ years experience"],
        skills=["Python", "JavaScript", "SQL"],
        experience_level="Mid Level", 
        industry="Technology",
        description="A test job posting for software engineering role."
    )


@pytest.fixture
def mock_html_response():
    """Mock HTML response for web scraping tests"""
    return '''
    <html>
        <head><title>Software Engineer - Test Company</title></head>
        <body>
            <h1>Software Engineer</h1>
            <h2>Test Company</h2>
            <div class="job-description">
                We are looking for a software engineer with 3+ years experience.
                Required skills include Python, JavaScript, and SQL.
                Bachelor's degree required.
            </div>
        </body>
    </html>
    '''


@pytest.fixture
def temp_job_postings_dir(tmp_path):
    """Create temporary job postings directory for testing"""
    job_postings_dir = tmp_path / "job_postings"
    job_postings_dir.mkdir()
    return job_postings_dir