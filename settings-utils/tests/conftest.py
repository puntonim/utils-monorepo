import pytest


@pytest.fixture(scope="session")
def monkeysession(request):
    from _pytest.monkeypatch import MonkeyPatch

    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()


@pytest.fixture(autouse=True, scope="function")
def mock_aws_credentials(monkeypatch, request):
    """
    Boto3 requires existing credentials.
    """
    if "nomoto" not in request.keywords:
        # See: http://docs.getmoto.org/en/latest/docs/getting_started.html#example-on-usage
        monkeypatch.setenv("AWS_ACCESS_KEY_ID", "pytesting")
        monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "pytesting")
        monkeypatch.setenv("AWS_SECURITY_TOKEN", "pytesting")
        monkeypatch.setenv("AWS_SESSION_TOKEN", "pytesting")
        monkeypatch.setenv("AWS_DEFAULT_REGION", "eu-south-1")
