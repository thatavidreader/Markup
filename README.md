# File to Markdown Convrter

This is a simple HTTP server that converts various document formats (like DOCX) to Markdown using the MarkItDown library and stores the results in a MongoDB database.

## Features

- Upload files.
- Convert uploaded files to Markdown.
- Store converted Markdown in a MongoDB database.
- Retrieve the converted Markdown and file ID in JSON format.

## Prerequisites
- Python 3.8 or later
- MongoDB installed and running
- Required Python libraries (see `requirements.txt`)

## Installation
1. Clone the repository:

   ```bash
   git clone https://github.com/Encaenia/file-to-markdown.git
   cd file-to-markdown
