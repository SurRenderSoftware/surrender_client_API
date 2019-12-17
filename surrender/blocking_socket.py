# -*- coding: utf-8 -*-
"""
# (C) 2019 Airbus copyright all rights reserved
Created on Fri Jun  8 17:33:21 2018

@author: brochard
"""

try:
    from PyQt5 import QtCore;
except:
    from PyQt4 import QtCore;

class BlockingSocket(QtCore.QIODevice):

    def __init__(self, dev, timeout = 300000):
        QtCore.QIODevice.__init__(self, dev);
        self.dev = dev;
        self.timeout_in_ms = timeout;
        self.open(QtCore.QIODevice.ReadWrite | QtCore.QIODevice.Unbuffered);

    def isSequential(self):
        return self.dev.isSequential();
        
    def size(self):
        return self.dev.size();

    def atEnd(self):
        return self.dev.atEnd() and QtCore.QIODevice.atEnd(self);

    def bytesAvailable(self):
        return QtCore.QIODevice.bytesAvailable(self) + self.dev.bytesAvailable();

    def bytesToWrite(self):
        return QtCore.QIODevice.bytesToWrite(self) + self.dev.bytesToWrite();

    def canReadLine(self):
        return self.dev.canReadLine() or QtCore.QIODevice.canReadLine(self);
        
    def close(self):
        self.dev.close();

    def setTimeOut(self, timeout):
        self.timeout_in_ms = timeout;

    def readLineData(self, maxSize):
        return self.dev.readLine(maxSize);

    def readData (self, maxSize):
        if (not self.dev.isOpen()):
            raise IOError("Connection is closed!");
        
        data = b'';
        while (len(data) < maxSize and self.dev.isOpen()):
            if (self.dev.bytesAvailable() == 0):
                if (not self.dev.waitForReadyRead(self.timeout_in_ms)):
                    self.dev.close();
                    raise IOError("Connection error: {} (timeout set to {} ms)".format(self.dev.errorString(), self.timeout_in_ms))
            try:
                chunk = self.dev.read(maxSize - len(data));
            except:
                self.dev.close();
                raise IOError("Socket error!");
            data = data + chunk;

        return data;

    def writeData (self, str):
        return self.dev.write(str);
