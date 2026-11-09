
import json

from database import (
    get_applications,
    get_application_stats
)


def register_resources(mcp):
    """Register CareerPilot MCP resources."""

    @mcp.resource("career://applications")
    def applications_resource() -> str:
        """Read all saved job applications as JSON."""

        applications = get_applications()

        return json.dumps(
            applications,
            indent=2,
            ensure_ascii=False
        )

    @mcp.resource("career://statistics")
    def statistics_resource() -> str:
        """Read job application statistics as JSON."""

        statistics = get_application_stats()

        return json.dumps(
            statistics,
            indent=2,
            ensure_ascii=False
        )
