import csv
from pathlib import Path

import boto3
from sqlalchemy import text
from common.config import config
from common.orm import engine


def soft_transform(filepath: Path, date: str):
    out_filepath = str(filepath.with_suffix("")) + "_soft_transformed.csv"
    reader = csv.reader(open(str(filepath), "r", encoding="utf-8-sig"))
    writer = csv.writer(open(out_filepath, "w"))
    headers = next(reader)
    
    # rewrite headers to db schema
    # old_headers = next(reader)
    # new_headers = []
    # for c in old_headers:
    #     for k in config.data_schema.keys():
    #         if c == config.data_schema[k]["field"]:
    #             new_headers.append(k)
    # new_headers.append("date")
    # writer.writerow(new_headers)

    # rewrite data with date appended
    for row in reader:
        row[-1] = date
        writer.writerow(row)

    return Path(out_filepath)


def upload_file_to_s3(filepath: Path):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=config.aws_access_key,
        aws_secret_access_key=config.aws_secret_key,
    )
    s3.upload_file(str(filepath), config.aws_bucket_name, filepath.name)
    return filepath.name


def upload_s3_to_staging(filename: str):
    query = text(
        """ 
        SELECT
            aws_s3.table_import_from_s3(
                'staging',
                'ticker,"name",number_of_shares,current_assets,non_current_assets,current_liabilities,non_current_liabilities,total_equity,r_and_d,admin_expenses,tangibles,depreciation_and_amortization,turnover,operating_margin_5y_av,ebit_5y_av,tax_rate_paid_5y_av,non_current_assets_5_y_av,turnover_5y_av,turnover_perc_chg,borrowing,leases,debt,beta,cash,"close",capex_5y_av,r_and_d_5y_av,admin_expenses_5y_av,data_extract_date',
                '(format csv)',
                (SELECT
                    aws_commons.create_s3_uri(
                        'valuation-data-pipeline-bucket-1',
                        '{0}',
                        'us-east-1')
                )
            )
        """.format(filename)
    )
    with engine.connect() as conn:
        result = conn.execute(query)
        r = result.one()
        conn.commit()
    return r
