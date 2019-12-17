# -*- coding: utf-8 -*-
"""
# (C) 2019 Airbus copyright all rights reserved
Created on Fri Jun  8 15:42:57 2018

@author: brochard
"""

try:
    from PyQt5 import QtCore, QtNetwork
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QCoreApplication
except:
    from PyQt4 import QtCore, QtNetwork
    from PyQt4.QtGui import QApplication
    from PyQt4.QtCore import QCoreApplication
from surrender.blocking_socket import BlockingSocket
import sys;
import numpy as np
import os

class surrender_client_base:
    XYZ_SCALAR_CONVENTION = 0;
    SCALAR_XYZ_CONVENTION = 1;

    Z_BACKWARD = 0;
    Z_FRONTWARD = 1;
   
    def __init__(self):
        if QApplication.instance() != None:
            self.app = None;
        else:
            if os.name == 'nt' or 'DISPLAY' in os.environ:
                self.app = QApplication(["Surrender Session"])
            else:
                self.app = QCoreApplication(["Surrender Session"])

        msg = "Surrender Python Client\n"
        if self.SURRENDER_CLIENT_GIT_REVISION != None:
            msg += "code revision : " + str(self.SURRENDER_CLIENT_GIT_REVISION) + '\n';
        self._printError(msg);

        self._verbosity_level = 2;
        self._sock = None;
        self._stream = None;
        self._blocking_sock = None;
        self._async = True;

        self._pGMC = None;
        self._pFIFO = None;
        self._buf = QtCore.QByteArray();
        
    def __del__(self):
        self._pFIFO = None;

        self._buf = None;

        if self._sock:
            if self.isConnected():
                self._stream.writeQVariantHash({ "" : "close" });
                self._flush(True);
                self._sock.close();

            self._stream = None;
            self._sock.deleteLater();
            self._sock = None;
            self._stream = None;

        if self.app:
            self.app = None;

    def connectToServer(self, hostname, port = 5151):
        """
        Connect to a Surrender server. First parameter is the hostname, second parameter the TCP port.
        """
        if self._sock:
            self._sock.deleteLater();
            self._sock = None;
            self._stream = None;

        self._sock = QtNetwork.QTcpSocket();
        self._sock.connectToHost(hostname, port, QtCore.QIODevice.ReadWrite);
        if not self._sock.waitForConnected():
            self._printError("error connecting to " + hostname + " : " + self._sock.errorString() + "\n");
            self._sock.deleteLater();
            self._sock = None;
            self._stream = None;
            return;

        self._sock.setSocketOption(QtNetwork.QTcpSocket.LowDelayOption, 1);
        self._sock.setSocketOption(QtNetwork.QTcpSocket.KeepAliveOption, 1);
        self._blocking_sock = BlockingSocket(self._sock);
        self._stream = QtCore.QDataStream(self._blocking_sock);
        self._stream.setVersion(QtCore.QDataStream.Qt_4_6);



    def getImage(self):
        """
        Return the last generated image with its 4 channels in float.
        The unit of the returned values depend on the effect enabled for rendering.
        """
        self._check_connection();
        self._stream.writeQVariantHash({ "" : "getImage" });
        self._flush(True);
        ret = self._read_return("getImage");

        w32 = ret["w"];
        h32 = ret["h"];

        if ret["compressed"]:
            self._buf = QtCore.qUncompress(ret["image_data"]);
        else:
            self._buf = ret["image_data"];

        return np.flipud(np.frombuffer(self._buf.data(), dtype=np.float32).reshape(h32, w32, 4));
        
    def getImageRGBA8(self):
        """
        Return the last generated image with its 4 channels in 8bits.
        """
        self._check_connection();
        self._stream.writeQVariantHash({ "" : "getImageRGBA8" });
        self._flush(True);
        ret = self._read_return("getImageRGBA8");

        w32 = ret["w"];
        h32 = ret["h"];

        if ret["compressed"]:
            self._buf = QtCore.qUncompress(ret["image_data"]);
        else:
            self._buf = ret["image_data"];

        return np.flipud(np.frombuffer(self._buf.data(), dtype=np.uint8).reshape(h32, w32, 4));

    def getDepthMap(self):
        """
        | Return the depth map of the last rendererd image in double precision.
        | NB: if PSF is enabled or if more than 1 ray is cast per pixel then this is likely to be meaningless.
        """
        self._check_connection();
        self._stream.writeQVariantHash({ "" : "getDepthMap" });
        self._flush(True);
        ret = self._read_return("getDepthMap");

        w32 = ret["w"];
        h32 = ret["h"];

        if ret["compressed"]:
            self._buf = QtCore.qUncompress(ret["depth_data"]);
        else:
            self._buf = ret["depth_data"];

        return np.flipud(np.frombuffer(self._buf.data(), dtype=np.float64).reshape(h32, w32));
        
    def getNormalMap(self):
        """
        | Return the normal map of the last rendererd image in double precision.
        | NB: if PSF is enabled or if more than 1 ray is cast per pixel then this is likely to be meaningless.
        """
        self._check_connection();
        self._stream.writeQVariantHash({ "" : "getNormalMap" });
        self._flush(True);
        ret = self._read_return("getNormalMap");

        w32 = ret["w"];
        h32 = ret["h"];

        if ret["compressed"]:
            self._buf = QtCore.qUncompress(ret["normal_data"]);
        else:
            self._buf = ret["normal_data"];

        return np.flipud(np.frombuffer(self._buf.data(), dtype=np.float32).reshape(h32, w32, 3));

    def closeViewer(self):
        """
        Close the viewer window on the server side.
        """
        self._stream.writeQVariantHash({ "" : "closeViewer" });
        self._flush(True);
        self._read_return("closeViewer");

    def setCompressionLevel(self, lvl):
        """
        Set the compression level for image transfer. Ranges from 0 to 9, 0 means no compression and 9 means maximum compression. Default value is 3 when server is on a different computer, 0 otherwise.
        """
        self._check_connection();
        params = {
            "compression_level" : int(lvl),
            "" : "setCompressionLevel"
            };
        self._stream.writeQVariantHash(params);
        self._flush(True);
        self._read_return("setCompressionLevel");
        
    def getImageGray32F(self):
        """
        Return the last generated image as a single channel (the mean of the first 3 channels, usually RGB) in float.
        """
        self._check_connection();
        self._stream.writeQVariantHash({ "" : "getImageGray32F" });
        self._flush(True);
        ret = self._read_return("getImageGray32F");

        w32 = ret["w"];
        h32 = ret["h"];

        if ret["compressed"]:
            self._buf = QtCore.qUncompress(ret["image_data"]);
        else:
            self._buf = ret["image_data"];

        return np.flipud(np.frombuffer(self._buf.data(), dtype=np.float32).reshape(h32, w32));

    def getImageGray8(self):
        """
        Return the last generated image as a single channel (the mean of the first 3 channels, usually RGB) in 8bits.
        """
        self._check_connection();
        self._stream.writeQVariantHash({ "" : "getImageGray8" });
        self._flush(True);
        ret = self._read_return("getImageGray8");

        w32 = ret["w"];
        h32 = ret["h"];

        if ret["compressed"]:
            self._buf = QtCore.qUncompress(ret["image_data"]);
        else:
            self._buf = ret["image_data"];

        return np.flipud(np.frombuffer(self._buf.data(), dtype=np.uint8).reshape(h32, w32));

    def isConnected(self):
        """
        Returns True if connected to a server, False otherwise.
        """
        return self._stream and self._sock and self._sock.isOpen();

    def runLuaCode(self, code):
        """
        Run the given Lua code on the server. The Lua VM is preserved across calls so you can store values in the VM global environment.
        """
        self._check_connection();
        self._stream.writeQVariantHash({"" : "runLUACode",
                                       "code" : str(code) });
        self._flush(True);

        ret = self._read_return("runLUACode");
        return ret.get("return");
        
    def runLuaScript(self, filename):
        """
        Run a Lua script (which should be on the server) in the Lua VM of the server.
        """
        self._check_connection();
        self._stream.writeQVariantHash({ "" : "runLUAScript",
                                  "filename" : str(filename) });
        self._flush(True);
        ret = self._read_return("runLUAScript");
        return ret.get("return");

    # Data is required to be in scanline order
    def updateUserDataTexture(self, name, data, compressionLevel):
        """
        | Send texture data to replace the content of a dynamic user texture.
        | name is the name of the texture to update.
        | data a vector of float values, one for each pixel.
        | compressionLevel allows enabling compression to speed up transfer (-1 means LZ4, 0 means no compression, 1-9 means zlib compression).
        """
        self._check_connection();
        params = {
            "name" : str(name),
            "" : "updateUserDataTexture"
            };
        if compressionLevel != -2:  # Zlib compression (deflate)
            params["data"] = QtCore.qCompress(QtCore.QByteArray.fromRawData(data), compressionLevel);
        else:                       # LZ4 compression
