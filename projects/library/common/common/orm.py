from sqlalchemy import create_engine, Column, Integer, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from common.config import config

Base = automap_base()


class Valuations(Base):
    __tablename__ = "valuations"
    id = Column("id", Integer, primary_key=True)


class Staging(Base):
    __tablename__ = "staging"
    id = Column("id", Integer, primary_key=True)


def orm_to_dict(query_obj):
    d = query_obj.__dict__
    d.pop("_sa_instance_state")
    return d


def truncate_table(tablename: str):
    with engine.connect() as conn:
        trunc = text("truncate table {0}".format(tablename))
        conn.execute(trunc)
        conn.commit()


# https://docs.sqlalchemy.org/en/14/core/pooling.html#dealing-with-disconnects
engine = create_engine(
    config.SQLALCHEMY_DATABASE_URI, echo=config.debug, future=True, pool_recycle=3600, pool_pre_ping=True
)
Base.prepare(engine, reflect=True)
Session = sessionmaker(engine, autoflush=False, autocommit=False)
