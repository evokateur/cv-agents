import json
import kickoff_crew

job_posting_url = "https://app.welcometothejungle.com/dashboard/jobs/oA1SArxV"
cv_data_path = "data/cv.json"
output_directory = "job_postings/automattic"


def test_main_with_config():
    config = {
        "inputs": {
            "job_posting_url": job_posting_url,
            "cv_data_path": cv_data_path,
            "output_directory": output_directory,
        }
    }
    argv = ["--config", json.dumps(config)]
    kickoff_crew.main(argv)


if __name__ == "__main__":
    test_main_with_config()
