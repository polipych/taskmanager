import pytest
from tmapp.models import Project, Task, User


@pytest.fixture
def test_create_user(db):
    user = User.objects.create_user("TestUser")
    # assert user.username == "TestUser"
    return user


def test_update_user(test_create_user):
    test_create_user.email = "test@test.xz"
    test_create_user.save()
    test_create_user_from_db = User.objects.get(email="test@test.xz")
    assert test_create_user_from_db.email == "test@test.xz"


@pytest.fixture
def project(db) -> Project:
    return Project.objects.create(
        title="PytestProject",
        key="TKEYFIX",
    )


def test_filter_project(project):
    assert Project.objects.filter(title="PytestProject").exists()


def test_update_project(project):
    project.title = "PytestProjectChange"
    project.save()
    project_from_db = Project.objects.get(title="PytestProjectChange")
    assert project_from_db.title == "PytestProjectChange"


@pytest.fixture
def task_one(db, project, test_create_user):
    return Task.objects.create(title="Task1", project=project, author=test_create_user)


@pytest.fixture
def task_two(db, project, test_create_user):
    return Task.objects.create(title="Task2", project=project, author=test_create_user)


def test_two_different_tasks_create(task_one, task_two):
    assert task_one.pk != task_two.pk
