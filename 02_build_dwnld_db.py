import rsgislib.tools.utils
import tqdm
import pysondb
import math



cop_urls_lst = rsgislib.tools.utils.read_json_to_dict("cop_dem_glo_30_urls.json")

n_urls = len(cop_urls_lst)
print(n_urls)

n_urls_per_set = 2500


n_out_files = math.floor(n_urls/n_urls_per_set)


if (n_urls_per_set*n_out_files) < n_urls:
    n_out_files += 1

print(n_out_files)

db_data = []
n_file = 1
for cop_url in tqdm.tqdm(cop_urls_lst):
    db_data.append(
            {
                "http_url": cop_url["nativeDemUrl"],
                "lcl_path": "",
                "downloaded": False,
            }
        )
    
    if (len(db_data) % n_urls_per_set) == 0:
        db_json = f"cop_dem_glo_30_urls_pydb_{n_file}.json"
        lst_db = pysondb.getDb(db_json)
        lst_db.addMany(db_data)
        n_file += 1
        db_data = []

if len(db_data) > 0:
        db_json = f"cop_dem_glo_30_urls_pydb_{n_file}.json"
        lst_db = pysondb.getDb(db_json)
        lst_db.addMany(db_data)
        n_file += 1

