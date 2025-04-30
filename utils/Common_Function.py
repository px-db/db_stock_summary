import pandas as pd
import os
import json
import subprocess
import sqlite3
import json
from pathlib import Path
import xmltodict
import psutil
if os.name == 'nt' :
   import win32api
   import win32net
   import win32netcon
import string
from datetime import datetime


def mid(text:str, start_pos:int, length:int):
  """
  Posisi dimulai dari 1
  """
  # Pastikan start_pos dan length adalah bilangan bulat yang valid
  if not isinstance(start_pos, int) or not isinstance(length, int):
      raise ValueError("Start position and length must be integers")
  
  # Periksa apakah start_pos valid dan tidak melebihi panjang string
  if start_pos < 0 or start_pos >= len(text):
      raise ValueError("Invalid start position")
  
  # Ambil substring dari string berdasarkan posisi dan panjang
  start_pos -= 1
  return text[start_pos:start_pos+length]

def parse_string(input_string, start_pos, length):
  """
  Posisi dimulai dari 0
  """
  # Pastikan start_pos dan length adalah bilangan bulat yang valid
  if not isinstance(start_pos, int) or not isinstance(length, int):
      raise ValueError("Start position and length must be integers")
  
  # Periksa apakah start_pos valid dan tidak melebihi panjang string
  if start_pos < 0 or start_pos >= len(input_string):
      raise ValueError("Invalid start position")
  
  # Ambil substring dari string berdasarkan posisi dan panjang
  return input_string[start_pos:start_pos + length]

def scan_file_in_dir(directory)->list:
  """
  Scan file di dalam direktori tidak termasuk sub direktori
  """
  # Konversi ke Path object
  directory = Path(directory)
  
  # Periksa apakah direktori valid
  if not directory.is_dir():
      raise ValueError("Invalid directory")
  
  # Minta list nama file dalam direktori
  files = [str(f) for f in directory.iterdir() if f.is_file()]
  
  # Kembalikan list nama file
  return files

def scan_dir_and_subdir(directory)->list:
  """
  Scan file dan sub direktori
  """
  # Konversi ke Path object
  directory = Path(directory)
  
  # Periksa apakah direktori valid
  if not directory.is_dir():
      raise ValueError("Invalid directory")
  
  # List untuk menyimpan semua nama file
  all_files = []
  
  # Lakukan pemindaian untuk setiap item dalam direktori
  for item in directory.rglob('*'):
      if item.is_file():
          all_files.append(str(item))
  
  return all_files

def file_exists(file_path):
  """
  Cek apakah file ada. return 'True' atau 'False'
  """
  return Path(file_path).exists()

def convert_xlsx_to_csv(file_xlsx, file_csv=None):
  """
  Proses konversi xlsx ke csv.
  """
  # Read xlsx and convert csv
  if file_csv :
    pd.read_excel(file_xlsx).to_csv(file_csv, index=False)
  else :
    pd.read_excel(file_xlsx).to_csv(f'{file_xlsx}.csv', index=False)
  return None

def convert_hexa_to_bitlist(hexa):
  '''
  Fungsi ini untuk konversi hexa dalam string menjadi bit dalam list
  dengan urutan Low Significant Bit (LSB) terlebih dahulu.

  Contoh :
  'A' = 1010 ; return [0,1,0,1]

  Parameter :
    hexa:str
  
  return : list
  '''
  # convert to bit
  bit = bin(int(hexa,16))
  len_x = len(str(bit)[2:])

  # add padding in front
  pad = '0'*(32-len_x)+str(bit)[2:]

  # list in reverse list
  return list(pad)[::-1]

def key_in_dict(key_to_check, dict_to_test:dict):
  '''
  Cek apakah value 'key_to_check' ada di dalam key dictionary 'dict_to_test'
  '''
  if key_to_check in dict_to_test.keys() :
    return True
  return False

def in_list(test, list_to_test):
  '''
  Cek apakah value 'test' ada di dalam list 'list_to_test'
  '''
  if test in list_to_test :
    return True
  return False

