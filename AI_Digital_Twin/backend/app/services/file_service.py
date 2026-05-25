from pypdf import PdfReader
from docx import Document


def extract_text(file):

    filename = file.filename.lower()


    # PDF
    if filename.endswith(".pdf"):

        pdf = PdfReader(file.file)

        text = ""

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text


    # TXT
    elif filename.endswith(".txt"):

        text = file.file.read()

        return text.decode(
            "utf-8"
        )


    # DOCX
    elif filename.endswith(".docx"):

        document = Document(
            file.file
        )

        text = "\n".join(

            paragraph.text
            for paragraph
            in document.paragraphs

        )

        return text


    else:

        return None