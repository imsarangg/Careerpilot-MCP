
def register_prompts(mcp):
    """Register CareerPilot reusable MCP prompts."""

    @mcp.prompt()
    def interview_prep(
        role: str,
        company: str,
        experience_level: str = "Entry-level"
    ) -> str:
        """Create a structured interview preparation prompt."""

        return f"""
You are an experienced technical interviewer.

Prepare a detailed interview guide for the following position.

Company: {company}
Job Role: {role}
Experience Level: {experience_level}

Include:

1. Company and role-specific preparation areas.
2. 10 technical interview questions.
3. 5 practical coding or problem-solving questions.
4. 5 behavioral interview questions.
5. Important concepts to revise.
6. Sample answers for the most important questions.
7. A suggested 3-day preparation plan.

Keep the questions relevant to the specified role
and experience level.

Present the response in a structured format.
"""

    @mcp.prompt()
    def job_description_analysis(
        job_description: str
    ) -> str:
        """Create a prompt for analyzing a job description."""

        return f"""
You are an expert technical recruiter and career advisor.

Analyze this job description:

{job_description}

Provide:

1. Key technical skills required.
2. Required programming languages and frameworks.
3. Important responsibilities.
4. Experience and qualification requirements.
5. Expected interview topics.
6. Skills a candidate should prepare.
7. Potential gaps to address before applying.

Separate mandatory requirements from preferred skills.
Present the analysis in a structured format.
"""
