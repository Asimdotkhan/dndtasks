import os
import tempfile
import pantab
import pyreadr
import pyreadstat
import pandas as pd

def convert_file(file, file_type, convert_to):
    if file and file.filename.endswith(('.RDS', '.txt', '.sav', '.csv')):
        temp_dir = tempfile.mkdtemp()

        file_extension = os.path.splitext(file.filename)[1]
        file_path = os.path.join(temp_dir, file.filename)
        file.save(file_path)

        if file_extension == '.RDS':
            result = pyreadr.read_r(file_path)
            df = result[None].convert_dtypes()
        elif file_extension == '.txt':
            df = pd.read_csv(file_path, sep='|')
        elif file_extension == '.sav':
            df, meta = pyreadstat.read_sav(file_path)
        elif file_extension == '.csv':
            df = pd.read_csv(file_path, low_memory=False)

        df = df.astype(str)

        if convert_to == '.hyper' or (file_extension == '.csv' and convert_to == '.csv'):
            hyper_filename = os.path.splitext(file.filename)[0] + '.hyper'
            hyper_file_path = os.path.join(temp_dir, hyper_filename)

            pantab.frame_to_hyper(df, hyper_file_path, table="the_table")

            os.remove(file_path)
            return hyper_file_path
        elif convert_to == '.csv':
            csv_filename = os.path.splitext(file.filename)[0] + '.csv'
            csv_file_path = os.path.join(temp_dir, csv_filename)

            df.to_csv(csv_file_path, index=False)

            os.remove(file_path)
            return csv_file_path
    return None
