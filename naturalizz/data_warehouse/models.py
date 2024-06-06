from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata


class Taxon(Base):
    __tablename__ = "taxon"

    id = Column(INTEGER(11), primary_key=True, autoincrement=True)

    name = Column(String(255), nullable=False)
    specie = Column(String(255), nullable=False)
    genus = Column(String(255))
    family = Column(String(255))
    order = Column(String(255))
    class_ = Column(String(255))

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )


class ConfigType(Base):
    __tablename__ = "config_type"

    id = Column(INTEGER(11), primary_key=True, autoincrement=True)

    type_name = Column(String(255), nullable=False)

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )


class TaxonType(Base):
    __tablename__ = "taxon_type"

    taxon_id = Column(Integer, ForeignKey("taxon.id"), primary_key=True)
    config_type_id = Column(Integer, ForeignKey("config_type.id"), primary_key=True)

    taxon = relationship("Taxon", back_populates="config_type")
    config_type = relationship("ConfigType", back_populates="taxon")


class TaxonPhoto(Base):
    __tablename__ = "taxon_photo"

    id = Column(Integer, primary_key=True, autoincrement=True)
    photo_url = Column(String, nullable=False)
    taxon_type_id = Column(Integer, ForeignKey("taxon.id"))
