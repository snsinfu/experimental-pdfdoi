import argparse
import signal

from . import heuristics
from . import pdf


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    return run(**parse_args())


def run(files, max_page, space_tol):
    for path in files:
        with open(path, "rb") as file:
            article_id = extract_article_id(file, max_page, space_tol) or "?"
        print(f"{article_id}\t{path}")


def parse_args():
    parser = argparse.ArgumentParser(description="Extract DOI from PDF files.")
    parser.add_argument(
        "--max-page",
        type=int,
        default=5,
        help="specify number of leading pages to look for a DOI (default: 5)",
    )
    parser.add_argument(
        "--space-tol",
        type=float,
        default=1,
        help="specify tolerable margin between fragmented text objects (default: 1)",
    )
    parser.add_argument("files", type=str, nargs="*")
    return vars(parser.parse_args())


def extract_article_id(file, max_page, space_tol):
    for page_index, page in enumerate(pdf.extract_pages(file)):
        if page_index == max_page:
            break
        for text in pdf.extract_text_blocks(page, space_tol):
            for article_id in heuristics.extract_article_ids(text):
                # Take the first hit.
                return article_id
    return None


if __name__ == "__main__":
    main()
