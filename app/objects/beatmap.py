from sqlalchemy import Column, Integer, Text, text, Numeric, DateTime
from app.constants.servers import Server
from app.database import Base


class Beatmap(Base):
    __tablename__ = "beatmaps"
    md5 = Column(Text, primary_key=True)
    id = Column(Integer, nullable=True)  # null if beatmap is on local server
    set_id = Column(Integer, nullable=True)  # null if beatmap is on local server
    ranked_status = Column(Integer, nullable=False)
    artist = Column(Text, nullable=False)
    title = Column(Text, nullable=False)
    version = Column(Text, nullable=False)
    creator = Column(Text, nullable=False)
    filename = Column(Text, nullable=False)
    total_length = Column(Integer, nullable=False)
    max_combo = Column(Integer, nullable=False)
    mode = Column(Integer, nullable=False)
    bpm = Column(Numeric(12, 2), nullable=False, server_default=text("0.00")),
    cs = Column(Numeric(4, 2), nullable=False, server_default=text("0.00")),
    ar = Column(Numeric(4, 2), nullable=False, server_default=text("0.00")),
    od = Column(Numeric(4, 2), nullable=False, server_default=text("0.00")),
    hp = Column(Numeric(4, 2), nullable=False, server_default=text("0.00")),
    star_rating = Column(Numeric(6, 3), nullable=False, server_default=text("0.000")),
    updated_at = Column(DateTime(True), nullable=False, server_default=text("now()")),
    server_updated_at = Column(DateTime(True), nullable=False),
    server_id = Column(Integer, nullable=False, default=Server.BANCHO)
