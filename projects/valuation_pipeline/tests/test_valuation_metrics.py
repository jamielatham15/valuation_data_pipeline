import sys
from pathlib import Path
import pandas as pd
import pytest
from random import randint

parent = Path(__file__).parents[1] / "valuation_data_pipeline"
sys.path.insert(0, str(parent))

from config import config
from orm import Session
from valuation_metrics.data import DataTransformer
from valuation_metrics.greenwald import valuation
from sqlalchemy import text

@pytest.fixture
def data():
    csv_data = pd.read_csv(config.greenwald) #, keep_default_na=False)
    return csv_data.to_dict(orient="records")

@pytest.fixture
def data_stack(data):
    stack = []
    for _dict in data:
        stack.append(DataTransformer(_dict))
    return stack

@pytest.fixture
def data_size(data):
    return len(data)

def test_data(data):
    assert len(data) > 0

def test_data_container(data, data_size):
    for i in range(10):
        assert DataTransformer(data[randint(0, data_size-1)])

def test_pop(data_stack):
    assert isinstance(data_stack.pop(), DataTransformer)

def test_data_transformer(data_stack):
    while data_stack:
        company = data_stack.pop()
        assert company.data

def test_greenwald_valuation(data_stack):
    while data_stack:
        company = data_stack.pop()
        per_share_valuation = valuation(company.data)
        print(f"Company: { company.data['name'] }, value per share: {per_share_valuation}" )

def test_db_connection():
    stmt = text("SELECT 1;")
    with Session() as s:
        result = s.execute(stmt)
        assert result.one() == (1,)






