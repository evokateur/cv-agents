import json
import optimizer.kickoff as kickoff

job_posting_url = "https://app.welcometothejungle.com/dashboard/jobs/oA1SArxV"
candidate_cv_path = "data/cv.yaml"
output_directory = "job_postings/automattic"


def test_main_with_config():
    config = {
        "inputs": {
            "job_posting_url": job_posting_url,
            "candidate_cv_path": candidate_cv_path,
            "output_directory": output_directory,
        }
    }
    argv = ["--config", json.dumps(config)]
    kickoff.main(argv)


if __name__ == "__main__":
    test_main_with_config()
