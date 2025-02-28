import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def create_blank_page(output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    c.showPage()
    c.save()

def merge_pdfs(test_file, notest_file, output_file, insert_blank=True):
    if insert_blank:
        blank_page_path = os.path.join(os.path.dirname(output_file), "blank.pdf")
        create_blank_page(blank_page_path)
    
    pdf_writer = PdfWriter()
    pdf_files = [test_file]
    
    if insert_blank:
        pdf_files.append(blank_page_path)
    
    pdf_files.append(notest_file)
    
    for pdf in pdf_files:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
    
    with open(output_file, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)
    
    # Delete the temporary blank.pdf file if it was created
    if insert_blank and os.path.exists(blank_page_path):
        os.remove(blank_page_path)

def process_folder(directory):
    for root, _, files in os.walk(directory):
        test_files = [f for f in files if f.endswith('_test.pdf')]
        notest_files = [f for f in files if f.endswith('_notest.pdf')]

        for test_file in test_files:
            base_name = test_file.replace('_test.pdf', '')
            notest_file = f'{base_name}_notest.pdf'
            
            if notest_file in notest_files:
                test_path = os.path.join(root, test_file)
                notest_path = os.path.join(root, notest_file)
                output_path = os.path.join(root, f'{base_name}.pdf')
                merge_pdfs(test_path, notest_path, output_path)
                print(f'Creato: {output_path}')