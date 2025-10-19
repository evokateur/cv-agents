import json
import optimizer.cli as kickoff

job_posting_url = "https://app.welcometothejungle.com/dashboard/jobs/oA1SArxV"
output_directory = "job_postings/automattic"


def job_analysis_with_config():
    config = {
        "inputs": {
            "job_posting_url": job_posting_url,
            "output_directory": output_directory,
        }
    }
    argv = ["--crew_name", "JobAnalysis", "--config", json.dumps(config)]
    kickoff.main(argv)


if __name__ == "__main__":
    job_analysis_with_config()
