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

    table_name = None
    zip_obj = None

    # Checks to See if the params have been populated
    for key, value in kwargs.items():
        if key is "table_name":
            table_name = value
        if key is "zip_list":
            filtered_zip = list(filter(lambda item: int(item["zip_code"]) == zip_code, value))
            zip_obj = filtered_zip[0] if len(filtered_zip) == 1 else None

    if table_name is None or zip_obj is None:
        db_interface.insert("failed_zips", {"zip_code": zip_code, "issue": "html not part of zip_list"})
        return

    # Checks to ensure that this is a valid html file
    soup = BeautifulSoup(file_data, 'html5lib')

    # Checks to see if this is a failed zip retrieval
    if soup.find("meta") is None:
        db_interface.insert("failed_zips", {"zip_code": zip_code, "issue": "no html"})
        return

    # The html file contains a script tag that holds the zip coordinates
    script_list = soup.select("script")[1].string.strip().split(" ")

    geo_json = literal_eval((script_list[2][:len(script_list[2]) - 12]))

    polygon_type = geo_json['features'][0]['geometry']["type"]
    if polygon_type == "MultiPolygon":
        db_interface.insert("failed_zips", {"zip_code": zip_code, "issue": "MultiPolygon"})
        return

    zip_coords = geo_json['features'][0]['geometry']['coordinates'][0]

    coord_boundaries = script_list[4]

    # Gets Neighboring Zips
    neighboring_zips = []
    if soup.find(".nearby-zips-list"):
        neighboring_zips = list(map(lambda item: item.text.split(" ")[2], soup.select(".nearby-zips-list")[0].select("ul li div a")))

    communities_obj = Communities(zip_code,zip_coords);

    # Batch inserts communites
    db_interface.insert("communities",communities_obj.get_json())

    db_interface.insert("zip_codes",{
        "zip_code": zip_code,
        "state": zip_obj["state"].split(" ")[0],
        "state_abrv": zip_obj["state"].split(" ")[1],
        "city": zip_obj["city"],
        "county": zip_obj["county"],
        "zip_coords": zip_coords,
        "bordering_zips": neighboring_zips,
        "bounding_coords": coord_boundaries
    })

    # for index,community in enumerate(communities_obj.communities):
    #     print(communities_obj.tri.neighbors[index])
    #     print(community.get_json())
    #     quit()








