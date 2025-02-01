from abc import abstractmethod


class BaseLogAdapter:
    @abstractmethod
    def configure_default(self, *arg, **kwargs):
        pass

    @abstractmethod
    def debug(self, *arg, **kwargs):
        pass

    @abstractmethod
    def info(self, *arg, **kwargs):
        pass

    @abstractmethod
    def error(self, *arg, **kwargs):
        pass

    @abstractmethod
    def exception(self, *arg, **kwargs):
        pass
