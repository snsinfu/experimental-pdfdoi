from pdfminer.layout import LTContainer, LTText
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice


def extract_pages(pdf):
    """
    Extract pages from a PDF file.

    Paramters
    ---------
    pdf : file
        PDF file to parse. Must be a file opened in binary mode.

    Yields
    ------
    page_layout : LTPage
        Interpreted LTPage object for a page.
    """
    parser = PDFParser(pdf)
    document = PDFDocument(parser)

    if not document.is_extractable:
        return

    resource_manager = PDFResourceManager()
    device = PDFPageAggregator(resource_manager)
    interpreter = PDFPageInterpreter(resource_manager, device)

    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        yield device.get_result()


def extract_text_blocks(layout, space_tol):
    """
    Extract text blocks from a PDF layout object and its descendants.

    Parameters
    ----------
    layout : object
        PDFMiner layout object (LTText, LTContainer, etc.).

    space_tol : float
        Maximum space before a text item to be considered as a continuation of its
        previous item. The unit is min(width, height) of the previous item. Too small
        value produces fragmented texts and too large value produces coalesced words.

    Yields
    -------
    text : string
        Content of a text block.
    """
    text = ""
    prev_item = None

    def is_text(item):
        return isinstance(item, LTText)

    def is_container(item):
        return isinstance(item, LTContainer)

    for item in layout:
        if is_text(item):
            max_distance = space_tol * min(item.width, item.height)
            if is_text(prev_item) and item.hdistance(prev_item) > max_distance:
                if len(text) > 0:
                    yield text
                    text = ""
            text += item.get_text()
        elif is_container(item):
            for text in extract_text_blocks(item, space_tol):
                yield text
        else:
            if len(text) != 0:
                yield text
                text = ""
        prev_item = item

    if len(text) != 0:
        yield text
