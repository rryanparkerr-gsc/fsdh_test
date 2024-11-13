# -*- coding: utf-8 -*-
"""
*DESCRIPTION*

Author: rparker
Created: 2023-05-31
"""

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker

host = "fsdh-pdbtest-psql-poc.postgres.database.azure.com"
database = "fsdh"
user = "fsdhadmin"
password = "dIssuGw46yrCy82080CE"
port = 5432

url = URL.create(drivername="postgresql", username=user, password=password, host=host, port=port,
                 database=database)
engine = create_engine(url, connect_args={"options": "-c timezone=utc"})
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)
