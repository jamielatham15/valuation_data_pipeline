from data_fetcher import app as df
from data_loader import app as dl
from valuation_metrics import app as vm
from common.orm import truncate_table
import logging
import sys

from datetime import datetime
from pathlib import Path

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

# download data
filepath, download_date = df.download_data()
logger.info("data file downloaded: %s", str(filepath))

# filepath = Path("resources/data/Portfolio__1. Watchlist_Greenwald Valuation.csv")
# download_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# soft transform
filepath = dl.soft_transform(filepath, download_date)
logger.info("soft transform complete: %s", str(filepath))

# load data
truncate_table("staging")
s3_filename = dl.upload_file_to_s3(filepath)
logger.info("uploaded to s3: %s", str(s3_filename))

dl.upload_s3_to_staging(s3_filename)
logger.info("data ingestion to aws rds from s3 complete: %s", str(s3_filename))

# transform
truncate_table("valuations")
companies = vm.get_company_data()
logger.info("fetched company data for valuaitons")

vm.run_valuations(companies)
logger.info("valuations completed")