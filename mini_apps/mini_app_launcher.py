import sys
sys.path.insert(0,'/Users/xavierthomas/pythonProjects/GenerateData')

from file_parser.parsers import zip_file_parser

with open("/Users/xavierthomas/client_storage/zip_html/20674.html", 'r') as f:
    zip_file_parser("20674.html", f.read())

