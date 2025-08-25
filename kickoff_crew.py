import argparse
import json
import jsonschema
import yaml
from optimizer.crew import CvOptimizer


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

    schema = {
        "type": "object",
        "properties": {
            "inputs": {
                "type": "object",
                "properties": {
                    "job_posting_url": {"type": "string"},
                    "cv_data_path": {"type": "string"},
                    "output_directory": {"type": "string"},
                },
                "required": ["job_posting_url", "cv_data_path", "output_directory"],
            }
        },
        "required": ["inputs"],
    }

    jsonschema.validate(instance=config, schema=schema)

    CvOptimizer().crew().kickoff(inputs=config.get("inputs"))


if __name__ == "__main__":
    main()
