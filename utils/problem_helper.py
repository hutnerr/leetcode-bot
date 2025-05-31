def titleToSlug(title: str) -> str:
    return title.replace(" ", "-").lower()

def slugToURL(slug: str) -> str:
    return f"https://www.leetcode.com/problems/{slug}"