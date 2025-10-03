from typing import Generic, TypeVar
from sqlalchemy.orm import Session

T = TypeVar('T')
U = TypeVar('U')

class BaseRepository(Generic[T, U]):
    @classmethod
    def from_session(cls, db: Session) -> U:
        return cls(db)
    
    def __init__(self, db: Session):
        self.db = db
        
    def create(self, model: T) -> T:
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model
    
    def get_all(self) -> list[T]:
        return self.db.query(T).all()
    
    def get_by_id(self, id: int) -> T:
        return self.db.query(T).filter(T.id == id).first()
    
    def update(self, model: T) -> T:
        self.db.commit()
        self.db.refresh(model)
        return model
    
    def delete(self, model: T) -> None:
        self.db.delete(model)
        self.db.commit()