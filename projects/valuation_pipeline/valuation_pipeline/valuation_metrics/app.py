import logging

from sqlalchemy import func
from common.config import config
from common.orm import (Session, Staging, Valuations,
                                         orm_to_dict)
from valuation_metrics import greenwald
from valuation_metrics.data import DataTransformer

logger = logging.getLogger(__name__)

def get_company_data():
    with Session() as session:
        sub_q = session.query(func.max(Staging.upload_date))
        query = session.query(Staging)
        query = query.filter(
            Staging.upload_date == sub_q.as_scalar()
        )
        return [orm_to_dict(company) for company in query]

def run_valuations(companies: list):
    with Session() as session:
        while companies:
            company = companies.pop()
            company = DataTransformer(company)
            if not company.valid:
                logger.info("Cannot value %s, the following data is missing %s", company.data['name'], company.missing)
                continue
            try:
                value = greenwald.valuation(company.data)
                v = Valuations(**value)
                session.add(v)
            except ZeroDivisionError:
                logger.info("Cannot value %s, due to zero division error", company.data['name'])
        session.flush()
        session.commit()
