from collections.abc import Generator
from tempfile import NamedTemporaryFile

from event_sourcery.event_store import Backend
from event_sourcery_sqlalchemy import SQLAlchemyBackendFactory
from event_sourcery_sqlalchemy.models import configure_models
from fastapi import Depends
from sqlalchemy import MetaData, StaticPool, create_engine
from sqlalchemy.orm import Session, as_declarative

with NamedTemporaryFile() as f:
    engine = create_engine(
        f"sqlite:///{f.name}",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )


@as_declarative()
class Base:
    metadata: MetaData


configure_models(Base)
Base.metadata.create_all(bind=engine)


def session() -> Generator[Session, None, None]:
    dbsession = Session(bind=engine, autoflush=False)
    try:
        yield dbsession
        dbsession.commit()
    finally:
        dbsession.close()


def backend(dbsession: Session = Depends(session)) -> Backend:
    return SQLAlchemyBackendFactory(dbsession).with_outbox().build()
