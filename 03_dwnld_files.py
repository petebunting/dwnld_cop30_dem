import os
import argparse

def download_http_files_use_lst_db(
    db_json: str,
    out_dir_path: str,
    username: str = None,
    password: str = None,
    use_wget: bool = False,
    chk_out_file_exists: bool = False,
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
        out_file_exists = os.path.exists(out_file_path)
        
        if chk_out_file_exists and out_file_exists:
            continue
        
        if use_wget:
            downloaded, out_message = wget_download_file(dwn_file["http_url"], out_file_path, username = username, password = password, try_number = 10, time_out = 60)
        else:
            downloaded = download_file_http(dwn_file["http_url"], out_file_path, username = username, password = password, no_except = True)
        
        if downloaded:
            lst_db.updateById(
                dwn_file["id"], {"lcl_path": out_file_path, "downloaded": True}
            )
        
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True, help="Input file")
    parser.add_argument("-o", "--output", type=str, required=True, help="Output directory.")
    args = parser.parse_args()

    download_http_files_use_lst_db(
        db_json=args.input,
        out_dir_path=args.output, use_wget=False, chk_out_file_exists=False)