##ifdef LZ4_FOUND
#            params["size"] = quint32(data.size() * sizeof(data.front()));
#            params["use_lz4"] = true;
#            QByteArray qdata = QByteArray::fromRawData((const char*)data.data(), data.size() * sizeof(data.front()));
#            const int worst_size = LZ4_compressBound(qdata.size());
#            QByteArray lz4_data(worst_size, Qt::Uninitialized);
#            const int lz4_size = LZ4_compress(qdata.data(), lz4_data.data(), qdata.size());
#            lz4_data.resize(lz4_size);
#            params["data"] = lz4_data;
##else
            self._printError("LZ4 support not implemented, falling back to zlib compression level 1");
            params["data"] = QtCore.qCompress(QtCore.QByteArray.fromRawData(data), 1);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        self._read_return("updateUserDataTexture");

    # Timeout in seconds for TCP requests
    def setTimeOut(self, timeout):
        """
        Sets the timeout in seconds to wait for server responses.
        """
        self._check_connection();
        if timeout>= sys.maxsize // 1000:       # In case of overflow
            self._blocking_sock.setTimeOut(sys.maxsize);
        else:
            self._blocking_sock.setTimeOut(timeout * 1000);

    def setPSF(self, psf_image, support_w = -1, support_h = -1, blooming_threshold_distance = 0):
        """
        Set the PSF as a 2D matrix of weights with its support (or size) in pixels and a distance in samples above which samples are considered part of the tail.
        """
        self._check_connection();
        w = psf_image.shape[1];
        h = psf_image.shape[0];
        
        psf = np.array(psf_image, dtype=np.float32).tobytes();

        params = {
            "w" : int(w),
            "h" : int(h),
            "psf" : QtCore.QByteArray.fromRawData(psf),
            "support_w" : float(support_w),
            "support_h" : float(support_h),
            "blooming_threshold_distance" : int(blooming_threshold_distance),
            "" : "setPSF"
            };

        self._stream.writeQVariantHash(params);
        self._flush(True);
        self._read_return("setPSF");

    def setPSFWithTail(self, psf_image,
                       psf_tail_image,
                       PSF_tail_coef,
                       support_w = -1,
                       support_h = -1,
                       support_w_tail = -1,
                       support_h_tail = -1):
        """
        | Same as setPSF but allows using a different sampling for the PSF tail.
        | psf_image, support_w and support_h define the PSF center and its support (in pixels).
        | psf_tail_image, support_w_tail and support_h_tail define the PSF tail and its support (in pixels).
        | PSF_tail_coef is the fraction of energy in the tail used when blending the 2 parts of the PSF.
        """
        self._check_connection();
        w = psf_image.shape[1];
        h = psf_image.shape[0];
        w_tail = psf_tail_image.shape[1];
        h_tail = psf_tail_image.shape[0];
        
        psf = np.array(psf_image, dtype=np.float32).tobytes();

        psf_tail = np.array(psf_tail_image, dtype=np.float32).tobytes();

        params = {
            "w" : int(w),
            "h" : int(h),
            "psf" : QtCore.QByteArray.fromRawData(psf),
            "support_w" : float(support_w),
            "support_h" : float(support_h),

            "w_tail" : int(w_tail),
            "h_tail" : int(h_tail),
            "psf_tail" : QtCore.QByteArray.fromRawData(psf_tail),
            "support_w_tail" : float(support_w_tail),
            "support_h_tail" : float(support_h_tail),

            "blooming_threshold_distance" : int(0),
            "PSF_tail_coef" : float(PSF_tail_coef),

            "" : "setPSFWithTail"
            };

        self._stream.writeQVariantHash(params);
        self._flush(True);
        self._read_return("setPSFWithTail");

