# PHP Internals Book Web Scraper 

This is a web scraper that downloads the contents of the ["PHP Internals Book"][1].

## Install

To install dependencies:
    
    pip install -r requirements.txt

## Download the book

The script downloads all the pages and images of the book, and packs them into a single HTML file.
Run:

    python crawler.py > php-internals-book.html


## Export as PDF:

The downloaded content can be also exported to PDF using `weasyprint`:

    weasyprint php-internals-book.html php-internals-book.pdf

[1]:http://www.phpinternalsbook.com/
