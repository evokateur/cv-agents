import pytest
from optimizer.tasks import CustomTasks
from optimizer.models import JobPosting, CandidateProfile
from optimizer.agents import CustomAgents


class TestCandidateProfilingTask:
    def test_candidate_profiling_task_description_schema_injection(self):
        """Test that JobPosting schema is properly injected into candidate profiling task description."""
        # Create a rudimentary JobPosting
        job_posting = JobPosting(
            title="Senior Python Developer",
            company="Tech Corp",
            industry="Software Development",
            description="Build scalable web applications using Python and Django",
            experience_level="Senior",
            requirements=["Bachelor's degree in CS", "5+ years Python experience"],
            required_skills=["Python", "Django", "PostgreSQL", "REST APIs"],
            preferred_skills=["AWS", "Docker", "Redis", "GraphQL"],
            responsibilities=[
                "Design APIs",
                "Code reviews",
                "Mentor junior developers",
            ],
        )

        # Create tasks instance
        tasks = CustomTasks()

        # Create a mock agent (we don't need it for this test)
        agents = CustomAgents()
        mock_agent = agents.candidate_profiler()

        # Create candidate profiling task with empty context (no job analysis task result)
        task = tasks.candidate_profiling_task(mock_agent, context_tasks=[])

        # Check that the task description contains the JobPosting schema
        description = task.description

        # Verify that [[JobPosting]] placeholder was replaced with actual schema
        assert "[[JobPosting]]" not in description, (
            "JobPosting placeholder should be replaced"
        )

        # Verify that JobPosting field names appear in the description
        job_posting_fields = [
            "title",
            "company",
            "industry",
            "description",
            "experience_level",
            "requirements",
            "required_skills",
            "preferred_skills",
            "responsibilities",
        ]

        for field in job_posting_fields:
            assert field in description, (
                f"JobPosting field '{field}' should appear in description"
            )

        # Verify that type information is included
        assert "str" in description, (
            "String type should be mentioned for JobPosting fields"
        )
        assert "List[str]" in description, (
            "List[str] type should be mentioned for JobPosting fields"
        )

        # Verify that the core task instructions are still present
        assert "CandidateKnowledgeBase" in description, (
            "Task should mention using the knowledge base"
        )
        assert "semantic search" in description, "Task should mention semantic search"
        assert "CandidateProfile" in description, "Task should mention output type"

    def test_candidate_profiling_task_has_correct_output_type(self):
        """Test that candidate profiling task is configured with CandidateProfile output."""
        tasks = CustomTasks()
        agents = CustomAgents()
        mock_agent = agents.candidate_profiler()

        task = tasks.candidate_profiling_task(mock_agent, context_tasks=[])

        # Verify the task has the correct Pydantic output model
        assert task.output_pydantic == CandidateProfile

        # Verify the agent is set correctly
        assert task.agent == mock_agent

    def test_candidate_profiling_task_yaml_config_integration(self):
        """Test that YAML config is properly integrated with dynamic description."""
        tasks = CustomTasks()
        agents = CustomAgents()
        mock_agent = agents.candidate_profiler()

        task = tasks.candidate_profiling_task(mock_agent, context_tasks=[])

        # Check that YAML config properties are preserved
        yaml_config = tasks.tasks_config["candidate_profiling_task"]

        # Expected output should match YAML
        assert "CandidateProfile" in task.expected_output
        assert "experiences" in task.expected_output
        assert "skills" in task.expected_output
        assert "projects" in task.expected_output

        # Output file should match YAML template
        assert task.output_file == yaml_config["output_file"]


class TestPromptUtilsIntegration:
    def test_jobposting_schema_rendering_in_isolation(self):
        """Test the prompt utils schema rendering functionality in isolation."""
        from optimizer.utils.prompt_utils import render_pydantic_models_in_prompt

        template = """
        Here is the JobPosting schema:
        [[JobPosting]]
        
        And some other text with {regular_placeholder}.
        """

        rendered = render_pydantic_models_in_prompt(
            template, model_registry={"JobPosting": JobPosting}
        )

        # Verify placeholder was replaced
        assert "[[JobPosting]]" not in rendered

        # Verify regular placeholders are preserved
        assert "{regular_placeholder}" in rendered

        # Verify JobPosting fields appear
        assert "title (str)" in rendered
        assert "required_skills (List[str])" in rendered
        assert "preferred_skills (List[str])" in rendered

    def test_unrecognized_schema_placeholders_preserved(self):
        """Test that unrecognized [[Model]] placeholders are left unchanged."""
        from optimizer.utils.prompt_utils import render_pydantic_models_in_prompt

        template = "Known: [[JobPosting]] Unknown: [[NonExistentModel]]"

        rendered = render_pydantic_models_in_prompt(
            template, model_registry={"JobPosting": JobPosting}
        )

        # Known model should be replaced
        assert "[[JobPosting]]" not in rendered
        assert "title (str)" in rendered

        # Unknown model should be preserved
        assert "[[NonExistentModel]]" in rendered

