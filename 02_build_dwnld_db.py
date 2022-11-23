import rsgislib.tools.utils
import tqdm
import pysondb

db_json = "cop_dem_glo_30_urls_pydb.json"

cop_urls_lst = rsgislib.tools.utils.read_json_to_dict("cop_dem_glo_30_urls.json")

lst_db = pysondb.getDb(db_json)
db_data = []
for cop_url in tqdm.tqdm(cop_urls_lst):
    db_data.append(
            {
                "http_url": cop_url["nativeDemUrl"],
                "lcl_path": "",
                "downloaded": False,
            }
        )
    
if len(db_data) > 0:
    lst_db.addMany(db_data)


