import sys
sys.path.insert(0,'/Users/xavierthomas/pythonProjects/GenerateData')

from file_parser.parsers import zip_file_parser

with open("/Users/xavierthomas/client_storage/zip_html/20674.html", 'r') as f:
    zip_file_parser("20674.html", f.read(),table_name="x1_table",zip_list=[
        {
            "bordering_zips": [ ],
            "city":  "Sun Valley, Elk Horn" ,
            "coordinates": {
            "lat": 30 ,
            "long": 50
            } ,
            "county":  "Blaine County" ,
            "id":  "0045c447-09c9-4e4b-8e10-3ebad8f1ad36" ,
            "link": "https://www.unitedstateszipcodes.org/83354/",
            "state":  "Idaho ID" ,
            "zip_code": 83354 ,
            "zip_type":  "PO Box"
        },
        {
            "bordering_zips": [],
            "city": "Huntington",
            "coordinates": {
                "lat": 30,
                "long": 50
            },
            "county": "Cabell County",
            "id": "003b3b8d-08ae-4976-9bc1-d2d5c2747d71",
            "link": "https: // www.unitedstateszipcodes.org / 25728 /",
            "state": "West_Virginia WV",
            "zip_code": 25728,
            "zip_type": "PO Box"
        },
        {
            "bordering_zips": [],
            "city": "Piney Point",
            "coordinates": {
                "lat": 30,
                "long": 50
            },
            "county": "St. Mary's County",
            "id": "1b806a44-ec5c-4b7b-bfa0-a9595cfed020",
            "link": "https: // www.unitedstateszipcodes.org / 20674 /",
            "state": "Maryland MD",
            "zip_code": 20674,
            "zip_type": "Standard"
        }
    ])

