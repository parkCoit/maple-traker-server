from abc import ABC, abstractmethod


class UserBase(ABC):

    @abstractmethod
    def create_user(self, nickname: str) -> dict:
        pass

    @abstractmethod
    def read_user_by_nickname(self, nickname: str) -> dict:
        pass