def curl(curl):
  return subprocess.run(
      curl.split(),
      capture_output=True,
      text=True
      ).stdout

def join_list(list_name:list, sep=","):
  return sep.join(map(str,list_name))

def print_list(list_name):
  for i in list_name :
    print(i)
  return None

def print_dict(dict_name):
  for key, value in dict_name.items():
    print(key, ":", value)
  return None

def string_to_json(json_string):
  """
  Konversi string json ke dict
  """
  return json.loads(json_string)

def json_to_string(py_dict):
  """
  Konveri dict ke string json
  """
  return json.dumps(py_dict)

def list_to_sqlite(db_name:str, data_list:list, columns:list, table_name:str)->None:
  """
  Parameter :
    db_name : nama database (string)
    data_list : data dalam list
    columns : kolom table
      columns = [
          ('ID', 'INTEGER PRIMARY KEY'),
          ('Name', 'TEXT'),
          ('Age', 'INTEGER')
      ]
    table_name : nama tabel (string)

  """
  # Koneksikan ke database SQLite (atau buat database baru jika belum ada)
  conn = sqlite3.connect(db_name)
  
  # Buat cursor objek
  cursor = conn.cursor()

  columns_with_types = ', '.join([f'{col_name} {col_type}' for col_name, col_type in columns])
  create_table_sql = f'CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types})'
  # Buat tabel jika belum ada
  cursor.execute(create_table_sql)
  # Simpan perubahan

  # Masukkan data ke dalam tabel
  insert_sql = f'INSERT INTO {table_name} ({", ".join([col_name for col_name, _ in columns])}) VALUES ({", ".join(["?" for _ in columns])})'
  cursor.executemany(insert_sql, data_list)

  conn.commit()
  
  # Tutup koneksi
  conn.close()

def join_list(data_list)->str:
   return ", ".join([col_name for col_name, _ in data_list])

def file_list(files:list, extensions:list)->list:
  # Filter file dengan ekstensi tertentu
  return [file for file in files if any(file.endswith(ext) for ext in extensions)]

def write_file(file_name, content, mode:str='w'):
  r"""
  mode :
    w = write (menimpa\mengganti)
    a = append (menambah)
  """  
  with open(file_name, mode) as file:
      file.write(content)
  
  return 0

def make_dirs(folder_name):
  """
  Make dir recursive
  """
  Path(folder_name).mkdir(parents=True, exist_ok=True)

def make_dir(folder_name):
  """
  make dir single
  """
  Path(folder_name).mkdir(exist_ok=True)

def list_dir(dir_path):
  """
  List dir tanpa file
  """  
  # Konversi ke Path object
  dir_path = Path(dir_path)
  
  # Mendapatkan daftar isi direktori
  return [str(d) for d in dir_path.iterdir() if d.is_dir()]

def list_dir_recursive(root_dir):
  directories = []
  root_dir = Path(root_dir)
  for dirpath in root_dir.rglob('*'):
    if dirpath.is_dir():
      directories.append(str(dirpath))
  return directories

def remove_string(path_string, text_to_remove):
  # Menghapus string
  return path_string.replace(text_to_remove, "", 1)


def csv_to_dataframe(path_file):
    # Mencoba membaca file dengan encoding yang berbeda
    encodings = ['utf-8', 'utf-16', 'latin-1', 'ascii']  # Daftar encoding yang dicoba
    for enc in encodings:
        try:
            df = pd.read_csv(path_file, encoding=enc)  # Menggunakan read_csv untuk memuat data CSV
            return df
        except (UnicodeDecodeError, pd.errors.ParserError):
            continue  # Coba encoding berikutnya
    raise ValueError("Tidak dapat membaca file CSV dengan encoding yang tersedia.")

