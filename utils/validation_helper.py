import re

from errors.simple_exception import SimpleException

# leetcode usernames are alphanumeric, underscores, and hyphens
USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_-]{1,39}$")

# leetcode slugs are lowercase words separated by single hyphens
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MAX_SLUG_LENGTH = 150

MAX_SUBMISSION_LIMIT = 100

# validates a leetcode username before it is sent in an api request
def validateUsername(username: str) -> str:
    if not isinstance(username, str) or not USERNAME_PATTERN.match(username):
        raise SimpleException(
            "INVALID_USERNAME",
            "Invalid LeetCode username",
            "Usernames can only contain letters, numbers, underscores, and hyphens."
        )
    return username

# validates a leetcode problem slug before it is sent in an api request
def validateSlug(slug: str) -> str:
    if not isinstance(slug, str) or len(slug) > MAX_SLUG_LENGTH or not SLUG_PATTERN.match(slug):
        raise SimpleException(
            "INVALID_SLUG",
            "Invalid problem slug",
            "Problem slugs can only contain lowercase letters, numbers, and hyphens."
        )
    return slug

# validates a submission limit before it is sent in an api request
def validateLimit(limit: int, maximum: int = MAX_SUBMISSION_LIMIT) -> int:
    if not isinstance(limit, int) or limit < 1 or limit > maximum:
        raise SimpleException(
            "INVALID_LIMIT",
            "Invalid request limit",
            f"Limit must be an integer between 1 and {maximum}."
        )
    return limit
