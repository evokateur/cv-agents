import json
import optimizer.kickoff as kickoff

candidate_cv_path = "data/cv.yaml"
output_directory = "job_postings/tests"


def test_cv_optimization_with_config():
    config = {
        "inputs": {
            "candidate_cv_path": candidate_cv_path,
            "output_directory": output_directory,
        }
    }
    argv = ["--crew_name", "CvOptimizationTest", "--config", json.dumps(config)]
    kickoff.main(argv)


if __name__ == "__main__":
    test_cv_optimization_with_config()