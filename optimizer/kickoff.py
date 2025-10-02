import argparse
import json
import jsonschema
import logging
import os
import warnings
import yaml
from optimizer.crew import (
    CvOptimization,
    CvAnalysis,
    JobAnalysis,
    CvAlignment,
    CvTransformation,
)
from optimizer.logging.console_capture import capture_console_output


def raise_exception_if_files_missing(file_paths):
    """Raise FileNotFoundError if any of the specified file paths do not exist."""
    missing_files = [path for path in file_paths if not os.path.exists(path)]

    if missing_files:
        raise FileNotFoundError(
            "Required input files are missing:\n"
            + "\n".join(f"  - {file}" for file in missing_files)
            + "\n\nRun the prerequisite crews to generate these files first."
        )


def setup_logging(output_directory, crew_name):
    os.makedirs(output_directory, exist_ok=True)

    # Convert PascalCase to snake_case
    snake_case_name = "".join(
        [
            "_" + c.lower() if c.isupper() and i > 0 else c.lower()
            for i, c in enumerate(crew_name)
        ]
    )

    console_output_log = os.path.join(output_directory, f"{snake_case_name}.log")

    # Only set up console logging for the kickoff script
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )

    logger = logging.getLogger(__name__)
    logger.info(f"Starting {crew_name} crew")
    logger.info(f"Console output logging to {console_output_log}")

    return logger, console_output_log


def dispatch_crew(crew_name, config, crew_functions):
    if crew_name not in crew_functions:
        raise ValueError(f"Unknown crew: {crew_name}")

    output_directory = config.get("inputs", {}).get("output_directory", "output")
    logger, console_output_log = setup_logging(output_directory, crew_name)

    # Capture console output while still printing to terminal
    with capture_console_output(console_output_log):
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
        "CvOptimization": kickoff_cv_optimization,
        "CvAnalysis": kickoff_cv_analysis,
        "JobAnalysis": kickoff_job_analysis,
        "CvAlignment": kickoff_cv_alignment,
        "CvTransformation": kickoff_cv_transformation,
    }

    dispatch_crew(args.crew_name, config, CREW_FUNCTIONS)


def kickoff_cv_optimization(config):
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

    CvOptimization().crew().kickoff(inputs=config.get("inputs"))


def kickoff_cv_analysis(config):
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

    CvAnalysis().crew().kickoff(inputs=config.get("inputs"))


def kickoff_job_analysis(config):
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

    JobAnalysis().crew().kickoff(inputs=config.get("inputs"))


def kickoff_cv_alignment(config):
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

    output_directory = config.get("inputs", {}).get("output_directory", "output")
    raise_exception_if_files_missing(
        [os.path.join(output_directory, "job_posting.json")]
    )

    CvAlignment().crew().kickoff(inputs=config.get("inputs"))


def kickoff_cv_transformation(config):
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

    output_directory = config.get("inputs", {}).get("output_directory", "output")
    raise_exception_if_files_missing(
        [
            os.path.join(output_directory, "job_posting.json"),
            os.path.join(output_directory, "cv_transformation_plan.json"),
        ]
    )

    CvTransformation().crew().kickoff(inputs=config.get("inputs"))


if __name__ == "__main__":
    main()