def load_json(path_file):
    # Mencoba membaca file dengan encoding yang berbeda
    encodings = ['utf-8', 'utf-16', 'latin-1', 'ascii']  # Daftar encoding yang dicoba
    for enc in encodings:
        try:
            with open(path_file, 'r', encoding=enc) as file:
                data = json.load(file)
            return data
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue  # Coba encoding berikutnya
    raise ValueError("Tidak dapat membaca file JSON dengan encoding yang tersedia.")

def path_join(list_path_file:list)->str:
    return str(Path(*list_path_file))

def json_to_dataframe(path_file: str) -> pd.DataFrame:
    """
    Memuat data JSON dari file dan mengonversinya menjadi DataFrame.

    Args:
        path_file (str): Path ke file JSON.

    Returns:
        pd.DataFrame: DataFrame yang berisi data dari file JSON.

    Raises:
        ValueError: Jika terjadi kesalahan saat memuat data JSON.
    """
    try:
        # Memuat data JSON
        data = load_json(path_file)  # Pastikan Anda memiliki fungsi load_json yang sudah didefinisikan
        
        # Mengonversi data JSON menjadi DataFrame
        df = pd.json_normalize(data)  # Menggunakan json_normalize untuk mengonversi nested JSON
        return df
    
    except FileNotFoundError:
        print(f"Error: File '{path_file}' tidak ditemukan.")
        return pd.DataFrame()  # Mengembalikan DataFrame kosong jika file tidak ditemukan
    except json.JSONDecodeError:
        print(f"Error: File '{path_file}' tidak berisi data JSON yang valid.")
        return pd.DataFrame()  # Mengembalikan DataFrame kosong jika JSON tidak valid
    except Exception as e:
        print(f"Error tak terduga saat memuat file JSON '{path_file}': {e}")
        return pd.DataFrame()  # Mengembalikan DataFrame kosong untuk kesalahan lainnya

def dataframe_to_json(df: pd.DataFrame, json_file_path: str) -> None:
    """
    Mengonversi DataFrame ke file JSON.

    Args:
        df (pd.DataFrame): DataFrame yang akan dikonversi.
        json_file_path (str): Path ke file JSON untuk menyimpan hasil konversi.
    """
    try:
        # Menyimpan DataFrame ke file JSON
        df.to_json(json_file_path, orient='records')
        print(f"File JSON berhasil disimpan di: '{json_file_path}'")
    except Exception as e:
        print(f"Error saat menyimpan DataFrame ke file JSON '{json_file_path}': {e}")

def json_to_dict(file_path, encoding='utf-8'):
    """
    Memuat data JSON dari file.
    
    Args:
        file_path (str): Path ke file JSON.
        
    Returns:
        dict: Data JSON dalam bentuk dictionary jika berhasil.
        None: Jika terjadi error saat memuat file.
    """
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' tidak ditemukan.")
    except json.JSONDecodeError:
        print(f"Error: File '{file_path}' tidak berisi data JSON yang valid.")
    except Exception as e:
        print(f"Error tak terduga: {e}")
    return None


def dict_to_dataframe(data_dict):
    # Mengonversi dictionary menjadi DataFrame
    df = pd.DataFrame.from_dict(data_dict)  # Menggunakan from_dict untuk mengonversi dictionary
    return df

def list_excel_sheets(path_file):
    # Membaca file Excel dan mendapatkan daftar sheet
    xls = pd.ExcelFile(path_file)  # Membuka file Excel
    return xls.sheet_names  # Mengembalikan daftar nama sheet

def scan_file_with_extension(path_file,extension='xml'):
    list_files =[]
    path_file = Path(path_file).resolve()
    for files in path_file.rglob(f'*.{extension}'):
        # Memisahkan path dan nama file
        file_path = str(files.parent)  # Path
        file_name = str(files.name)    # Nama file
        if not file_name.startswith("~$"):  # Mengabaikan file yang namanya diawali dengan "~"
            list_files.append((file_path, file_name))  # Menyimpan sebagai tuple
    return list_files

