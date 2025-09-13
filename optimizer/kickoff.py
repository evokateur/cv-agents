import argparse
import json
import jsonschema
import yaml
from optimizer.crew import CvOptimizer, JobAnalysisTest, CvAlignmentTest, CvOptimizationTest


def dispatch_crew(crew_name, config, crew_functions):
    if crew_name not in crew_functions:
        raise ValueError(f"Unknown crew: {crew_name}")
    crew_functions[crew_name](config)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--crew_name", default="CvOptimizer", help="Crew name")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--config", type=str, help="Config as JSON/YAML string")
    group.add_argument("--config_path", type=str, help="Path to config file")
    args = parser.parse_args(argv)

    config = {}
    if args.config:
        # Try JSON first, then YAML
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
