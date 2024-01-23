import configparser
# import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


config = configparser.ConfigParser()
config.read('postgres.ini')

post_user = config.get('DB', 'user')
post_pass = config.get('DB', 'pass')
post_host = config.get('DB', 'host')
post_port = config.get('DB', 'port')
post_db = config.get('DB', 'db_name')

# ----- posgres connect -----
db_uri = f"""postgresql://{post_user}:{post_pass}@{post_host}:{post_port}/{post_db}"""
engine = create_engine(db_uri) #, echo=True) # for debug

DBSession = sessionmaker(bind=engine)
# session = DBSession() # this one should be closed, so we will call it in the main module
