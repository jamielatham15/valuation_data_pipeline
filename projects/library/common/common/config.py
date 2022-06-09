import platform
import os
import yaml

from pathlib import Path


class MarketAssumptions:
    # https://pages.stern.nyu.edu/~adamodar/
    # Cost of Equity and Capital (US)
    cost_of_debt = 0.0358
    # Implied Equity Risk Premium
    equity_risk_premium = 0.0517
    # Tax Rates By Sector (US) (Average across only money-making companies)
    average_tax_rate = 0.178
    # https://www.cnbc.com/quotes/US10Y
    risk_free_rate = 0.03014


class DevConfig:
    def __init__(self):
        # files and folders
        self.download_dir = "/tmp/data/"
        self.screenshot_dir = "/tmp/screenshots/"
        self.data_schema = self.load_schema(str(Path(__file__).parent) + "/schema.yml")

        # dev data
        self.greenwald = (
            "resources/data/Portfolio__1. Watchlist_Greenwald Valuation.csv"
        )
        self.rule_one = (
            "resources/data/Portfolio__1. Watchlist_Rule One Valuation Project.csv"
        )

        # sqlalchemy & flask
        self.pg_host = os.getenv("AWS_RDS_HOST")
        self.pg_user = os.getenv("AWS_RDS_USER")
        self.pg_password = os.getenv("AWS_RDS_PASSWORD")
        self.debug = False
        self.SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{self.pg_user}:{self.pg_password}@{self.pg_host}:5432/valuation_db"
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False

        # aws
        self.aws_access_key = os.getenv("AWS_ACCESS_KEY")
        self.aws_secret_key = os.getenv("AWS_SECRET_KEY")
        self.aws_bucket_name = os.getenv("AWS_BUCKET_NAME")
        self.aws_account_id = os.getenv("AWS_ACCOUNT_ID")

    def load_schema(self, filepath: str):
        with open(filepath, "r") as f:
            return yaml.safe_load(f)["raw_data"]


config = DevConfig()
