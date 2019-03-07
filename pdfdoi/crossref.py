import urllib.request as request


AUTHOR_EMAIL = "sinfu@nagoya-u.jp"
USER_AGENT = f"pdfdoi (mailto:{AUTHOR_EMAIL})"
CROSSREF_ENDPOINT = "https://api.crossref.org/works"
CROSSREF_CHARSET = "utf-8"
MIMETYPE_BIBTEX = "application/x-bibtex"


def query_bibtex(doi):
    """
    Query CrossRef server for a bibtex entry for the DOI-specified work.
    """
    url = f"{CROSSREF_ENDPOINT}/{doi}/transform/{MIMETYPE_BIBTEX}"
    req = request.Request(url)
    req.add_header("User-Agent", USER_AGENT)
    with request.urlopen(req) as resp:
        if resp.status // 100 != 2:
            raise Exception(f"HTTP {resp.status}: {resp.reason}")
        return resp.read().decode(CROSSREF_CHARSET)
