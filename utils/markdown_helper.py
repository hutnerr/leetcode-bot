from markdownify import markdownify as md

def convertHTMLToMarkdown(html_content):
    try:
        return md(html_content)
    except ImportError:
        raise ImportError("Please install the 'markdownify' package to use this function.")