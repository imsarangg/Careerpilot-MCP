
from database import (
    add_application,
    get_applications,
    search_applications,
    update_application,
    get_application_stats
)


def test_add_application(test_database):
    application_id = add_application(
        "Google",
        "Python Developer Intern"
    )

    assert application_id > 0


def test_get_applications(test_database):
    add_application("Google", "Python Developer")

    applications = get_applications()

    assert len(applications) == 1
    assert applications[0]["company"] == "Google"


def test_search_applications(test_database):
    add_application("Microsoft", "Software Engineer")

    results = search_applications("Microsoft")

    assert len(results) == 1


def test_update_application(test_database):
    application_id = add_application(
        "Amazon",
        "Backend Developer"
    )

    updated = update_application(
        application_id,
        "Interview"
    )

    assert updated is True

    applications = get_applications("Interview")

    assert len(applications) == 1


def test_application_statistics(test_database):
    add_application("Google", "Python Developer")
    add_application("Microsoft", "Backend Developer")

    stats = get_application_stats()

    assert stats["total_applications"] == 2
    assert stats["by_status"]["Applied"] == 2
