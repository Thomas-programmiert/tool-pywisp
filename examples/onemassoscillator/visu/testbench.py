# -*- coding: utf-8 -*-
import struct
from collections import OrderedDict

from pywisp.experimentModules import ExperimentModule

from connection import Connection


class OneMassOscillator(ExperimentModule):
    dataPoints = [
        'pos',
        'speed',
        'u',
    ]

    publicSettings = OrderedDict([
        ("Config", 0),
        ("mass", 1.0),
        ("frictionCoeff", 0.1),
        ("springCoeff", 0.5),
    ])

    connection = Connection.__name__

    def getParams(self, data):
        payloadConfig = struct.pack('<B',
                                    int(data[0]),
                                    )

        payloadData = struct.pack('<3d',
                                  float(data[1]),
                                  float(data[2]),
                                  float(data[3]))
        
        dataPoints = [
            {'id': 10,
             'msg': payloadConfig
            },
            {'id': 11,
             'msg': payloadData
            }
        ]

        return dataPoints

    def handleFrame(self, frame):
        dataPoints = {}
        fid = frame.min_id
        if fid == 15:
            data = struct.unpack(f'<L{len(OneMassOscillator.dataPoints)}d', frame.payload)
            dataPoints['Time'] = data[0]
            dataPoints['DataPoints'] = dict(zip(OneMassOscillator.dataPoints, data[1:]))
        else:
            dataPoints = None

        return dataPoints
