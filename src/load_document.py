from pathlib import Path
from pypdf import PdfReader
from clean_text import clean_page_text


# This points Python to the government AI assurance framework PDF
# that I'm using as the first public source for this project.
pdf_path = Path("data/national_ai_assurance_framework.pdf")

# Open the PDF so I can access and process each page.
reader = PdfReader(pdf_path)


# I'll store the extracted text here.
#
# I'm deliberately keeping the page number attached to the text
# rather than combining the entire document into one large block.
#
# Later, I want the prototype to be able to trace retrieved evidence
# and assessment findings back to the original public guidance.
pages_text = []


# Work through the document one page at a time.
#
# enumerate() gives me both the page itself and a page number.
# start=1 keeps the numbering consistent with how a person would
# refer to pages in the actual document.
for page_number, page in enumerate(reader.pages, start=1):

    # Extract the written text from the current PDF page.
    text = page.extract_text()

    # Some pages may not contain extractable text.
    # If that happens, I'll use an empty string instead.
    if text is None:
        text = ""

    # Clean the extracted PDF text before I store it.
    #
    # This means the rest of the project will work with a more
    # consistent version of the source material.
    text = clean_page_text(text)

    # Store the cleaned text together with its original page number.
    #
    # Preserving this metadata is important because I want any
    # retrieved evidence to remain traceable to its source.
    pages_text.append(
        {
            "page_number": page_number,
            "text": text,
        }
    )


# ---------------------------------------------------------
# TEST THE DOCUMENT LOADER
# ---------------------------------------------------------
#
# I only want these checks to run when I execute this file directly.
#
# Other parts of the project import pages_text from this file.
# Without this check, the preview messages would also print every
# time another part of the application imports the document loader.
#
# __name__ == "__main__" lets me keep useful testing code here
# without creating unnecessary output elsewhere in the application.


if __name__ == "__main__":

    # Confirm that the document was loaded and processed correctly.
    print("Document loaded successfully.")
    print(f"Number of pages: {len(reader.pages)}")
    print(f"\nPages processed: {len(pages_text)}")

    # I don't want to dump the entire government framework
    # into the terminal.
    #
    # Instead, I'll preview the first 1,500 characters from page 1
    # to make sure the extraction and cleaning still look sensible.
    print("\n--- FIRST PAGE PREVIEW ---\n")
    print(pages_text[0]["text"][:1500])