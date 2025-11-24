from abc import ABC, abstractmethod

class AbstractSessionManager(ABC):
    @abstractmethod
    def create_session():
        pass

    @abstractmethod
    def set_semaphore():
        pass
