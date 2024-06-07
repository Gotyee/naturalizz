from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata


class Taxon(Base):
    __tablename__ = "taxon"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name_id = Column(Integer, ForeignKey("language_translation.id"))
    specie_id = Column(Integer, ForeignKey("language_translation.id"))
    genus_id = Column(Integer, ForeignKey("language_translation.id"))
    family_id = Column(Integer, ForeignKey("language_translation.id"))
    order_id = Column(Integer, ForeignKey("language_translation.id"))
    class_id = Column(Integer, ForeignKey("language_translation.id"))

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )


class ConfigType(Base):
    __tablename__ = "config_type"

    id = Column(Integer, primary_key=True, autoincrement=True)

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
    taxon_id = Column(Integer, ForeignKey("taxon.id"))
    photo_url = Column(String, nullable=False)


class LanguageTranslation(Base):
    __tablename__ = "language_translation"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    vernacular = Column(String(255), nullable=False)
    french = Column(String(255))