def load_xml(path_file):
    # Mencoba membaca file dengan encoding yang berbeda
    encodings = ['utf-8', 'utf-16', 'latin-1','ascii']  # Daftar encoding yang dicoba
    for enc in encodings:
        try:
            with open(path_file, 'r', encoding=enc) as file:
                my_xml = file.read()
            return my_xml
        except UnicodeDecodeError:
            continue  # Coba encoding berikutnya
    raise ValueError("Tidak dapat membaca file dengan encoding yang tersedia.")

def xml_to_dict(xml_string):
    return xmltodict.parse(xml_string)

def dict_to_json(dict_data, indent=2):
    return json.dumps(dict_data,indent)

def save_dict_to_file_json(data_dict, file_name='file_json',path_save=None, indent=2):
    # Menyimpan dictionary ke file JSON
    path_file_name = os.path.join(path_save,file_name)
    with open(f'{path_file_name}.json', 'w', encoding='utf-8') as json_file:
        json.dump(data_dict, json_file, ensure_ascii=False, indent=indent)

def create_directory_if_not_exists(path):
    # Konversi ke Path object
    path = Path(path)
    # Memeriksa apakah folder sudah ada
    if not path.exists():
        # Jika tidak ada, buat folder dan subfolder
        path.mkdir(parents=True, exist_ok=True)
        return True
    return True

def generate_all_xml_to_file_json(source_list_path_and_files,root_source,root_dest,suffix_file=None):
    xml_string = ''
    for i in source_list_path_and_files :
        xml_dicts = xml_to_dict(load_xml(os.path.join(*i)))
        path_dest = i[0].replace(root_source, root_dest)
        file_name = i[1]
        create_directory_if_not_exists(path_dest)
        if suffix_file :
            save_dict_to_file_json(data_dict = xml_dicts,path_save=path_dest,file_name=f'{file_name}{suffix_file}')
            print(f'{path_dest}:{file_name+suffix_file}.json')
        else:
            save_dict_to_file_json(data_dict = xml_dicts,path_save=path_dest,file_name=file_name)
            print(f'{path_dest}:{file_name}.json')

def get_active_drives():
    drives = []
    for drive in range(65, 91):  # ASCII A-Z
        drive_letter = f"{chr(drive)}:\\"
        if os.path.exists(drive_letter):
            drives.append(drive_letter)
    return drives

if os.name == 'nt':  # Windows
    def map_network_drive(drive_letter, network_path, username=None, password=None):
        """Memetakan drive jaringan ke drive kosong."""
        try:
            # Lepas drive jika sudah ada
            win32net.NetUseDel(None, drive_letter, win32netcon.USE_FORCE)
        except Exception:
            pass  # Abaikan jika drive tidak terhubung sebelumnya
    
        try:
            # Mapping drive ke lokasi jaringan
            use_info = {
                "remote": network_path,
                "local": drive_letter,
                "password": password,
                "username": username,
                "asg_type": win32netcon.USE_DISK,
            }
            win32net.NetUseAdd(None, 2, use_info)
            print(f"Drive {drive_letter} berhasil dimapping ke {network_path}")
        except Exception as e:
            print(f"Gagal memapping drive {drive_letter}: {e}")


def get_inactive_drives():
    """
    Mendapatkan daftar huruf drive yang tidak aktif (tidak digunakan),
    dimulai dari Z hingga E.
    """
    # Urutan huruf drive dari Z ke E
    all_drives = [f"{chr(drive)}:\\" for drive in range(90, 68, -1)]  # Z hingga E (ASCII 90 ke 69)
    
    # Dapatkan drive yang aktif
    active_drives = [f"{chr(drive)}:\\" for drive in range(65, 91) if os.path.exists(f"{chr(drive)}:\\")]

    # Cari drive yang tidak aktif
    inactive_drives = [drive for drive in all_drives if drive not in active_drives]
    return inactive_drives

def get_current_path():
    """
    Mengembalikan path direktori kerja saat ini.
    """
    return str(Path.cwd())  # Mendapatkan current working directory


