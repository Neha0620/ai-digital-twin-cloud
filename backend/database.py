import os

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime


# Use Render PostgreSQL when DATABASE_URL exists.
# Fall back to local SQLite when running on your laptop.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./smarthome.db")

# Render commonly provides postgresql://...
# Explicitly tell SQLAlchemy to use psycopg.
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1,
    )
elif DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql+psycopg://",
        1,
    )

connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    room = Column(String)
    appliance = Column(String)
    power_w = Column(Float)
    temp_c = Column(Float)
    is_on = Column(Integer, default=1)

    humidity = Column(Float, nullable=True)
    smoke_ppm = Column(Float, nullable=True)
    smoke_alert = Column(Integer, nullable=True)
    motion = Column(Integer, nullable=True)


class IotEvent(Base):
    __tablename__ = "iot_events"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    event_type = Column(String)
    room = Column(String)
    value = Column(Float, nullable=True)
    message = Column(String, nullable=True)
class DeviceState(Base):
    __tablename__ = "device_states"

    id = Column(Integer, primary_key=True, index=True)
    room = Column(String, unique=True, index=True)

    lights_on = Column(Integer, default=0)
    ac_on = Column(Integer, default=0)
    ac_level = Column(Integer, default=0)   # 0=OFF, 1=LOW, 2=MEDIUM, 3=HIGH
    geyser_on = Column(Integer, default=0)
    fridge_on = Column(Integer, default=0)
    servo_angle = Column(Integer, default=0)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)