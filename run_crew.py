from optimizer_new.crew import CvOptimizer

job_posting_url = "https://app.welcometothejungle.com/dashboard/jobs/oA1SArxV"
output_directory = "output/automattic"

inputs = {
    "job_posting_url": job_posting_url,
    "cv_data_path": "data/cv.yaml",
    "output_directory": output_directory,
}

CvOptimizer().crew().kickoff(inputs=inputs)