def generate_credentials_file(file_path:None):
    """
    Menghasilkan file credential dengan format "user=" dan "pass=".
    
    Args:
        file_path (str): Path ke file credential yang akan dibuat.
    """
    if not file_path : 
        file_path = Path.cwd() / 'credentail'
    else:
        file_path = Path(file_path)

    with open(file_path, 'w') as file:
        file.write("user=\n")
        file.write("pass=\n")
    print(f"File credential telah dibuat di: {file_path}")

def load_credentials(file_path):
    """
    Memuat file credential dan mengembalikan username dan password.

    Args:
        file_path (str): Path ke file credential.

    Returns:
        dict: Dictionary berisi username dan password, atau None jika terjadi kesalahan.
    """
    credentials = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Hilangkan spasi dan baris kosong
                line = line.strip()
                if line and "=" in line and not line.startswith("#"):  # Abaikan baris komentar
                    key, value = line.split("=", 1)  # Pisahkan berdasarkan "="
                    credentials[key.strip()] = value.strip()
        return credentials
    except FileNotFoundError:
        print(f"File {file_path} tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi kesalahan saat membaca file: {e}")
    return None

def is_linux():
    if os.name == 'posix':
        return True
    return False

def is_Windows():
    if os.name == 'nt':
        return True
    return False

# Mapping untuk Linux
def mount_samba_with_credentials(server, share='l$/TCPLogging/', cred_file='.smsCredentials'):        
    # Cek mapping apakah sudah ada, jika ada tidak perlu buat mapping.
    if check_gvfs_path_exists(server) : return True
    try:
        smb_url = f"smb://{server}/{share}"
        subprocess.run(["gio", "mount", smb_url, f"--credentials={cred_file}"], check=True)
        return f"{smb_url}"
    except subprocess.CalledProcessError as e:
        print(f"Error mounting {smb_url}: {e}")

def check_gvfs_path_exists(server, share='l$/TCPLogging/',):
    path = f"/run/user/1003/gvfs/smb-share:server={server},share={share}"
    try:
        if os.path.exists(path):
            return True
        else:
            print(f"Path '{path}' tidak ditemukan.")
            return False
    except Exception as e:
        print(f"Kesalahan saat memeriksa path: {e}")
        return False
    
def check_path_exists(path):
    if os.path.exists(path):
        return True
    else:
        print(f"Path '{path}' tidak ditemukan.")
        return False
    
def query_sqlite_to_df(database_sqlite,query):
    with sqlite3.connect(database_sqlite) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        df = pd.read_sql(query, conn)
        return df

def query_sqlite_to_list(database_sqlite, query):
    with sqlite3.connect(database_sqlite) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        df = pd.read_sql(query, conn)
        return df.to_dict(orient='records')  # Convert DataFrame to list
    
    
def list_sqlite_tables(database_sqlite):
    """
    Mengembalikan daftar nama tabel dalam database SQLite.
    """
    with sqlite3.connect(database_sqlite) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()  # Mengambil semua nama tabel
    return [table[0] for table in tables]  # Mengembalikan daftar nama tabel

def list_columns_in_table_sqlite(database_sqlite, table_name):
    """
    Mengembalikan daftar nama kolom dalam tabel SQLite.
    
    Args:
        database_sqlite (str): Nama database SQLite.
        table_name (str): Nama tabel yang ingin diperiksa.
    
    Returns:
        list: Daftar nama kolom dalam tabel.
    """
    with sqlite3.connect(database_sqlite) as conn:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()  # Mengambil informasi kolom
    return [column[1] for column in columns]  # Mengembalikan daftar nama kolom

def save_dataframe_to_excel(df, file_name, sheet_name='Sheet1', index=False):
    """
    Menyimpan DataFrame ke file Excel.

    Args:
        df (pd.DataFrame): DataFrame yang ingin disimpan.
        file_name (str): Nama file Excel untuk menyimpan DataFrame.
        sheet_name (str): Nama sheet dalam file Excel (default: 'Sheet1').
        index (bool): Apakah menyertakan indeks DataFrame (default: False).
    """
    df.to_excel(file_name, sheet_name=sheet_name, index=index)

