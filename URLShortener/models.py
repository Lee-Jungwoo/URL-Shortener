from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from .db import db

class URL(db.Model): # table 'URLS'
    __tablename__ = 'urls'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    original_url: Mapped[str] = mapped_column(String(500))
    short_url: Mapped[str] = mapped_column(String(30), unique=True)
    

    def __repr__(self):
        return f'<URL {self.short_url}>'
