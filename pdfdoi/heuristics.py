import re


DOI_REGEX = r"doi[:/]?\s*(\d+\.\d+/[a-z0-9-._;()/]+)"
DOIURL_REGEX = r"doi.org/(\d+\.\d+/[a-z0-9-._;()/]+)"
ARXIV_REGEX = r"arxiv:(\d+\.\d+)"

# FIXME: Add more cases like unmatched parens.
DOI_GARBAGE_REGEXES = [
    r"\.$",
    r";publishedonline.*$",
    r"availableonlineathttp$"
]

TEXT_MOJIBAKES = [
    ("兾", "/")
]


def extract_article_ids(text):
    """
    Find article IDs (DOI or arXiv ID) from text.

    Parameters
    ----------
    text : str
        Text to find article IDs.

    Yield
    -----
    article_id : str
        Article ID found in the text, prefixed by "doi:" or "arxiv:".
    """
    text = standardize_text(text)

    matches = re.findall(DOI_REGEX, text, re.IGNORECASE)
    for match in matches:
        yield "doi:" + cleanup_article_id(match)

    matches = re.findall(DOIURL_REGEX, text, re.IGNORECASE)
    for match in matches:
        yield "doi:" + cleanup_article_id(match)

    matches = re.findall(ARXIV_REGEX, text, re.IGNORECASE)
    for match in matches:
        yield "arxiv:" + cleanup_article_id(match)


def standardize_text(text):
    """
    Standardize raw text for our heuristics to work correctly.
    """
    for bake, tru in TEXT_MOJIBAKES:
        text = text.replace(bake, tru)
    return text


def cleanup_article_id(article_id):
    """
    Remove common garbages (like enclosing parens) around a valid article ID.
    """
    for garbage in DOI_GARBAGE_REGEXES:
        match = re.search(garbage, article_id)
        if match:
            beg, end = match.span()
            article_id = article_id[:beg] + article_id[end:]
    return article_id