def save_dataframe_to_csv(df, file_name, index=False):
    """
    Menyimpan DataFrame ke file CSV.

    Args:
        df (pd.DataFrame): DataFrame yang ingin disimpan.
        file_name (str): Nama file CSV untuk menyimpan DataFrame.
        index (bool): Apakah menyertakan indeks DataFrame (default: False).
    """
    df.to_csv(file_name, index=index)


def excel_to_dataframe(filePath: str,
                       sheet:str,
                       cols = 'A:J',
                       column = None,
                       skip_rows = 0,
                       header = 0
                       ) -> pd.DataFrame:
    """
    Mengonversi file Excel ke DataFrame, mulai dari baris ke-n hingga menemukan string "endtype"
    pada kolom "type" atau kolom "C".

    Args:
        file_path (str): Path ke file Excel.

    Returns:
        pd.DataFrame: DataFrame yang berisi data yang diambil.
    """
    try:
        df = pd.read_excel(filePath,
                       sheet_name=sheet, 
                       usecols=cols, 
                       names=column,
                       skiprows=skip_rows,
                       header=header)
        
    except ValueError:
        raise ValueError(f"Sheet '{sheet}' tidak ditemukan dalam file Excel.")


    # Menemukan indeks baris di mana kolom "type" atau kolom "C" berisi "endtype"
    #endtype_index = df[(df['type'] == 'endtype') | (df['C'] == 'endtype')].index

    # Jika ditemukan, ambil data hingga baris tersebut
    #if not endtype_index.empty:
    #    df = df.loc[:endtype_index[0]]

    return df

def excel_to_sqlite(file_path: str, db_name: str, table_name: str, sheet_name: str = None) -> None:
    """
    Mengonversi data dari file Excel ke database SQLite.

    Args:
        file_path (str): Path ke file Excel.
        db_name (str): Nama database SQLite.
        table_name (str): Nama tabel untuk menyimpan data.
        sheet_name (str, optional): Nama sheet dalam file Excel. Jika None, sheet pertama akan digunakan.
    """
    # Membaca data dari file Excel
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # Koneksikan ke database SQLite (atau buat database baru jika belum ada)
    with sqlite3.connect(db_name) as conn:
        # Simpan DataFrame ke dalam tabel SQLite
        df.to_sql(table_name, conn, if_exists='replace', index=False)

    # Koneksi akan otomatis ditutup di sini

def add_column_and_update(db_name, table_name, column_name, column_type, default_value):
    conn = None
    try:
        # Koneksi ke database SQLite
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # Tambahkan kolom baru
        alter_query = f"""
        ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type};
        """
        cursor.execute(alter_query)
        
        # Perbarui nilai kolom baru untuk semua baris
        update_query = f"""
        UPDATE {table_name} SET {column_name} = ?;
        """
        cursor.execute(update_query, (default_value,))
        
        # Simpan perubahan dan tutup koneksi
        conn.commit()
        print(f"Kolom '{column_name}' berhasil ditambahkan dan diperbarui dengan nilai '{default_value}'")
    except sqlite3.Error as e:
        print("Terjadi kesalahan:", e)
    finally:
        if conn:
            conn.close()

def merge_tables(db_name: str, table1: str, table2: str, key_column: str, new_table_name: str) -> None:
    """
    Menggabungkan dua tabel dalam database SQLite berdasarkan kolom kunci.

    Args:
        db_name (str): Nama database SQLite.
        table1 (str): Nama tabel pertama.
        table2 (str): Nama tabel kedua.
        key_column (str): Nama kolom kunci untuk penggabungan.
        new_table_name (str): Nama tabel baru untuk menyimpan hasil penggabungan.
    """
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        
        # Buat query untuk menggabungkan tabel
        merge_query = f"""
        CREATE TABLE {new_table_name} AS
        SELECT *
        FROM {table1}
        LEFT JOIN {table2} ON {table1}.{key_column} = {table2}.{key_column};
        """
        
        cursor.execute(merge_query)
        print(f"Tabel '{new_table_name}' berhasil dibuat dengan hasil penggabungan dari '{table1}' dan '{table2}'.")

