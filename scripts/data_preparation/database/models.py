from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, Identity, UniqueConstraint, Date

Base = declarative_base()


class IndiceAperturas(Base):
    """indice_aperturas data model."""

    __tablename__ = "indice_aperturas"
    id = Column(Integer, Identity(start=1, cycle=True), primary_key=True)
    date = Column(Date, nullable=False)
    region = Column(String(50), nullable=False)
    category = Column(String(100), nullable=False)
    value = Column(Float, nullable=False)
    __table_args__ = (
        UniqueConstraint(
            date,
            region,
            category,
            name="one_value_per_datetime_per_region_per_category",
        ),
    )

    def __init__(self, id, date, region, category, value):
        self.id = id
        self.date = date
        self.region = region
        self.category = category
        self.value = value

    def __repr__(self):
        return f"({self.id}, {self.date}, {self.region}, {self.category}, {self.value})"
