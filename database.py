import json
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./nexus_database.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    role = Column(String) # "user" or "agent"
    content = Column(Text)

class VectorChunk(Base):
    __tablename__ = "vector_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_name = Column(String, index=True)
    chunk_text = Column(Text)
    embedding_json = Column(Text) # Store numpy array as JSON string

Base.metadata.create_all(bind=engine)
