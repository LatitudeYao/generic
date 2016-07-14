# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

class Rule(base):
    __tablename__ = 'rules'

    # 表的结构
    id = Column(Integer, primary_key=True)
    name = Column(String)
    allow_domains = Column(String)
    start_urls = Column(String)
    next_page = Column(String)
    allow_url = Column(String)
    extract_from = Column(String)
    title_xpath = Column(String)
    body_xpath = Column(String)
    publish_time_xpath = Column(String)
    source_site_xpath = Column(String)
    enable = Column(Integer)