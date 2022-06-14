"# simple_PDF_steganography_tools" 

This repository contains few Python3 tools for PDF steganography and steganalysis.
All of the tools were written during working on Bachelor thesis "Research on PDF Files Steganalysis" (originally written in Latvian).

##############################################################################################################################################

Algorithms used for PDF steganography tools (more details in writeStego.py and readStego.py comments):
 - Modifying /MediaBox array's values 
 - Modifying Page Tree's /Count value to hide pages (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7517136/)
 - Modifying PDF stream's TJ text operator's values
*Tools for hiding data in PDF files were written for Windows OS.

##############################################################################################################################################

Tools for analyzing PDF stream's text operators.
 - Counting how many text operators' values the PDF file contains
 - Extracting all of the TJ operator's values [for steganalysis against pdf_hide tool (https://github.com/ncanceill/pdf_hide) by N. Canceill]
*Tools for hiding data in PDF files were written for Linux OS and require qpdf (https://github.com/qpdf/qpdf) installation:

sudo apt-get update
sudo apt-get install qpdf

##############################################################################################################################################

BONUS:
 - Tool for extracting a file hidden in a PDF document via wbStego4open software (http://wbstego.wbailer.com/)

That's more of a 'for fun' tool since wbStego4open is an open-source project. Furthermore, you can simply extract
hidden file using wbStego4open software.
