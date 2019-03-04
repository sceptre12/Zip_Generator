from os import path
from bs4 import BeautifulSoup
from ast import literal_eval

from config.constants.state_info import StateAcronyms, StateName
from models.state_html_models import ZipCode, StateInfo, State
from models.zip_html_models import Communities
from models import ZipManager
from db_storage.db_interface import DbModule


def generate_state_obj_list():
    state_name_list = list(StateName.__members__)
    state_acronym_list = list(StateAcronyms.__members__)
    state_list = {}

    for idx, val in enumerate(state_acronym_list):
        state_list[val] = State(state_name_list[idx],state_acronym_list[idx])
    return state_list


state_dic = generate_state_obj_list()


def state_file_parser(file, file_data):
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

    zip_manager.add_state_info(state_info)


def zip_file_parser(file,file_data,**kwargs):
    db_interface = DbModule()

    zip_code = int(path.basename(file).split(".")[0])
    soup = BeautifulSoup(file_data, 'html5lib')

    # Checks to see if this is a failed zip retrevial
    if soup.find("meta") is None:
        db_interface.insert("failed_zips",zip_code)

    table_name = None
    zip_obj = None

    for key, value in kwargs.items():
        if key is "table_name":
            table_name = value
        if key is "zip_list":
            zip_obj = list(filter(lambda zip: int(zip["zip_code"]) == zip_code, value))[0]

    if table_name is None and zip_obj is None: return None

    # The html file contains a script tag that holds the zip coordinates
    script_list = soup.select("script")[1].string.strip().split(" ")

    geo_json = literal_eval((script_list[2][:len(script_list[2]) - 12]))

    zip_coords = geo_json['features'][0]['geometry']['coordinates'][0]

    coord_boundaries = script_list[4]

    # Gets Neighboring Zips
    neighboring_zips = list(map(lambda item: item.text.split(" ")[2], soup.select(".nearby-zips-list")[0].select("ul li div a")))

    # Batch inserts communites
    # db_interface.insert("communities",Communities(zip_code,zip_coords).get_json())
    #
    # db_interface.insert("zip_codes",{
    #     "zip_code": zip_obj['zip_code'],
    #     "state": zip_obj["state"].split(" ")[0],
    #     "state_abrv": zip_obj["state"].split(" ")[1],
    #     "city": zip_obj["city"],
    #     "county": zip_obj["county"],
    #     "bordering_zips": neighboring_zips,
    #     "bounding_coords": coord_boundaries
    # })






