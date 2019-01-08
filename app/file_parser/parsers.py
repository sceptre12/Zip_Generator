from os import path
from bs4 import BeautifulSoup

from configs.constants.generator_functions import generate_state_obj_list
from configs.constants.state_info import StateAcronyms
from models.zip_objects import ZipCode, StateInfo
from .zip_manager import ZipManager

state_dic = generate_state_obj_list()


def parse_file(file, file_data):
    zip_manager = ZipManager()
    state_acronym = StateAcronyms(path.basename(file).split(".")[0].upper())
    soup = BeautifulSoup(file_data, 'html5lib')
    state = state_dic[state_acronym.value]
    state_info = StateInfo(state)
    zip_rows = soup.select("div.panel.panel-default.panel-prefixes")[0].find_all("div", class_="list-group-item")

    for row in zip_rows:
        row_list = []
        is_zip = False;
        for col in row.find_all("div", class_="col-xs-12"):
            if col.find("a") and is_zip is False:
                row_list.append({
                    "zip": int(col.a.string),
                    "url": col.a['href']
                })
                is_zip = True
            else:
                for text in col.stripped_strings:
                    row_list.append(text)

        zip_code = ZipCode(row_list[0]["zip"], row_list[0]["url"], str(state), row_list[1], row_list[2],
                           row_list[3] if len(row_list) > 3 else "")
        zip_manager.add_zip(zip_code)
        state_info.add_zip(zip_code)
        zip_code.add_coords(30,50)

    zip_manager.add_state_info(state_info)





