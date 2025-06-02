from sqlalchemy import create_engine
from sqlalchemy.engine import URL


class Config:

    # 直接使用字典构建数据库URL，避免字符串拼接问题
    DATABASE_URL = URL.create(
        drivername="mysql+pymysql",
        username="root",
        password="Edz@1230",
        host="localhost",
        port=3306,
        database="shuaigestore",
        query={"charset": "utf8mb4"}
    )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False