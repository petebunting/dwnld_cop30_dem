import os

def download_http_files_use_lst_db(
    db_json: str,
    out_dir_path: str,
    username: str = None,
    password: str = None,
    use_wget: bool = False,
):
    """
    A function which uses the pysondb JSON database to download all the files
    recording whether files have been downloaded successful and the output
    path for the file.

    :param db_json: file path for the JSON db file.
    :param out_dir_path: the output path where data should be downloaded to.
    :param ftp_timeout: the timeout for the download. Default: 300 seconds.
    :param ftp_user: the username, if required, for the ftp server.
    :param ftp_pass: the password, if required, for the ftp server.
    :param create_dir_struct: boolean specifying whether the folder structure on the
                              ftp server should be maintained within the out_dir_path
                              (True) or ignored and all the individual files just
                              downloaded into the output directory as a flat
                              structure (False; Default).
    :param use_curl: boolean specifying whether to use CURL to download the files.
                     (Default: False).

    """
    import pysondb
    from rsgislib.tools.httptools import download_file_http, wget_download_file
    
    lst_db = pysondb.getDb(db_json)

    dwld_files = lst_db.getByQuery({"downloaded": False})

    for dwn_file in dwld_files:
        print(dwn_file["http_url"])
        filename = os.path.basename(dwn_file["http_url"])
        out_file_path = os.path.join(out_dir_path, filename)
        if use_wget:
            downloaded, out_message = wget_download_file(dwn_file["http_url"], out_file_path, username = username, password = password, try_number = 10, time_out = 60)
        else:
            downloaded = download_file_http(dwn_file["http_url"], out_file_path, username = username, password = password, no_except = True)
        
        if downloaded:
            lst_db.updateById(
                dwn_file["id"], {"lcl_path": out_file_path, "downloaded": True}
            )
        
        




download_http_files_use_lst_db(
    db_json="cop_dem_glo_30_urls_pydb.json",
    out_dir_path="../copernicus-dem-30m", use_wget=False)




   
"""        
        if create_dir_struct:
            dir_path = os.path.dirname(dwn_file["rmt_path"])
            if dir_path[0] == "/":
                dir_path = dir_path[1:]
            local_dir_path = os.path.join(out_dir_path, dir_path)
            if not os.path.exists(local_dir_path):
                os.makedirs(local_dir_path)
            local_path = os.path.join(local_dir_path, basename)
        else:
            local_path = os.path.join(out_dir_path, basename)
        if use_curl:
            dwnlded = download_curl_ftp_file(
                ftp_url=dwn_file["ftp_url"],
                remote_file=dwn_file["rmt_path"],
                local_file=local_path,
                ftp_timeout=ftp_timeout,
                ftp_user=ftp_user,
                ftp_pass=ftp_pass,
                print_info=False,
            )
        else:
            dwnlded = download_ftp_file(
                ftp_url=dwn_file["ftp_url"],
                remote_file=dwn_file["rmt_path"],
                local_file=local_path,
                ftp_timeout=ftp_timeout,
                ftp_user=ftp_user,
                ftp_pass=ftp_pass,
                print_info=False,
            )
        if dwnlded:
            lst_db.updateById(
                dwn_file["id"], {"lcl_path": local_path, "downloaded": True}
            )
            
"""
