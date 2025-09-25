import json
import optimizer.kickoff as kickoff

candidate_cv_path = "data/cv.yaml"
output_directory = "job_postings/automattic"


def cv_transformation_with_config():
    config = {
        "inputs": {
            "candidate_cv_path": candidate_cv_path,
            "output_directory": output_directory,
        }
    }
    argv = ["--crew_name", "CvTransformation", "--config", json.dumps(config)]
    kickoff.main(argv)


if __name__ == "__main__":
    cv_transformation_with_config()

