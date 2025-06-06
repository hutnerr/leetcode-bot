PROBLEMS_URL = "https://www.leetcode.com/problems/"

# converts a title to a slug
# i.e. Two Sum -> two-sum
def titleToSlug(title: str) -> str:
    return title.replace(" ", "-").lower()

# creates a link to a problem using its slug
def slugToURL(slug: str) -> str:
    return f"{PROBLEMS_URL}{slug}"