import os
from fpdf import FPDF, HTMLMixin
from database import *


def make_pdf(appraisal):
    class WriteHtmlPDF(FPDF, HTMLMixin):
        pass

    document = WriteHtmlPDF()
    #class object FPDF() which is predefiend in side the package fpdf.
    #document=FPDF()
    document.add_page()

    #borders
    document.set_line_width(0.0)#
    #outer
    document.line(5.0, 5.0, 205.0, 5.0) # top one
    document.line(205.0, 5.0, 205.0, 292.0) # right one
    document.line(205.0, 292.0, 5.0, 292.0) # bottom one
    document.line(5.0, 292.0, 5.0, 5.0) # left one
    #inner
    document.line(6.0, 6.0, 204.0, 6.0) # top one
    document.line(204.0, 6.0, 204.0, 291.0) # right one
    document.line(204.0, 291.0, 6.0, 291.0) # bottom one
    document.line(6.0, 291.0, 6.0, 6.0) # left one

    #text
    employee = getUser(appraisal['employee_id'])
    appraiser = getUser(appraisal['appraiser_id'])

    html =  f"""<div class='pdf_appraisal-container'>
                <h1>Report Number {appraisal['report_number']}</h1>
                <h3>Date: {appraisal['date']}</h3>
                <h3>Status: {appraisal['status']}</h3>
                <h3>Employee Name: {employee['first_name']} {employee['last_name']}</h3>
                <h3>Appraiser Last Name: {appraiser['first_name']} {appraiser['last_name']}</h3>
                <h3>Report:</h>
                <p>{appraisal['report']}</p>
                <h3>Reviewer Comment</h3>
                <p>{appraisal['reviewer_comment']}<p>
                </div>"""
    document.write_html(html)

    #pdf file naming.
    document.output(name="Appraisal.pdf")
    #creating page format A4 Or A3 Or ...
    document=FPDF(orientation='P', unit='mm', format='A4')
    
    os.system('Appraisal.pdf')

    print("pdf has been created successfully")