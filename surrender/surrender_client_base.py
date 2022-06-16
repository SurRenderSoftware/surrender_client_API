# -*- coding: utf-8 -*-
"""
# (C) 2019 Airbus copyright all rights reserved
Created on Fri Jun  8 15:42:57 2018

@author: brochard
"""

import numpy as np
import os
import socket
import struct
import zlib
from hashlib import md5

class surrender_client_base:
    XYZ_SCALAR_CONVENTION = 0;
    SCALAR_XYZ_CONVENTION = 1;

    Z_BACKWARD = 0;
    Z_FRONTWARD = 1;
    
    _DT_Invalid = 0;
    _DT_Bool = 1;
    _DT_Int = 2;
    _DT_UInt = 3;
    _DT_ULongLong = 5;
    _DT_Double = 6;
    _DT_Map = 8;
    _DT_List = 9;
    _DT_String = 10;
    _DT_ByteArray = 12;
    _DT_Hash = 28;
    
   
    def __init__(self):
        msg = "Surrender Python Client\n"
        if self.SURRENDER_CLIENT_GIT_REVISION != None:
            msg += "code revision : " + str(self.SURRENDER_CLIENT_GIT_REVISION) + '\n';
        self._printError(msg);

        self._verbosity_level = 2;
        self._sock = None;
        self._async = True;
        self._exception_on_error = True;
        self._exception_on_warning = False;

        # This is temporary
        self._stream = self;
        
    def __del__(self):
        if self._sock:
            try:
                if self.isConnected():
                    self.writeQVariantHash({ "" : "close" });
                    self._flush(True);
                    self._sock.close();
            except:
                pass;
            self._sock = None;

    def connectToServer(self, hostname, port = 5151):
        """
        Connect to a Surrender server. First parameter is the hostname, second parameter the TCP port.
        """
        if self._sock:
            self._sock.close();
            self._sock = None;

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0);
        if self._sock == -1 or self._sock == None:
            raise IOError("Error creating TCP socket");

        try:
            self._sock.connect((hostname, port))
            self._sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

        except Exception as e:
            msg = "error connecting to " + hostname + " : " + str(e) + "\n";
            self._printError(msg);
            self._sock = None;
            if self._exception_on_error:
                raise RuntimeError(msg);
            return;

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
            _buf = self._uncompress(ret["image_data"]);
        else:
            _buf = ret["image_data"];

        return np.flipud(np.frombuffer(_buf, dtype=np.float32).reshape(h32, w32, 4));
        
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
            _buf = self._uncompress(ret["image_data"]);
        else:
            _buf = ret["image_data"];

        return np.flipud(np.frombuffer(_buf, dtype=np.uint8).reshape(h32, w32, 4));

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
            _buf = self._uncompress(ret["depth_data"]);
        else:
            _buf = ret["depth_data"];

        return np.flipud(np.frombuffer(_buf, dtype=np.float64).reshape(h32, w32));
        
    def getNormalMap(self):
        """
        | Return the normal map of the last rendererd image in single precision.
        | NB: if PSF is enabled or if more than 1 ray is cast per pixel then this is likely to be meaningless.
        """
        self._check_connection();
        self._stream.writeQVariantHash({ "" : "getNormalMap" });
        self._flush(True);
        ret = self._read_return("getNormalMap");

        w32 = ret["w"];
        h32 = ret["h"];

        if ret["compressed"]:
            _buf = self._uncompress(ret["normal_data"]);
        else:
            _buf = ret["normal_data"];

        return np.flipud(np.frombuffer(_buf, dtype=np.float32).reshape(h32, w32, 3));

    def getLOSMap(self):
        """
        | Returns the LOS map of the last raytraced image in single precision.
        | Each pixel is a 3D vector containing the average LOS for each simulated pixel.
        | 'Empty' pixels (pixels we don't bother to scan because we known there is nothing or
        | because pixel integration time is 0) will be set to (0,0,0).
        """
        self._check_connection();
        self._stream.writeQVariantHash({ "" : "getLOSMap" });
        self._flush(True);
        ret = self._read_return("getLOSMap");

        w32 = ret["w"];
        h32 = ret["h"];
        
        if w32 * h32 == 0:
            return None

        if ret["compressed"]:
            _buf = self._uncompress(ret["los_data"]);
        else:
            _buf = ret["los_data"];

        return np.flipud(np.frombuffer(_buf, dtype=np.float32).reshape(h32, w32, 3));

    def getTimeMap(self):
        """
        | Returns the time map of the last raytraced image in single precision.
        | Each pixel is a float containing the average time for each simulated pixel.
        | 'Empty' pixels (pixels we don't bother to scan because we known there is nothing or
        | because pixel integration time is 0) will be set to NaN.
        """
        self._check_connection();
        self._stream.writeQVariantHash({ "" : "getTimeMap" });
        self._flush(True);
        ret = self._read_return("getTimeMap");

        w32 = ret["w"];
        h32 = ret["h"];
        
        if w32 * h32 == 0:
            return None

        if ret["compressed"]:
            _buf = self._uncompress(ret["time_data"]);
        else:
            _buf = ret["time_data"];

        return np.flipud(np.frombuffer(_buf, dtype=np.float32).reshape(h32, w32));

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
            _buf = self._uncompress(ret["image_data"]);
        else:
            _buf = ret["image_data"];

        return np.flipud(np.frombuffer(_buf, dtype=np.float32).reshape(h32, w32));

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
            _buf = self._uncompress(ret["image_data"]);
        else:
            _buf = ret["image_data"];

        return np.flipud(np.frombuffer(_buf, dtype=np.uint8).reshape(h32, w32));

    def isConnected(self):
        """
        Returns True if connected to a server, False otherwise.
        """
        return self._sock != None

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
            params["data"] = self._compress(data, compressionLevel);
        else:                       # LZ4 compression
