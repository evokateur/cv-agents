import json
import optimizer.cli as kickoff

job_posting_url = "https://app.welcometothejungle.com/dashboard/jobs/oA1SArxV"
candidate_cv_path = "data/cv.yaml"
output_directory = "job_postings/automattic"


def cv_optimization_with_config():
    config = {
        "inputs": {
            "job_posting_url": job_posting_url,
            "candidate_cv_path": candidate_cv_path,
            "output_directory": output_directory,
        }
    }
    argv = ["--crew_name", "CvOptimization", "--config", json.dumps(config)]
    kickoff.main(argv)


if __name__ == "__main__":
    cv_optimization_with_config()
