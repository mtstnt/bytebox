from bytebox.config.repository import BaseRepository
from bytebox.users.models import UserModel

class UserRepository(BaseRepository[UserModel, 'UserRepository']):
    
    def get_by_email_or_username(self, email: str, username: str) -> UserModel:
        return self.db.query(UserModel).filter(
            (UserModel.email == email) | (UserModel.username == username)
        ).first()