##ifdef LZ4_FOUND
#            params["size"] = uint32_t(data.size() * sizeof(data.front()));
#            params["use_lz4"] = true;
#            QByteArray qdata = QByteArray::fromRawData((const char*)data.data(), data.size() * sizeof(data.front()));
#            const int worst_size = LZ4_compressBound(qdata.size());
#            QByteArray lz4_data(worst_size, Qt::Uninitialized);
#            const int lz4_size = LZ4_compress(qdata.data(), lz4_data.data(), qdata.size());
#            lz4_data.resize(lz4_size);
#            params["data"] = lz4_data;
##else
            self._printError("LZ4 support not implemented, falling back to zlib compression level 1");
            params["data"] = self._compress(data, 1);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        self._read_return("updateUserDataTexture");

    # Timeout in seconds for TCP requests
    def setTimeOut(self, timeout):
        """
        Sets the timeout in seconds to wait for server responses.
        """
        self._check_connection();
        if self._sock:
            self._sock.settimeout(timeout);

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
            "psf" : psf,
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
            "psf" : psf,
            "support_w" : float(support_w),
            "support_h" : float(support_h),

            "w_tail" : int(w_tail),
            "h_tail" : int(h_tail),
            "psf_tail" : psf_tail,
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
            _buf = self._uncompress(ret["image_data"]);
            # Reorder bytes (splitting the 4 bytes of each float into 4 planes helps compressing data)
            byte_planes = np.frombuffer(_buf, dtype=np.uint8).reshape(4,h32, w32);
            img = np.frombuffer(byte_planes.transpose(1,2,0).tobytes(), dtype=np.float32).reshape(h32,w32);
        else:
            _buf = ret["image_data"];
            img = np.frombuffer(_buf, dtype=np.float32).reshape(h32,w32);

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

    def sendFile(self, filename, data, compressionLevel = -1, offset = 0, append = False):
        """
        | Send a file to the server.
        | filename is the name of the file to be created/replaced on the server.
        | data is the file content.
        | compressionLevel level of zlib compression ranging from 0 (no compression) to 9 (maximum compression).
        | offset is an offset, in bytes, from the beginning of the file.
        | append enables keeping file content, otherwise file content is discarded before writing.
        """
        self._check_connection();
        params = {
            "filename" : str(filename),
            "compressed" : bool(compressionLevel > 0),
            "offset" : int(offset),
            "append" : bool(append),
            "" : "sendFile"
            };
        if (compressionLevel <= 0):
            params["data"] = data;
        else:
            params["data"] = self._compress(data, compressionLevel);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        self._read_return("sendFile");

    def syncDir(self, dirname, compressionLevel = -1):
        """
        | Synchronize a folder with the active resource folder on the server.
        | This function first sends check sums to send data only when needed.
        | dirname is the name of the client folder to be synchronized on the server.
        | compressionLevel level of zlib compression ranging from 0 (no compression) to 9 (maximum compression).
        """
        self._check_connection();
        
        files = []
        for (dirpath, dirnames, filenames) in os.walk(dirname):
            for f in filenames:
                fname = dirpath + '/' + f
                short_fname = os.path.relpath(fname, dirname)
                hash_md5 = md5()
                print('Checking "{}"'.format(fname))
                with open(fname, "rb") as fd:
                    file_size = fd.seek(0,2)
                    fd.seek(0)
                    offset = 0
                    last_ratio = int(0)
                    for chunk in iter(lambda: fd.read(1048576), b""):
                        hash_md5.update(chunk)
                        offset += len(chunk)

                        ratio = int(offset * 100 / file_size)
                        if (last_ratio != ratio):
                            last_ratio = ratio
                            print('\r{}%    '.format(ratio), end='', flush=True)
                files.append([short_fname, hash_md5.hexdigest()])
                print('\r    \r', end='', flush=True)
        params = {
            "dirname" : dirname,
            "files" : files,
            "compressionLevel" : int(compressionLevel),
            "" : "syncDir"
            };
        self._stream.writeQVariantHash(params);
        self._flush(True);

        self._read_return("syncDir");

    def syncFile(self, fname, server_fname = None, compressionLevel = -1):
        """
        | Synchronize a server file with a local file.
        | This function first sends check sums to send data only when needed.
        | fname is the name of the client file to be synchronized on the server.
        | server_fname is the name of the file on the server. If None it is assumed to be the same as fname.
        | compressionLevel level of zlib compression ranging from 0 (no compression) to 9 (maximum compression).
        """
        self._check_connection();
        
        if type(server_fname) == type(None):
            server_fname = fname;
        
        files = []
        targets = []
        hash_md5 = md5()
        print('Checking "{}"'.format(fname))
        with open(fname, "rb") as fd:
            file_size = fd.seek(0,2)
            fd.seek(0)
            offset = 0
            last_ratio = int(0)
            for chunk in iter(lambda: fd.read(1048576), b""):
                hash_md5.update(chunk)
                offset += len(chunk)

                ratio = int(offset * 100 / file_size)
                if (last_ratio != ratio):
                    last_ratio = ratio
                    print('\r{}%    '.format(ratio), end='', flush=True)
        files.append([fname, hash_md5.hexdigest()])
        targets.append(server_fname)
        print('\r    \r', end='', flush=True)
        params = {
            "dirname" : "./",
            "files" : files,
            "targets" : targets,
            "compressionLevel" : int(compressionLevel),
            "" : "syncDir"
            };
        self._stream.writeQVariantHash(params);
        self._flush(True);

        self._read_return("syncDir");

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
        if (self._sock and b_force):
            self._sock.sendall(b'');

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
        file_reqs = []
        while (self._sock != None and (ret.get("") == None or ret.get("") != COMMAND_ID)):
            self._check_connection();
            ret = self.readQVariantHash();
            # Check if file resend requests are pending
            if ret.get("files2update") != None:
                file_reqs = ret.get("files2update")
                
            if (ret.get("") == None or ret.get("") == "") and self._verbosity_level > 0 and ret.get("data") != None:
                    msg = ret["data"].decode('utf-8');
                    error_level = 3;
                    if msg.find("[error]") != -1:
                        error_level = 1;
                    elif msg.find("[warning]") != -1:
                        error_level = 2;
                    elif msg.find("[info]") != -1:
                        error_level = 3;
                    elif msg.find("[debug]") != -1:
                        error_level = 4;
                    if self._verbosity_level >= error_level:
                        self._printError(msg);
                    if error_level == 1 and (self._exception_on_error or self._exception_on_warning):
                        raise RuntimeError(msg);
                    elif error_level == 2 and self._exception_on_warning:
                        raise RuntimeError(msg);
        
        for req in file_reqs:
            if req.get("requested_file") != None and req.get("dirname") != None and req.get("compressionLevel") != None:
                compressionLevel = req.get("compressionLevel")
                dirname = req.get("dirname")
                fname = req.get("requested_file")
                target = req.get("target")
                if type(target) == type(None):
                    target = fname;
                last_ratio = int(0)
                print('Sending "{}" to server'.format(dirname + "/" + fname))
                with open(dirname + "/" + fname, "rb") as f:
                    file_size = f.seek(0,2)
                    f.seek(0)
                    offset = 0;
                    append = False;
                    for chunk in iter(lambda: f.read(1048576), b""):
                        self.sendFile(target, chunk, compressionLevel, offset, append);
                        offset += len(chunk);
                        append = True;

                        ratio = int(offset * 100 / file_size)
                        if (last_ratio != ratio):
                            last_ratio = ratio
                            print('\r{}%    '.format(ratio), end='', flush=True)
                print('\r    \r', end='', flush=True)
                        
        return ret;

    # This will fail if object is not iterable which is desired behavior
    def _vec(self, v):
        return np.array(v, dtype=np.float64).tolist()

    # This will fail if object is not a 4x4 numpy array
    def _mat44(self, v):
        return [ [ float(v[j,i]) for i in range(4) ] for j in range(4)]

    # Write support functions    
    def _write_int8(self, v):
        self._sock.send(struct.pack('>b', int(v)))
    def _write_uint8(self, v):
        self._sock.send(struct.pack('>B', int(v)))
    def _write_int16(self, v):
        self._sock.send(struct.pack('>h', int(v)))
    def _write_uint16(self, v):
        self._sock.send(struct.pack('>H', int(v)))
    def _write_int32(self, v):
        self._sock.send(struct.pack('>i', int(v)))
    def _write_uint32(self, v):
        self._sock.send(struct.pack('>I', int(v)))
    def _write_int64(self, v):
        self._sock.send(struct.pack('>q', int(v)))
    def _write_uint64(self, v):
        self._sock.send(struct.pack('>Q', int(v)))
    def _write_float32(self, v):
        self._sock.send(struct.pack(">f", float(v)))
    def _write_float64(self, v):
        self._sock.send(struct.pack(">d", float(v)))

    def _write_string(self, v):
        v = str(v)
        if v == '':
            self._write_uint32(0xFFFFFFFF)
            return
        data = v.encode('utf-16be')
        self._write_uint32(len(data))
        self._sock.send(data)

    def _write_map(self, table):
        self._write_uint32(len(table))
        for k in table:
            v = table[k]
            self._write_string(k)
            self._write(v)

    def _write_list(self, table):
        self._write_uint32(len(table))
        for k in table:
            self._write(k)

    def _write_bytearray(self, buffer):
        if len(buffer) == 0:
            self._write_uint32(0xFFFFFFFF)
            return
        self._write_uint32(len(buffer))
        self._sock.send(buffer)
        
    def _write(self, v):
        T = type(v)
        if T == np.float16 or\
            T == np.float32 or\
            T == np.float64 or\
            T == np.float or\
            T == float:
            self._write_uint32(self._DT_Double)
            self._write_uint8(0)
            self._write_float64(v)
        elif T == bool:
            self._write_uint32(self._DT_Bool)
            self._write_uint8(0)
            self._write_uint8(v)
        elif T == np.int8 or\
            T == np.int16 or\
            T == np.int32 or\
            T == np.int64 or\
            T == np.int or\
            T == np.uint8 or\
            T == np.uint16 or\
            T == np.uint32 or\
            T == np.uint64 or\
            T == np.uint or\
            T == int:
            if v >= -2147483648 and v <= 2147483647:
                self._write_uint32(self._DT_Int)
                self._write_uint8(0)
                self._write_int32(v)
            elif v >= 0 and v <= 4294967295:
                self._write_uint32(self._DT_UInt)
                self._write_uint8(0)
                self._write_uint32(v)
            else:
                self._write_uint32(self._DT_ULongLong)
                self._write_uint8(0)
                self._write_uint64(v)
        elif T == str:
            self._write_uint32(self._DT_String)
            self._write_uint8(0)
            self._write_string(v)
        elif T == dict:
            self._write_uint32(self._DT_Hash)
            self._write_uint8(0)
            self._write_map(v)
        elif T == list or T == tuple or T == np.ndarray:    # Interpret tuples and numpy arrays as lists
            self._write_uint32(self._DT_List)
            self._write_uint8(0)
            self._write_list(v)
        elif T == bytes:
            self._write_uint32(self._DT_ByteArray)
            self._write_uint8(0)
            self._write_bytearray(v)
        else:
            self._write_uint32(self._DT_Invalid)
            self._write_uint8(0)

    # Serializes a dictionnary (which maps string to values) as a QHash<QString, QVariant>
    def writeQVariantHash(self, table):
        self._write_uint32(len(table))
        for k in table:
            v = table[k]
            self._write_string(k)
            self._write(v)
        return

    # Read support functions
    def _recv(self, l):
        ret = self._sock.recv(l)
        if ret == b'' or ret == None:
            return b''
        while len(ret) < l:
            buf = self._sock.recv(l - len(ret))
            if buf == b'' or ret == None:
                self._sock = None
                raise RuntimeError('Socket error')
            ret = ret + buf
        return ret;
        
    def _read_uint8(self):
        return struct.unpack('B', self._recv(1))[0];
    def _read_int8(self):
        return struct.unpack('b', self._recv(1))[0];
    def _read_uint16(self):
        return struct.unpack('>H', self._recv(2))[0];
    def _read_int16(self):
        return struct.unpack('>h', self._recv(2))[0];
    def _read_uint32(self):
        return struct.unpack('>I', self._recv(4))[0];
    def _read_int32(self):
        return struct.unpack('>i', self._recv(4))[0];
    def _read_uint64(self):
        return struct.unpack('>Q', self._recv(8))[0];
    def _read_int64(self):
        return struct.unpack('>q', self._recv(8))[0];
    def _read_float32(self):
        return struct.unpack('>f', self._recv(4))[0];
    def _read_float64(self):
        return struct.unpack('>d', self._recv(8))[0];

    def _read_string(self):
        l = self._read_uint32();
        if l == 0xFFFFFFFF:
            return '';
        return self._recv(l).decode('utf-16be');
        
    def _read_map(self):
        nb_elts = self._read_uint32()
        table = {}
        for i in range(nb_elts):
            k = self._read_string()
            table[k] = self._read()
        return table

    def _read_list(self):
        nb_elts = self._read_uint32()
        table = []
        for i in range(nb_elts):
            table.append(self._read())
        return table
        
    def _read_bytearray(self):
        l = self._read_uint32()
        if l == 0 or l == 0xFFFFFFFF:
            return b''
        return self._recv(l)
        
    def _read(self):
        T = self._read_uint32()
        self._read_uint8()
        if T == self._DT_Double:
            return self._read_float64()
        elif T == self._DT_Bool:
            return self._read_uint8() != 0
        elif T == self._DT_Int:
            return self._read_int32()
        elif T == self._DT_UInt:
            return self._read_uint32()
        elif T == self._DT_ULongLong:
            return self._read_uint64()
        elif T == self._DT_String:
            return self._read_string()
        elif T == self._DT_Hash or T == self._DT_Map:
            return self._read_map()
        elif T == self._DT_List:
            return self._read_list()
        elif T == self._DT_ByteArray:
            return self._read_bytearray()
        elif T == self._DT_Invalid:
            return None
        else:
            raise RuntimeError('Unsupported type: {}'.format(T))
            
    # Deserializes a dictionnary (which maps string to values) from a QHash<QString, QVariant>
    def readQVariantHash(self):
        return self._read_map()
    
    # Compression support functions
    def _compress(self, buffer, level):
        buf = zlib.compress(buffer, level)
        return struct.pack('>I', int(len(buf))) + buf
    
    def _uncompress(self, buffer):
        size = struct.unpack('>I', buffer[0:4])[0]
        return zlib.decompress(buffer[4:], bufsize = size)
