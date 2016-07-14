# -*-coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 初始化数据库连接
engine = create_engine('mysql+mysqldb://root:wahty0673@localhost:3306/spider?charset=utf8')
# 创建DBSession类型
DBSession = sessionmaker(bind=engine)
