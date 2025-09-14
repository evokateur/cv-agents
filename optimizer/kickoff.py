import argparse
import json
import jsonschema
import logging
import os
import warnings
import yaml
from optimizer.crew import CvOptimizer, JobAnalysisTest, CvAlignmentTest, CvOptimizationTest


def setup_logging(output_directory, crew_name):
    os.makedirs(output_directory, exist_ok=True)
    log_file = os.path.join(output_directory, f"{crew_name.lower()}.log")

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger(__name__)
    logger.info(f"Starting {crew_name} with logging to {log_file}")
    return logger


def dispatch_crew(crew_name, config, crew_functions):
    if crew_name not in crew_functions:
        raise ValueError(f"Unknown crew: {crew_name}")

    output_directory = config.get("inputs", {}).get("output_directory", "output")
    setup_logging(output_directory, crew_name)

    crew_functions[crew_name](config)


def main(argv=None):
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    parser = argparse.ArgumentParser()
    parser.add_argument("--crew_name", default="CvOptimizer", help="Crew name")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--config", type=str, help="Config as JSON/YAML string")
    group.add_argument("--config_path", type=str, help="Path to config file")
    args = parser.parse_args(argv)

    config = {}
    if args.config:
        try:
            config = json.loads(args.config)
        except json.JSONDecodeError:
            config = yaml.safe_load(args.config)
    elif args.config_path:
        with open(args.config_path) as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError:
                config = yaml.safe_load(f)

    CREW_FUNCTIONS = {
        "CvOptimizer": kickoff_cv_optimizer,
        "JobAnalysisTest": kickoff_job_analysis_test,
        "CvAlignmentTest": kickoff_cv_alignment_test,
        "CvOptimizationTest": kickoff_cv_optimization_test,
    }

    dispatch_crew(args.crew_name, config, CREW_FUNCTIONS)


def kickoff_cv_optimizer(config):
    schema = {
        "type": "object",
        "properties": {
            "inputs": {
                "type": "object",
                "properties": {
                    "job_posting_url": {"type": "string"},
                    "candidate_cv_path": {"type": "string"},
                    "output_directory": {"type": "string"},
                },
                "required": [
                    "job_posting_url",
                    "candidate_cv_path",
                    "output_directory",
                ],
            }
        },
        "required": ["inputs"],
    }

    jsonschema.validate(instance=config, schema=schema)

    CvOptimizer().crew().kickoff(inputs=config.get("inputs"))


def kickoff_job_analysis_test(config):
    schema = {
        "type": "object",
        "properties": {
            "inputs": {
                "type": "object",
                "properties": {
                    "job_posting_url": {"type": "string"},
                    "output_directory": {"type": "string"},
                },
                "required": ["job_posting_url"],
            }
        },
        "required": ["inputs"],
    }

    jsonschema.validate(instance=config, schema=schema)

    JobAnalysisTest().crew().kickoff(inputs=config.get("inputs"))


def kickoff_cv_alignment_test(config):
    schema = {
        "type": "object",
        "properties": {
            "inputs": {
                "type": "object",
                "properties": {
                    "candidate_cv_path": {"type": "string"},
                    "output_directory": {"type": "string"},
                },
                "required": ["candidate_cv_path"],
            }
        },
        "required": ["inputs"],
    }

    jsonschema.validate(instance=config, schema=schema)

    CvAlignmentTest().crew().kickoff(inputs=config.get("inputs"))


def kickoff_cv_optimization_test(config):
    schema = {
        "type": "object",
        "properties": {
            "inputs": {
                "type": "object",
                "properties": {
                    "candidate_cv_path": {"type": "string"},
                    "output_directory": {"type": "string"},
                },
                "required": ["candidate_cv_path"],
            }
        },
        "required": ["inputs"],
    }

    jsonschema.validate(instance=config, schema=schema)

    CvOptimizationTest().crew().kickoff(inputs=config.get("inputs"))


if __name__ == "__main__":
    main()
