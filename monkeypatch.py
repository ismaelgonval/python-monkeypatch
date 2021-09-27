import base64
import os
import github
from github import Github, GithubIntegration, Organization


def get_random_stuff(self):
    return "Random stuff"


setattr(Organization.Organization, "get_random", get_random_stuff)

_PRIVATE_KEY = os.environ.get("GH_PRIVATE_KEY")
_APP_ID = os.environ.get("GH_APP_ID")
_INSTALLATION_ID = os.environ.get("GH_INSTALLATION_ID")
_RETRIES = 5


def generate_client() -> Github:
    """Generate a new GitHub client authenticated via GitHub App."""
    if not _PRIVATE_KEY or not _APP_ID or not _INSTALLATION_ID:
        raise EnvironmentError("Information not found in env var.")

    private_key = base64.b64decode(_PRIVATE_KEY).decode("utf-8")

    app = GithubIntegration(int(_APP_ID), private_key)
    token = app.get_access_token(int(_INSTALLATION_ID))

    return Github(token.token, retry=_RETRIES, per_page=100)


if __name__ == "__main__":
    gh_client = generate_client()
    organization = gh_client.get_organization("inditex")
    print(organization.get_random())
