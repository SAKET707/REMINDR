from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
# SQLAlchemy database setup and Session factory.
from core.config import settings


engine = create_engine( # engine is sqlalachemy connection manager , Sessions use the Engine to communicate with PostgreSQL. does NOT execute queries itself.
    settings.DATABASE_URL, 
    echo=True, # for dev prints raw sql for debugging 
    pool_pre_ping=True, # if db connection is idle for say 30 min the connnection is closed ,
                        # w/o this next req use dead connection so crash , it asks if connection is alive or not , if no create new one
    pool_recycle=300, # every 300 sec discard connection n create new one to prevent stale connection
)

# session = conversation with db, every req gets 1 session
# sessionLocal is a factory , it knows how to create sessions , every req gets an isolated transaction 
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False, # means flush only when told , no auto flush , gives more control , no flush till i write db.flush()
                    # Prevent SQLAlchemy from automatically flushing pending SQL before certain queries
    autocommit=False, # means commit only when told, no auto commit , no commit till i say db.commit() , till then nothing is permanantly saved
                        # Helps keep multiple operations inside one transaction.
)

# this is the parent of every model , all models inherits this
class Base(DeclarativeBase):
    pass
# also responsible for making mapped classes
# w/o this sqlalchemy doesnt even know User is a table, alembic wouldnt even see it
# Base.metadata is compared with the current db schemas by alemibc to generate migration