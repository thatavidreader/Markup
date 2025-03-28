from http.server import BaseHTTPRequestHandler
import os
import json
import cgi
from pymongo import MongoClient
from markitdown import MarkItDown

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

#mongodb connection
client = MongoClient("mongodb://localhost:27017/")
db = client["markdown_db"]
collection = db["markdown_files"]

class MarkdownHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/convert":
            content_type, pdict = cgi.parse_header(self.headers.get("Content-Type"))
            if content_type == "multipart/form-data":
                pdict["boundary"] = bytes(pdict["boundary"], "utf-8")
                pdict["CONTENT-LENGTH"] = int(self.headers["Content-Length"])
                fields = cgi.parse_multipart(self.rfile, pdict)
                file_data = fields.get("file")[0]
                filename = fields.get("file-filename")[0]

                #temporarily save file
                filepath = os.path.join(UPLOAD_DIR, filename)
                with open(filepath, "wb") as f:
                    f.write(file_data)

                try:
                    #convert text to markdown
                    markdown_text = self.convert_to_markdown(filepath)
                    
                    #store in database
                    file_id = collection.insert_one({
                        "filename": filename,
                        "markdown": markdown_text
                    }).inserted_id

                    #send markdown and id response
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({
                        "markdown": markdown_text,
                        "file_id": str(file_id)
                    }).encode("utf-8"))
                except ValueError as e:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
                finally:
                    os.remove(filepath)
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error": "Invalid content type"}')
        else:
            self.send_response(404)
            self.end_headers()


    def convert_to_markdown(self, filepath):
        markdown_text = ""
        try:
            #create an instance of MarkItDown
            md = MarkItDown()
            
            #convert the file to Markdown
            result = md.convert(filepath)
            markdown_text = result.text_content
        except Exception as e:
            raise ValueError(f"Error converting file: {str(e)}")
        
        return markdown_text