#        void getGMCVideo_streamRGB8(image_rgba8_t &image);
#
    def getImageSpectrumProjection(self, spectrum):
        """
        | Return the last generated image as a single channel in float.
        | For each pixel the returned value is the projection of the pixel data along the given spectrum vector.
        """
        self._check_connection();
        self._stream.writeQVariantHash({ "" : "getImageSpectrumProjection",
                                        "spectrum" : self._vec(spectrum) });
        self._flush(True);
        ret = self._read_return("getImageSpectrumProjection");

        w32 = ret["w"];
        h32 = ret["h"];
        
        if ret["compressed"]:
            self._buf = QtCore.qUncompress(ret["image_data"]);
            # Reorder bytes (splitting the 4 bytes of each float into 4 planes helps compressing data)
            byte_planes = np.frombuffer(self._buf.data(), dtype=np.uint8).reshape(4,h32, w32);
            img = np.frombuffer(byte_planes.transpose(1,2,0).tobytes(), dtype=np.float32).reshape(h32,w32);
        else:
            self._buf = ret["image_data"];
            img = np.frombuffer(self._buf.data(), dtype=np.float32).reshape(h32,w32);

        return np.flipud(img);

    def setVerbosityLevel(self, verbosity_level):
        """
        | Set the verbosity of server log.
        | 0 : quiet
        | 1 : errors only
        | 2 : errors and warnings
        | 3 : everything
        """
        self._verbosity_level = verbosity_level;

    def getPSF(self):
        """
        Return a 2D matrix of weights correponding to the active PSF.
        """
        self._check_connection();
        self._stream.writeQVariantHash({ "" : "getPSF" });
        self._flush(True);
        ret = self._read_return("getPSF");
        w = ret["width"];
        h = ret["height"];
        data = ret["psf"];

        return np.frombuffer(data, dtype=np.float32).reshape(h,w);

    def sendFile(self, filename, data, compressionLevel = -1):
        """
        | Send a file to the server.
        | filename is the name of the file to be created/replaced on the server.
        | data is the file content.
        | compressionLevel level of zlib compression ranging from 0 (no compression) to 9 (maximum compression).
        """
        self._check_connection();
        params = {
            "filename" : str(filename),
            "compressed" : bool(compressionLevel != 0),
            "" : "sendFile"
            };
        if (compressionLevel == 0):
            params["data"] = QtCore.QByteArray.fromRawData(data);
        else:
            params["data"] = QtCore.qCompress(QtCore.QByteArray.fromRawData(data), compressionLevel);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        self._read_return("sendFile");

    def sendImageTo(self,
                    target,  # IP / Hostname
                    port,
                    format,  # raw, lz4, zlib
                    depth,   # 8, 16, 32
                    channels,# 1, 2, 3, 4
                    texture_name = ""):   # texture name or empty for frame _buffer
        """
        | Send an image over another TCP/IP link.
        | target is the hostname/IP of the destination.
        | port is the port over which to connect.
        | format is either \"raw\", \"lz4\" or \"zlib\", a \"_bs\" suffix can be used to swap bytes in order to match a different endianness (\"raw_bs\", \"lz4_bs\" or \"zlib_bs\").
        | depth is the number of bits per plane (8, 10, 12, 14, 16 or 32). 10, 12, 14 and 16 bits are stored as 16bits elements
        | channels is the number of planes (1, 2, 3 or 4).
        | texture_name is the name of the source texture to send. Empty string means the last rendered image.
        """
        self._check_connection();
        params = {
            "target_name" : str(target),
            "format" : str(format),
            "port" : int(port),
            "depth" : int(depth),
            "channels" : int(channels),
            "texture_name" : str(texture_name),
            "" : "sendImageTo"
            };
        self._stream.writeQVariantHash(params);
        self._flush(True);

    def _flush(self, b_force = False):
        if (self._sock and (self._sock.bytesToWrite() > 0x1000 or b_force)):
            self._sock.flush();
            while (self._sock.bytesToWrite() > 0 and self._sock.isOpen()):
                self._sock.flush();
                self._sock.waitForBytesWritten(1000);

    def _printError(self, s):
        print(s, end='');
        if len(s) > 0 and s[-1] != '\n':
            print();

    def _check_connection(self):
        if not self.isConnected():
            self._printError("error: you must connect to a server before sending commands.\n");
            raise RuntimeError("error: you must connect to a server before sending commands.\n");

    def _read_return(self, COMMAND_ID):
        ret = {};
        while (self._sock.isOpen() and (ret.get("") == None or ret.get("") != COMMAND_ID)):
            self._check_connection();
            ret = self._stream.readQVariantHash();
            if ret.get("") == None and self._verbosity_level > 0 and ret.get("data") != None:
                msg = ret["data"].data().decode('utf-8');
                if (self._verbosity_level == 2 or (self._verbosity_level == 1 and msg.find("[error]") != -1)):
                    self._printError(msg);
        return ret;

    # This will fail if object is not iterable which is desired behavior
    def _vec(self, v):
        return np.array(v, dtype=np.float64).tolist()

    # This will fail if object is not a 4x4 numpy array
    def _mat44(self, v):
        return [ [ float(v[j,i]) for i in range(4) ] for j in range(4)]