def merge_databases(source_db: str, target_db: str) -> None:
    """
    Menggabungkan dua database SQLite dengan menyalin semua tabel dari database sumber ke database target.

    Args:
        source_db (str): Nama database sumber.
        target_db (str): Nama database target.
    """
    with sqlite3.connect(source_db) as source_conn, sqlite3.connect(target_db) as target_conn:
        source_cursor = source_conn.cursor()
        target_cursor = target_conn.cursor()

        # Ambil daftar tabel dari database sumber
        source_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = source_cursor.fetchall()

        for table in tables:
            table_name = table[0]
            # Ambil semua data dari tabel
            source_cursor.execute(f"SELECT * FROM {table_name};")
            rows = source_cursor.fetchall()

            # Ambil nama kolom dari tabel
            source_cursor.execute(f"PRAGMA table_info({table_name});")
            columns = [column[1] for column in source_cursor.fetchall()]

            # Buat tabel di database target jika belum ada
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"
            target_cursor.execute(create_table_query)

            # Masukkan data ke dalam tabel di database target
            insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['?' for _ in columns])});"
            target_cursor.executemany(insert_query, rows)

        target_conn.commit()
        print(f"Semua tabel dari '{source_db}' berhasil digabungkan ke '{target_db}'.")

def copy_table_structure(source_db: str, target_db: str, table_name: str) -> None:
    """
    Menyalin struktur tabel dari database sumber ke database target.

    Args:
        source_db (str): Nama database sumber.
        target_db (str): Nama database target.
        table_name (str): Nama tabel yang akan disalin strukturnya.
    """
    with sqlite3.connect(source_db) as conn_lama, sqlite3.connect(target_db) as conn_baru:
        cursor_lama = conn_lama.cursor()
        cursor_baru = conn_baru.cursor()

        try:
            # 1. Mendapatkan struktur tabel dari database lama
            cursor_lama.execute(f'PRAGMA table_info({table_name});')
            columns = cursor_lama.fetchall()

            # 2. Membuat tabel baru di database baru dengan struktur yang sama
            column_definitions = ", ".join([f"{col[1]} {col[2]}" for col in columns])  # Mengambil nama kolom dan tipe datanya
            cursor_baru.execute(f'''
                CREATE TABLE IF NOT EXISTS {table_name} (
                    {column_definitions}
                );
            ''')

            # Commit perubahan
            conn_baru.commit()
            print("Tabel baru dengan struktur yang sama telah dibuat di database baru!")

        except sqlite3.Error as e:
            print(f"Terjadi kesalahan: {e}")

def csv_to_json(csv_file_path: str, json_file_path: str) -> None:
    """
    Mengonversi file CSV ke file JSON.

    Args:
        csv_file_path (str): Path ke file CSV yang akan dikonversi.
        json_file_path (str): Path ke file JSON untuk menyimpan hasil konversi.
    """
    try:
        # Membaca file CSV
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        print(f"Error: File '{csv_file_path}' tidak ditemukan.")
        return
    except pd.errors.EmptyDataError:
        print(f"Error: File '{csv_file_path}' kosong.")
        return
    except pd.errors.ParserError:
        print(f"Error: Terjadi kesalahan saat mem-parsing file '{csv_file_path}'.")
        return
    except Exception as e:
        print(f"Error tak terduga saat membaca file '{csv_file_path}': {e}")
        return

    try:
        # Menyimpan DataFrame ke file JSON
        df.to_json(json_file_path, orient='records', lines=True)
        print(f"File JSON berhasil disimpan di: '{json_file_path}'")
    except Exception as e:
        print(f"Error saat menyimpan file JSON ke '{json_file_path}': {e}")

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

def get_current_year():
    return datetime.now().year