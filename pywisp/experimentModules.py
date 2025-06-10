# -*- coding: utf-8 -*-
import logging
from abc import ABCMeta, abstractmethod

from PyQt5.QtCore import QObject

pyqtWrapperType = type(QObject)

__all__ = ["ExperimentModule"]


class ExperimentModuleMeta(ABCMeta, pyqtWrapperType):
    pass


class ExperimentModuleException(Exception):
    pass


class ExperimentModule(QObject, metaclass=ExperimentModuleMeta):
    """
    Smallest unit of the framework.
    This class provides necessary functions like start, stop and general
    parameter handling and holds all settings that can be accessed by the
    user.
    The :py:attr:`publicSettings` are rendered by the GUI. All entries
    stated in this dictionary will be available as changeable settings for the
    module. On initialization, a possibly modified (in terms of its values) version of
    this dict will be passed back to this class and is thenceforward available
    via the :py:attr:`settings` property.
    The :py:attr:`dataPoints` are accessible by the GUI for plotting.
    The :py:attr:`connection` determines the connection interface.
    """
    def __init__(self):
        QObject.__init__(self, None)
        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    @abstractmethod
    def publicSettings(self):
        """
        OrderedDict of settings which can be changed in the GUI with keys and values.
        must be declared
        """
        pass

    @property
    @abstractmethod
    def dataPoints(self):
        """
        array of strings for the names of every plotable parameter.
        must be declared
        """
        pass

    @property
    @abstractmethod
    def connection(self):
        """
        string of the chosen connections classname.
        must be declared
        """
        pass

    @abstractmethod
    def handleFrame(self, frame):
        """
        returns a dict with keys 'Time' and 'DataPoints',
        where the value of 'Time' is the time in milliseconds as a long int,
        and the value of 'Datapoints' is a dict. 
        The Datapoint dict has names as keys and the current values of plottable parameters
        """
        pass

    @abstractmethod
    def getStartParams(self, *args):
        """
        fetches parameters from the GUI when starting an experiment
        returns them as array of dicts with key's 'id' and 'msg',
        where the value of 'id' is the identifier of the frame,
        and the value of 'msg' is the raw data of a packed struct.
        """
        pass

    @abstractmethod
    def getStopParams(self, *args):
        """
        fetches parameters from the GUI when stopping an experiment
        returns them as array of dicts with key's 'id' and 'msg',
        where the value of 'id' is the identifier of the frame,
        and the value of 'msg' is the raw data of a packed struct.
        """
        pass

    @abstractmethod
    def getParams(self, *args):
        """
        fetches parameters from the GUI every tick
        returns them as array of dicts with key's 'id' and 'msg',
        where the value of 'id' is the identifier of the frame,
        and the value of 'msg' is the raw data of a packed struct.
        """
        pass

