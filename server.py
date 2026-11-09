
from mcp.server.mcpserver import MCPServer
from resources.career_data import register_resources
from prompts.interview_prep import register_prompts
from ai.gemini_service import generate_ai_response

from database import (
    initialize_database,
    
    add_application as db_add_application,
    get_applications as db_get_applications,
    search_applications as db_search_applications,
    update_application as db_update_application,
    get_application_stats as db_get_application_stats
)

mcp = MCPServer("CareerPilot")

# Initialize database when the server module loads.
# This also works when launched through MCP Inspector.
initialize_database()
register_resources(mcp)
register_prompts(mcp)


def validate_text(value: str, field_name: str, max_length: int) -> str:
    """Validate and normalize text input."""
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be text.")

    value = value.strip()

    if not value:
        raise ValueError(f"{field_name} cannot be empty.")

    if len(value) > max_length:
        raise ValueError(
            f"{field_name} cannot exceed {max_length} characters."
        )

    return value

@mcp.tool()
def add_application(
    company: str,
    role: str,
    status: str = "Applied"
) -> dict:
    """Add a new job application to the CareerPilot database."""

    application_id = db_add_application(
        company,
        role,
        status
    )

    return {
        "success": True,
        "application_id": application_id,
        "company": company,
        "role": role,
        "status": status
    }


@mcp.tool()
def get_applications(
    status: str | None = None
) -> list[dict]:
    """Retrieve all job applications or filter by status."""

    return db_get_applications(status)


@mcp.tool()
def search_applications(keyword: str) -> list[dict]:
    """Search applications using company name or job role."""

    return db_search_applications(keyword)


@mcp.tool()
def update_application(
    application_id: int,
    status: str
) -> dict:
    """Update the status of an existing job application."""

    updated = db_update_application(
        application_id,
        status
    )

    return {
        "success": updated,
        "message": (
            "Application updated successfully."
            if updated
            else "Application not found."
        )
    }


@mcp.tool()
def get_application_stats() -> dict:
    """Get total applications and counts grouped by status."""

    return db_get_application_stats()


@mcp.tool()
def analyze_job_description(job_description: str) -> dict:
    """
    Analyze a job description and extract skills,
    responsibilities, qualifications and interview topics.
    """

    job_description = validate_text(
    job_description,
    "Job description",
    20000
)

    if not isinstance(job_description, str):
        raise ValueError("Job description must be text.")

    job_description = job_description.strip()

    if not job_description:
        raise ValueError("Job description cannot be empty.")

    if len(job_description) > 20000:
        raise ValueError("Job description is too long.")
    
    if not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    prompt = f"""
You are an expert technical recruiter.

Analyze the following job description:

{job_description}

Provide the analysis in these sections:

1. Job Overview
2. Required Technical Skills
3. Preferred Skills
4. Key Responsibilities
5. Educational Requirements
6. Experience Requirements
7. Expected Interview Topics
8. Recommended Preparation Strategy

Clearly distinguish mandatory and preferred requirements.
"""

    result = generate_ai_response(prompt)

    return {
        "success": True,
        "analysis": result
    }


@mcp.tool()
def generate_interview_questions(
    role: str,
    company: str,
    experience_level: str = "Entry-level"
) -> dict:
    """
    Generate technical, coding and behavioral
    interview questions for a particular job.
    """


    role = validate_text(role, "Role", 200)
    company = validate_text(company, "Company", 200)
    experience_level = validate_text(
        experience_level,
        "Experience level",
        100
    )   

    if not role.strip() or not company.strip():
        raise ValueError("Role and company are required.")

    prompt = f"""
You are an experienced technical interviewer.

Generate interview preparation material for:

Company: {company}
Role: {role}
Experience Level: {experience_level}

Include:

1. 10 technical questions with answers.
2. 5 coding questions.
3. 5 behavioral questions.
4. Important concepts to revise.
5. A 3-day preparation plan.

Keep questions relevant to the job role and experience.
"""

    result = generate_ai_response(prompt)

    return {
        "success": True,
        "company": company,
        "role": role,
        "interview_questions": result
    }


@mcp.tool()
def match_candidate_profile(
    candidate_skills: list[str],
    job_description: str
) -> dict:
    """
    Compare candidate skills against job requirements
    and identify skill gaps.
    """
    
    job_description = validate_text(
        job_description,
        "Job description",
        20000
    )

    if not isinstance(candidate_skills, list):
        raise ValueError("Candidate skills must be a list.")

    if not candidate_skills:
        raise ValueError("Provide at least one candidate skill.")

    if len(candidate_skills) > 30:
        raise ValueError("You can provide a maximum of 30 skills.")

    candidate_skills = [
        validate_text(skill, "Skill", 80)
        for skill in candidate_skills
    ]

    if not candidate_skills:
        raise ValueError("Candidate skills cannot be empty.")

    if not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    skills = ", ".join(candidate_skills)

    prompt = f"""
You are an expert technical recruiter.

Compare this candidate's skills with the job description.

Candidate Skills:
{skills}

Job Description:
{job_description}

Provide:

1. Matching Skills
2. Missing Skills
3. Partially Matching Skills
4. Important Skills to Learn
5. Practical Recommendations

Give an honest assessment.
Do not invent qualifications or experience.
Do not claim this is a scientifically validated score.
"""

    result = generate_ai_response(prompt)

    return {
        "success": True,
        "candidate_skills": candidate_skills,
        "analysis": result
    }


if __name__ == "__main__":
    mcp.run()
