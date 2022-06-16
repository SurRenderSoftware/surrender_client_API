# -*- coding: utf-8 -*-
# (C) 2019 Airbus copyright all rights reserved

from surrender.surrender_client_base import surrender_client_base;


class surrender_client(surrender_client_base):
    SURRENDER_CLIENT_GIT_REVISION = "31f49a7f5306a3e94aff57d36d2e25925a83a994";
    def attachDynamicTexture(self, object_name, element_name, texture_name, texture_unit_id):
        """
        | Link a dynamic texture to an element of an object.
        | 'texture_unit_id' is the texture unit (diffuse, specular, normal, emission) which is set to the given texture.
        """
        self._check_connection();
        params = { "" : "attachDynamicTexture"};
        params["object_name"] = str(object_name);
        params["element_name"] = str(element_name);
        params["texture_name"] = str(texture_name);
        params["texture_unit_id"] = int(texture_unit_id);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("attachDynamicTexture");

    def cd(self, path):
        """
        | Change the current resource path.
        | This is similar to the 'cd' command on Linux.
        """
        self._check_connection();
        params = { "" : "cd"};
        params["path"] = str(path);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("cd");

    def clearMetadata(self):
        """
        | Resets the metadata table
        """
        self._check_connection();
        params = { "" : "clearMetadata"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("clearMetadata");

    def createBRDF(self, name, filename, parameters):
        """
        | Create a BRDF object which can be referenced with the name 'name'.
        | The BRDF model is loaded from the SuMoL file 'filename' with the parameters in 'parameters'.
        """
        self._check_connection();
        params = { "" : "createBRDF"};
        params["name"] = str(name);
        params["filename"] = str(filename);
        params["parameters"] = parameters;
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("createBRDF");

    def createBody(self, body_name, shape_name, brdf_name, textures):
        """
        | Create an object with the shape 'shape_name' and BRDF 'brdf_name'.
        | 'textures' contain the textures to be used for (in order):
        |  - diffuse map
        |  - specular map
        |  - emission map
        |  - normal map
        """
        self._check_connection();
        params = { "" : "createBody"};
        params["body_name"] = str(body_name);
        params["shape_name"] = str(shape_name);
        params["brdf_name"] = str(brdf_name);
        params["textures"] = textures;
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("createBody");

    def createDEM(self, object_name, conemap_filename, brdf_name, texture):
        """
        | Create a DEM (Digital Elevation Model) from a '.dem' file. Displacement mapping is done from a plan.
        | The conemap can be built with the build_conemap tool.
        | 'texture' is the texture to be used for the diffuse texture map, empty means default white texture.
        """
        self._check_connection();
        params = { "" : "createDEM"};
        params["object_name"] = str(object_name);
        params["conemap_filename"] = str(conemap_filename);
        params["brdf_name"] = str(brdf_name);
        params["texture"] = str(texture);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("createDEM");
        return ret["info"]

    def createLight(self, light_name, spectrum, cutoff, exponent):
        """
        | Create a spot light.
        | 'spectrum' is the 4D spectrum of the light (in W for each wavelength simulated).
        | 'cutoff' is the maximum angle in degrees from the spot direction where the spot produce light.
        | 'exponent' controls how the power decreases when reaching the cutoff angle. 1 means linear, the higher the flatter it gets.
        """
        self._check_connection();
        params = { "" : "createLight"};
        params["light_name"] = str(light_name);
        params["spectrum"] = self._vec(spectrum);
        params["cutoff"] = float(cutoff);
        params["exponent"] = float(exponent);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("createLight");

    def createMesh(self, object_name, model_name, scale):
        """
        | Create a new mesh object in the scene.
        | 'object_name' is the name of the new object in the scene.
        | 'model_name' is the name of the model file.
        | 'scale' is the scaling factor to apply when loading the model (use 1 if the mesh is in meters, 1e-3 is it is in km, ...)
        """
        self._check_connection();
        params = { "" : "createMesh"};
        params["object_name"] = str(object_name);
        params["model_name"] = str(model_name);
        params["scale"] = float(scale);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("createMesh");

    def createPerPixelProcess(self, name, filename, parameters):
        """
        | Create a PerPixelProcess object for a SuMoL file and a set of parameters.
        | 'name' is used to reference the created object.
        | 
        """
        self._check_connection();
        params = { "" : "createPerPixelProcess"};
        params["name"] = str(name);
        params["filename"] = str(filename);
        params["parameters"] = parameters;
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("createPerPixelProcess");

    def createShape(self, name, filename, parameters):
        """
        | Create a Shape object which can be referenced with the name 'name'.
        | The shape model is loaded from the SuMoL file 'filename' with the parameters in 'parameters'.
        """
        self._check_connection();
        params = { "" : "createShape"};
        params["name"] = str(name);
        params["filename"] = str(filename);
        params["parameters"] = parameters;
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("createShape");

    def createSphericalDEM(self, object_name, conemap_filename, brdf_name, texture):
        """
        | Create a DEM (Digital Elevation Model) from a '.dem' file. Displacement mapping is done from the spherical body described in the DEM/PDS file.
        | The conemap can be built with the build_conemap tool.
        | 'texture' is the texture to be used for the diffuse texture map, empty means default white texture.
        """
        self._check_connection();
        params = { "" : "createSphericalDEM"};
        params["object_name"] = str(object_name);
        params["conemap_filename"] = str(conemap_filename);
        params["brdf_name"] = str(brdf_name);
        params["texture"] = str(texture);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("createSphericalDEM");
        return ret["info"]

    def createUserDataTexture(self, name, width, height, gray):
        """
        | Create a data texture whose content has to be provided by the client.
        | If 'gray' is true, the texture type is Y32F (single channel, float).
        | If 'gray' is false, the texture type is RGBA32F (4 channels, float).
        """
        self._check_connection();
        params = { "" : "createUserDataTexture"};
        params["name"] = str(name);
        params["width"] = int(width);
        params["height"] = int(height);
        params["gray"] = bool(gray);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("createUserDataTexture");

    def createVideoTexture(self, name, filename, loop):
        """
        | Create a new dynamic texture from a video.
        | If 'loop' is true, the video loops indefinitely, otherwise it stops at the last frame.
        """
        self._check_connection();
        params = { "" : "createVideoTexture"};
        params["name"] = str(name);
        params["filename"] = str(filename);
        params["loop"] = bool(loop);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("createVideoTexture");

    def dumpPhotonMapToFile(self, object_name, filename):
        """
        | Dump the photon map of an object to a PLY file.
        """
        self._check_connection();
        params = { "" : "dumpPhotonMapToFile"};
        params["object_name"] = str(object_name);
        params["filename"] = str(filename);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("dumpPhotonMapToFile");

    def enableAutoUpdate(self, enable):
        """
        | Enable (true) or disable (false) automatic update of viewer window after rendering.
        | Default: enabled
        """
        self._check_connection();
        params = { "" : "enableAutoUpdate"};
        params["enable"] = bool(enable);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("enableAutoUpdate");

    def enableDoublePrecisionMode(self, *args, **kwargs):
        """
        | This function is deprecated and has been removed!
        | It has been replaced with a stub function to avoid legacy script failures.
        """
        self._check_connection();
        params = { "" : "enableDoublePrecisionMode"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        self._read_return("enableDoublePrecisionMode");
        return None;

    def enableFastPSFMode(self, *args, **kwargs):
        """
        | This function is deprecated and has been removed!
        | It has been replaced with a stub function to avoid legacy script failures.
        """
        self._check_connection();
        params = { "" : "enableFastPSFMode"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        self._read_return("enableFastPSFMode");
        return None;

    def enableGlobalDynamicShadowMap(self, enable):
        """
        | If true, create a dynamic shadow map to compute sun visibility when rendering all objects
        | This shadow map is global, ie. adapted to exterior environments such as rover simulations or close range rendez-vous.
        | It overrides per object shadow maps.
        | If false, restore the default behavior with per object shadow maps.
        """
        self._check_connection();
        params = { "" : "enableGlobalDynamicShadowMap"};
        params["enable"] = bool(enable);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("enableGlobalDynamicShadowMap");

    def enableIrradianceMode(self, enable):
        """
        | Enable (true) or disable (false) irradiance mode.
        """
        self._check_connection();
        params = { "" : "enableIrradianceMode"};
        params["enable"] = bool(enable);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("enableIrradianceMode");

    def enableLOSmapping(self, b_enable):
        """
        | enable or disable LOS mapping
        | If true, LOS map will be allocated on image generation. Otherwise it is destroyed if one was allocated before.
        | LOS mapping only works in raytracing (in OpenGL you can deduce it from the pinhole model)
        """
        self._check_connection();
        params = { "" : "enableLOSmapping"};
        params["b_enable"] = bool(b_enable);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("enableLOSmapping");

    def enableMultilateralFiltering(self, *args, **kwargs):
        """
        | This function is deprecated and has been removed!
        | It has been replaced with a stub function to avoid legacy script failures.
        """
        self._check_connection();
        params = { "" : "enableMultilateralFiltering"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        self._read_return("enableMultilateralFiltering");
        return None;

    def enablePathTracing(self, enable):
        """
        | Enable (true) or disable (false) pathtracing.
        | Pathtracing requires raytracing to be enabled.
        """
        self._check_connection();
        params = { "" : "enablePathTracing"};
        params["enable"] = bool(enable);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("enablePathTracing");

    def enablePhotonAccumulation(self, enable):
        """
        | Enable (true) or disable (false) photon accumulation mode (Raytracing only).
        | Objects with the photon_map property set to true will be mapped with the energy received.
        | No image will be renderer in this mode!
        """
        self._check_connection();
        params = { "" : "enablePhotonAccumulation"};
        params["enable"] = bool(enable);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("enablePhotonAccumulation");

    def enablePreviewMode(self, enable):
        """
        | Enable (true) or disable (false) preview mode.
        | This mode enables faster OpenGL rendering at the cost of reduced quality.
        """
        self._check_connection();
        params = { "" : "enablePreviewMode"};
        params["enable"] = bool(enable);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("enablePreviewMode");

    def enableRaySharing(self, enable):
        """
        | Enable (true) or disable (false) reuse of rays for neighbors pixels (Raytracing only).
        | This optimization assumes pixels are acquired simultaneously.
        | It only works with SuMoL PSF!!
        """
        self._check_connection();
        params = { "" : "enableRaySharing"};
        params["enable"] = bool(enable);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("enableRaySharing");

    def enableRaytracing(self, enable):
        """
        | Enable (true) or disable (false) raytracing.
        """
        self._check_connection();
        params = { "" : "enableRaytracing"};
        params["enable"] = bool(enable);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("enableRaytracing");

    def enableRegularPSFSampling(self, enable):
        """
        | Enable (true) or disable (false) regular PSF sampling. It implies regular pixel sampling.
        """
        self._check_connection();
        params = { "" : "enableRegularPSFSampling"};
        params["enable"] = bool(enable);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("enableRegularPSFSampling");

    def enableRegularPixelSampling(self, enable):
        """
        | Enable (true) or disable (false) regular pixel sampling. It doesn't affect PSF sampling.
        """
        self._check_connection();
        params = { "" : "enableRegularPixelSampling"};
        params["enable"] = bool(enable);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("enableRegularPixelSampling");

    def enableScanningDeviceMode(self, enable):
        """
        | Enable (true) or disable (false) scanning device mode (Raytracing only).
        | Scanning device mode disables optimizations which assume a typical image projection.
        | This is useful for scanning LiDARs. It has the following characteristics:
        | - simulate a single detector cell (projection model applied to a 1x1 pixel matrix)
        | - does not support rendering stars
        | - PSF tail optimization (blooming) is disabled
        | - RaySharing is disabled
        """
        self._check_connection();
        params = { "" : "enableScanningDeviceMode"};
        params["enable"] = bool(enable);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("enableScanningDeviceMode");

    def enableSkipPixelSampling(self, enable):
        """
        | Enable (true) or disable (false) skipping the pixel surface sampling.
        | Enable only when PSF model is already integrated over the pixel surface otherwise image will be smoother than expected!
        | Default: disabled
        """
        self._check_connection();
        params = { "" : "enableSkipPixelSampling"};
        params["enable"] = bool(enable);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("enableSkipPixelSampling");

    def enableSpecularOptimization(self, enable):
        """
        | Enable a dedicated optimization for sampling specular reflections of the Sun (pathtracing only).
        """
        self._check_connection();
        params = { "" : "enableSpecularOptimization"};
        params["enable"] = bool(enable);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("enableSpecularOptimization");

    def enableTimeMapping(self, b_enable):
        """
        | enable or disable time mapping
        | If true, time map will be allocated on image generation. Otherwise it is destroyed if one was allocated before.
        | Time mapping only works in raytracing
        """
        self._check_connection();
        params = { "" : "enableTimeMapping"};
        params["b_enable"] = bool(b_enable);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("enableTimeMapping");

    def exists(self, object_name):
        """
        | Returns true if an object with the given name already exists.
        | This function checks aliases and builtin objects!
        """
        self._check_connection();
        params = { "" : "exists"};
        params["object_name"] = str(object_name);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("exists");
        return ret["exists"]

    def generateMicroTasks(self):
        """
        | Generate the list of µtasks required to render an image.
        | This is what makes possible to distribute the rendering process of a single image across several machines.
        | 
        | The format of the returned matrix is as follow (everything is encoded as double, types are given as hints):
        | cluster_id(int64), x(int32), y(int32), samples(int32), object_id(int32), start(s), end(s), weight([0-1]), flags(int)
        | 
        | NB: works in raytracing only!
        | WARNING: since cluster_id is stored as double, expect issues with images with width or height above 32.000.000 pixels
        """
        self._check_connection();
        params = { "" : "generateMicroTasks"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("generateMicroTasks");
        return ret["utasks"]

    def getCameraFOVDeg(self):
        """
        | Return camera field of view in degrees.
        """
        self._check_connection();
        params = { "" : "getCameraFOVDeg"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("getCameraFOVDeg");
        return ret["fov"]

    def getCameraFOVRad(self):
        """
        | Return camera field of view in radians.
        """
        self._check_connection();
        params = { "" : "getCameraFOVRad"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("getCameraFOVRad");
        return ret["fov"]

    def getConventions(self):
        """
        | Get the active conventions for quaternions and camera frame definition.
        """
        self._check_connection();
        params = { "" : "getConventions"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("getConventions");
        return ret["conventions"]

    def getCubeMapSize(self):
        """
        | Return the size of cube maps when creating new meshes.
        """
        self._check_connection();
        params = { "" : "getCubeMapSize"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("getCubeMapSize");
        return ret["cube_map_size"]

    def getDoublePrecisionMode(self, *args, **kwargs):
        """
        | This function is deprecated and has been removed!
        | It has been replaced with a stub function to avoid legacy script failures.
        """
        self._check_connection();
        params = { "" : "getDoublePrecisionMode"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        self._read_return("getDoublePrecisionMode");
        return None;

    def getGlobalVariables(self):
        """
        | Return the values of active global SuMoL variables.
        | 
        """
        self._check_connection();
        params = { "" : "getGlobalVariables"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("getGlobalVariables");
        return ret["names_and_values"]

    def getImageSize(self):
        """
        | Return the size of the image.
        """
        self._check_connection();
        params = { "" : "getImageSize"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("getImageSize");
        return ret["size"]

    def getIntegrationTime(self):
        """
        | Return integration time in seconds.
        """
        self._check_connection();
        params = { "" : "getIntegrationTime"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("getIntegrationTime");
        return ret["integration_time"]

    def getIrradianceMode(self):
        """
        | Return true if irradiance mode is enabled, false otherwise.
        """
        self._check_connection();
        params = { "" : "getIrradianceMode"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("getIrradianceMode");
        return ret["enable"]

    def getLOSmapping(self):
        """
        | return true is LOS mapping is enabled, false otherwise.
        """
        self._check_connection();
        params = { "" : "getLOSmapping"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("getLOSmapping");
        return ret["b_enable"]

    def getMaxSamplesPerPixel(self):
        """
        | Return the maximum number of samples allowed per pixel.
        """
        self._check_connection();
        params = { "" : "getMaxSamplesPerPixel"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("getMaxSamplesPerPixel");
        return ret["max_samples"]

    def getMaxSecondaryRays(self):
        """
        | Return the number of secondary rays used for pathtracing.
        """
        self._check_connection();
        params = { "" : "getMaxSecondaryRays"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("getMaxSecondaryRays");
        return ret["max_secondary_rays"]

    def getMaxShadowRays(self):
        """
        | Get the maximum number of rays used for direct shadows.
        | Default is 4.
        """
        self._check_connection();
        params = { "" : "getMaxShadowRays"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("getMaxShadowRays");
        return ret["max_shadow_rays"]

    def getMetadata(self):
        """
        | Returns the metadata table
        """
        self._check_connection();
        params = { "" : "getMetadata"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("getMetadata");
        return ret["metadata"]

    def getNbSamplesPerPixel(self):
        """
        | Return the number of samples per pixel.
        """
        self._check_connection();
        params = { "" : "getNbSamplesPerPixel"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("getNbSamplesPerPixel");
        return ret["nb_samples"]

    def getObjectAttitude(self, object_name):
        """
        | Return the attitude of object 'object_name'.
        | Use 'camera' as object name to get the attitude of the camera.
        """
        self._check_connection();
        params = { "" : "getObjectAttitude"};
        params["object_name"] = str(object_name);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("getObjectAttitude");
        return ret["attitude"]

    def getObjectDynamicCubeMap(self, object_name):
        """
        | Return true if object 'object_name' has dynamic cube maps, false otherwise.
        | A dynamic cube map is updated at each frame whereas a static one is kept as is.
        | This is an OpenGL only option.
        """
        self._check_connection();
        params = { "" : "getObjectDynamicCubeMap"};
        params["object_name"] = str(object_name);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("getObjectDynamicCubeMap");
        return ret["enable"]

    def getObjectDynamicShadowMap(self, object_name):
        """
        | Return true if object 'object_name' has dynamic shadow maps, false otherwise.
        | A dynamic shadow map is updated at each frame whereas a static one is kept as is.
        | This is an OpenGL only option.
        """
        self._check_connection();
        params = { "" : "getObjectDynamicShadowMap"};
        params["object_name"] = str(object_name);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("getObjectDynamicShadowMap");
        return ret["enable"]

    def getObjectElementProperty(self, name, element_name, property):
        """
        | Return the value of property 'property' for element 'element_name' in object 'name'.
        """
        self._check_connection();
        params = { "" : "getObjectElementProperty"};
        params["name"] = str(name);
        params["element_name"] = str(element_name);
        params["property"] = str(property);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("getObjectElementProperty");
        return ret["value"]

    def getObjectMotion(self, object_name):
        """
        | Return motion parameters for object 'object_name'.
        """
        self._check_connection();
        params = { "" : "getObjectMotion"};
        params["object_name"] = str(object_name);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("getObjectMotion");
        return ret["motion"]

    def getObjectPosition(self, object_name):
        """
        | Return the position of object 'object_name'.
        | Use 'camera' as object name to get the position of the camera.
        """
        self._check_connection();
        params = { "" : "getObjectPosition"};
        params["object_name"] = str(object_name);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("getObjectPosition");
        return ret["pos"]

    def getObjectProperty(self, name, property):
        """
        | Return the value of property 'property' for object 'name'.
        """
        self._check_connection();
        params = { "" : "getObjectProperty"};
        params["name"] = str(name);
        params["property"] = str(property);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("getObjectProperty");
        return ret["value"]

    def getObjectSamples(self, object_name):
        """
        | Return the required number of rays for object 'object_name'.
        """
        self._check_connection();
        params = { "" : "getObjectSamples"};
        params["object_name"] = str(object_name);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("getObjectSamples");
        return ret["nb_samples"]

    def getPhotonMapSamplingStep(self):
        """
        | Return the sampling step for photon maps.
        """
        self._check_connection();
        params = { "" : "getPhotonMapSamplingStep"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("getPhotonMapSamplingStep");
        return ret["step"]

    def getPreviewMode(self):
        """
        | Return true if preview mode is enabled, false otherwise.
        """
        self._check_connection();
        params = { "" : "getPreviewMode"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("getPreviewMode");
        return ret["enable"]

    def getRessourcePath(self):
        """
        | Return current path to ressource files.
        """
        self._check_connection();
        params = { "" : "getRessourcePath"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("getRessourcePath");
        return ret["ressource_path"]

    def getScanningDeviceMode(self):
        """
        | Return the status of scanning device mode.
        """
        self._check_connection();
        params = { "" : "getScanningDeviceMode"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("getScanningDeviceMode");
        return ret["enable"]

    def getSelfVisibilitySamplingStep(self):
        """
        | Return the sampling step for self visibility maps.
        """
        self._check_connection();
        params = { "" : "getSelfVisibilitySamplingStep"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("getSelfVisibilitySamplingStep");
        return ret["step"]

    def getShadowMapSize(self):
        """
        | Return the size of shadow maps when creating new meshes.
        """
        self._check_connection();
        params = { "" : "getShadowMapSize"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("getShadowMapSize");
        return ret["shadow_map_size"]

    def getState(self):
        """
        | Return the state of the scene manager as a string.
        | This state contains position,attitude,motion of all objects in the scene as well as renderer settings.
        """
        self._check_connection();
        params = { "" : "getState"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("getState");
        return ret["state"]

    def getSunPower(self):
        """
        | Return the power of the sun.
        """
        self._check_connection();
        params = { "" : "getSunPower"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("getSunPower");
        return ret["sun_power"]

    def getTimeMapping(self):
        """
        | return true is time mapping is enabled, false otherwise.
        """
        self._check_connection();
        params = { "" : "getTimeMapping"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("getTimeMapping");
        return ret["b_enable"]

    def help(self, function_name):
        """
        | Print the available documentation for function 'function_name'.
        """
        self._check_connection();
        params = { "" : "help"};
        params["function_name"] = str(function_name);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("help");
        print(ret['help']);
        return ret["help"]

    def intersectScene(self, rays):
        """
        | Compute the intersection of a set of rays with the scene
        | Each ray is stored as a (position,direction) pair in a std::vector/list
        | Returns the distance to the hit along each ray.
        """
        self._check_connection();
        params = { "" : "intersectScene"};
        params["rays"] = rays;
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("intersectScene");
        return ret["distance_to_hit"]

    def loadAndProjectMultipleMeshes(self, object_name, mesh_names, positions, attitudes, projection_center, offset_ratio):
        """
        | Like loadMultipleMeshes it loads a list of meshes with the given positions and attitudes into a single object.
        | A quaternion on the unit sphere is a simple rotation, otherwise its norm is interpreted as a scaling factor.
        | The difference with loadMultipleMeshes is the projection of the given position onto the scene towards a projection center.
        | This point is defined in homogeneous coordinates and can be set at inifinity by setting its last coordinate to 0.
        | The last parameter is the offset, relative to the radius of each instance's bounding sphere, from the surface to the center of each object.
        | An offset_ratio of 0 means the center is on the surface, 1 means a sphere would be at the limit of penetrating the surface.
        """
        self._check_connection();
        params = { "" : "loadAndProjectMultipleMeshes"};
        params["object_name"] = str(object_name);
        params["mesh_names"] = mesh_names;
        params["positions"] = positions;
        params["attitudes"] = attitudes;
        params["projection_center"] = self._vec(projection_center);
        params["offset_ratio"] = float(offset_ratio);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("loadAndProjectMultipleMeshes");

    def loadMotionModel(self, filename, parameters):
        """
        | Load a motion model written in SuMoL from the file 'filename' with the parameters in 'parameters'.
        | A motion model defines the camera motion during image acquisition, it can also define microvibrations.
        """
        self._check_connection();
        params = { "" : "loadMotionModel"};
        params["filename"] = str(filename);
        params["parameters"] = parameters;
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("loadMotionModel");

    def loadMultipleMeshes(self, object_name, mesh_names, positions, attitudes):
        """
        | Load a list of meshes with the given positions and attitudes into a single object.
        | A quaternion on the unit sphere is a simple rotation, otherwise its norm is interpreted as a scaling factor.
        """
        self._check_connection();
        params = { "" : "loadMultipleMeshes"};
        params["object_name"] = str(object_name);
        params["mesh_names"] = mesh_names;
        params["positions"] = positions;
        params["attitudes"] = attitudes;
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("loadMultipleMeshes");

    def loadPSFModel(self, filename, parameters):
        """
        | Load a PSF model written in SuMoL from the file 'filename' with the parameters in 'parameters'.
        | A PSF model defines the PSF integral.
        """
        self._check_connection();
        params = { "" : "loadPSFModel"};
        params["filename"] = str(filename);
        params["parameters"] = parameters;
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("loadPSFModel");

    def loadProjectionModel(self, filename, parameters):
        """
        | Load a projection model written in SuMoL from the file 'filename' with the parameters in 'parameters'.
        | A projection model defines both the projection to image plane and the optical distortion.
        """
        self._check_connection();
        params = { "" : "loadProjectionModel"};
        params["filename"] = str(filename);
        params["parameters"] = parameters;
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("loadProjectionModel");

    def loadSpectrumModel(self, filename, parameters):
        """
        | Load a Spectrum model written in SuMoL from the file 'filename' with the parameters in 'parameters'.
        | A Spectrum model defines how a 4D color spectrum is converted into a continuous one and how the spectrum is sampled.
        | This is required to simulate achromatism (with a PSF model with a dependency to lambda).
        """
        self._check_connection();
        params = { "" : "loadSpectrumModel"};
        params["filename"] = str(filename);
        params["parameters"] = parameters;
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("loadSpectrumModel");

    def loadTextureObject(self, name, filename, parameters):
        """
        | Load a texture. It can be any supported type of image format.
        | It can also be a procedural texture model written in SuMoL from the file 'filename' with the parameters in 'parameters' and give it the the name 'name'.
        | A procedural texture model describes a 2D or 3D texture (4D color spectrum) using lookup functions.
        """
        self._check_connection();
        params = { "" : "loadTextureObject"};
        params["name"] = str(name);
        params["filename"] = str(filename);
        params["parameters"] = parameters;
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("loadTextureObject");

    def loadTimeSamplingModel(self, filename, parameters):
        """
        | Load a sampling model (raytracing) which defines when and for how long pixels gather light.
        | The model is loaded from the SuMoL file 'filename' with the parameters 'parameters'.
        """
        self._check_connection();
        params = { "" : "loadTimeSamplingModel"};
        params["filename"] = str(filename);
        params["parameters"] = parameters;
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("loadTimeSamplingModel");

    def ls(self):
        """
        | List the content of the current resource path
        | This is similar to the 'ls -lh' command on Linux.
        """
        self._check_connection();
        params = { "" : "ls"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("ls");
        print(ret['listing']);
        return ret["listing"]

    def printAPI(self):
        """
        | List all the functions of the client API.
        """
        self._check_connection();
        params = { "" : "printAPI"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("printAPI");
        print(ret['api']);
        return ret["api"]

    def printObjectStructure(self, object_name):
        """
        | Print the structure of object 'object_name'.
        """
        self._check_connection();
        params = { "" : "printObjectStructure"};
        params["object_name"] = str(object_name);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("printObjectStructure");
        print(ret['object_structure']);
        return ret["object_structure"]

    def printState(self, state):
        """
        | Generates a human readable string representation of a saved state.
        """
        self._check_connection();
        params = { "" : "printState"};
        params["state"] = str(state);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("printState");
        print(ret['readable_state']);
        return ret["readable_state"]

    def pwd(self):
        """
        | Return the current resource path.
        | This is similar to the 'pwd' command on Linux.
        """
        self._check_connection();
        params = { "" : "pwd"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("pwd");
        print(ret['path']);
        return ret["path"]

    def render(self):
        """
        | Render an image with current parameters.
        """
        self._check_connection();
        params = { "" : "render"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("render");

    def renderMicroTasks(self, utasks):
        """
        | Render an image using a pregenerated list of µtasks
        | This is what makes possible to distribute the rendering process of a single image across several machines.
        | Using this function one can generate only a fraction of an image which can be split to be generated on several machines in parallel.
        | 
        | NB: works in raytracing only
        """
        self._check_connection();
        params = { "" : "renderMicroTasks"};
        params["utasks"] = utasks;
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("renderMicroTasks");

    def reset(self):
        """
        | Reset the engine.
        | All ressources are freed, all scene objects/elements are deleted.
        """
        self._check_connection();
        params = { "" : "reset"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("reset");

    def runPerPixelProcess(self, output_name, process_name):
        """
        | Run a function on each pixel of a texture.
        | If 'output_name' is empty, it targets the framebuffer (rendered image buffer).
        | You must create the PerPixelProcess object first with createPerPixelProcess.
        """
        self._check_connection();
        params = { "" : "runPerPixelProcess"};
        params["output_name"] = str(output_name);
        params["process_name"] = str(process_name);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("runPerPixelProcess");

    def saveDepthMap(self, filename):
        """
        | Save the depth map in file 'filename'. Only TIF format is supported.
        """
        self._check_connection();
        params = { "" : "saveDepthMap"};
        params["filename"] = str(filename);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("saveDepthMap");

    def saveImage(self, filename):
        """
        | Save the image in file 'filename'. File format is guessed from extension.
        | [0-1] range is mapped to 8bits when required.
        """
        self._check_connection();
        params = { "" : "saveImage"};
        params["filename"] = str(filename);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("saveImage");

    def saveImageGray32F(self, filename):
        """
        | Save the image in file 'filename'. File format is guessed from extension.
        | The first 3 channels are averaged and the result is stored in float format.
        """
        self._check_connection();
        params = { "" : "saveImageGray32F"};
        params["filename"] = str(filename);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("saveImageGray32F");

    def saveImageGray8(self, filename):
        """
        | Save the image in file 'filename'. File format is guessed from extension.
        | [0-1] range is mapped to 8bits and the first 3 channels are averaged.
        """
        self._check_connection();
        params = { "" : "saveImageGray8"};
        params["filename"] = str(filename);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("saveImageGray8");

    def saveImageRGB8(self, filename):
        """
        | Save the image in file 'filename'. File format is guessed from extension.
        | [0-1] range is mapped to 8bits and only the first 3 channels are considered.
        """
        self._check_connection();
        params = { "" : "saveImageRGB8"};
        params["filename"] = str(filename);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("saveImageRGB8");

    def saveImageSpectrumProjection(self, filename, spectrum):
        """
        | Save the image in file 'filename'. File format is guessed from extension.
        | The 4 channels are weighted according to the 'spectrum' parameter and the result is stored in float format.
        """
        self._check_connection();
        params = { "" : "saveImageSpectrumProjection"};
        params["filename"] = str(filename);
        params["spectrum"] = self._vec(spectrum);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("saveImageSpectrumProjection");

    def saveImageSpectrumProjectionQuantized(self, filename, spectrum, nbits):
        """
        | Save the image in file 'filename'. File format is guessed from extension.
        | The 4 channels are weighted according to the 'spectrum' parameter and the result is stored in integer 8/16bits format after quantization.
        | This last step is done using 'nbits' to define the valid range. If nbits <= 8, the result is stored in an 8bits image, otherwise it is stored in a 16bits image.
        """
        self._check_connection();
        params = { "" : "saveImageSpectrumProjectionQuantized"};
        params["filename"] = str(filename);
        params["spectrum"] = self._vec(spectrum);
        params["nbits"] = int(nbits);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("saveImageSpectrumProjectionQuantized");

    def saveObject(self, object_name, filename):
        """
        | Save object 'object_name' to file 'filename'.
        """
        self._check_connection();
        params = { "" : "saveObject"};
        params["object_name"] = str(object_name);
        params["filename"] = str(filename);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("saveObject");

    def setAlias(self, object_name, alias):
        """
        | Create an alias for an existing object.
        """
        self._check_connection();
        params = { "" : "setAlias"};
        params["object_name"] = str(object_name);
        params["alias"] = str(alias);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setAlias");

    def setBackground(self, background):
        """
        | Set the background to render: either a spherical texture or a star map.
        """
        self._check_connection();
        params = { "" : "setBackground"};
        params["background"] = str(background);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setBackground");

    def setCameraFOVDeg(self, fov_x, fov_y):
        """
        | Set camera field of view in degrees.
        """
        self._check_connection();
        params = { "" : "setCameraFOVDeg"};
        params["fov_x"] = float(fov_x);
        params["fov_y"] = float(fov_y);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setCameraFOVDeg");

    def setCameraFOVRad(self, fov_x, fov_y):
        """
        | Set camera field of view in radians.
        """
        self._check_connection();
        params = { "" : "setCameraFOVRad"};
        params["fov_x"] = float(fov_x);
        params["fov_y"] = float(fov_y);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setCameraFOVRad");

    def setConventions(self, quaternion_convention, camera_convention):
        """
        | Set the conventions for quaternions and camera frame definition.
        """
        self._check_connection();
        params = { "" : "setConventions"};
        params["quaternion_convention"] = int(quaternion_convention);
        params["camera_convention"] = int(camera_convention);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setConventions");

    def setCubeMapSize(self, cube_map_size):
        """
        | Set the size of cube maps when creating new meshes.
        """
        self._check_connection();
        params = { "" : "setCubeMapSize"};
        params["cube_map_size"] = cube_map_size;
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setCubeMapSize");

    def setCubeMapZNear(self, znear):
        """
        | Set the distance (in meters) of the near plane when rendering cubemaps. Default is 10km.
        """
        self._check_connection();
        params = { "" : "setCubeMapZNear"};
        params["znear"] = float(znear);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setCubeMapZNear");

    def setFSAA(self, fsaa):
        """
        | Set the super sampling factor in OpenGL mode. 1 means disabled.
        | The number of samples per pixel is equal to this parameter squared.
        | Disabled by default.
        """
        self._check_connection();
        params = { "" : "setFSAA"};
        params["fsaa"] = int(fsaa);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setFSAA");

    def setFocus(self, focus_plane_Z, pupil_radius):
        """
        | Set parameters for defocus/depth of field simulation.
        | If focus_plane_Z or pupil_radius is set to 0, defocus/depth of field is not simulated.
        | 
        | Default: disabled
        """
        self._check_connection();
        params = { "" : "setFocus"};
        params["focus_plane_Z"] = float(focus_plane_Z);
        params["pupil_radius"] = float(pupil_radius);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setFocus");

    def setGlobalVariables(self, names_and_values):
        """
        | Set the values of a set of global SuMoL variables.
        | NB: this only affects globals for already loaded SuMoL models. When loading a new model its globals will be kept at their default values!
        """
        self._check_connection();
        params = { "" : "setGlobalVariables"};
        params["names_and_values"] = names_and_values;
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setGlobalVariables");

    def setImageSize(self, width, height):
        """
        | Set image size.
        """
        self._check_connection();
        params = { "" : "setImageSize"};
        params["width"] = width;
        params["height"] = height;
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setImageSize");

    def setIntegrationTime(self, integration_time):
        """
        | Set integration time in seconds.
        | NB: if using a sensor model, please refer to its API instead of this function.
        """
        self._check_connection();
        params = { "" : "setIntegrationTime"};
        params["integration_time"] = float(integration_time);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setIntegrationTime");

    def setMaxSamplesPerPixel(self, max_samples):
        """
        | Set the maximum number of samples per pixel when dynamically increased to reduce noise on edges.
        """
        self._check_connection();
        params = { "" : "setMaxSamplesPerPixel"};
        params["max_samples"] = int(max_samples);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setMaxSamplesPerPixel");

    def setMaxSecondaryRays(self, max_secondary_rays):
        """
        | Set the maximum number of secondary rays (default is 4) when pathtracing is enabled.
        """
        self._check_connection();
        params = { "" : "setMaxSecondaryRays"};
        params["max_secondary_rays"] = int(max_secondary_rays);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setMaxSecondaryRays");

    def setMaxShadowRays(self, max_shadow_rays):
        """
        | Set the maximum number of rays used for direct shadows.
        | Default is 4.
        """
        self._check_connection();
        params = { "" : "setMaxShadowRays"};
        params["max_shadow_rays"] = int(max_shadow_rays);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setMaxShadowRays");

    def setMetadata(self, name, value):
        """
        | Add, update or remove a metadata
        | If value is empty, the metadata is removed
        | Metadata are used when sending images over TCP. This is typically used to store timestamps and image IDs.
        """
        self._check_connection();
        params = { "" : "setMetadata"};
        params["name"] = str(name);
        params["value"] = value;
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setMetadata");

    def setNbSamplesPerPixel(self, nb_samples):
        """
        | Set the number of samples per pixel (raytracing).
        """
        self._check_connection();
        params = { "" : "setNbSamplesPerPixel"};
        params["nb_samples"] = int(nb_samples);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setNbSamplesPerPixel");

    def setNearPlane(self, z):
        """
        | Set the distance of the near plane (OpenGL only). Objects or parts of objects closer than this distance won't be rendered.
        """
        self._check_connection();
        params = { "" : "setNearPlane"};
        params["z"] = float(z);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setNearPlane");

    def setObjectAttitude(self, object_name, attitude):
        """
        | Set the attitude of object 'object_name'.
        | Use 'camera' as object name to change the attitude of the camera.
        """
        self._check_connection();
        params = { "" : "setObjectAttitude"};
        params["object_name"] = str(object_name);
        params["attitude"] = self._vec(attitude);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setObjectAttitude");

    def setObjectDynamicCubeMap(self, object_name, enable):
        """
        | Enable (true) or disable (false) dynamic cube maps for object 'object_name'.
        | A dynamic cube map is updated at each frame whereas a static one is kept as is.
        | This is an OpenGL only option.
        """
        self._check_connection();
        params = { "" : "setObjectDynamicCubeMap"};
        params["object_name"] = str(object_name);
        params["enable"] = bool(enable);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setObjectDynamicCubeMap");

    def setObjectDynamicShadowMap(self, object_name, enable):
        """
        | Enable (true) or disable (false) dynamic shadow maps for object 'object_name'.
        | A dynamic shadow map is updated at each frame whereas a static one is kept as is.
        | This is an OpenGL only option.
        """
        self._check_connection();
        params = { "" : "setObjectDynamicShadowMap"};
        params["object_name"] = str(object_name);
        params["enable"] = bool(enable);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setObjectDynamicShadowMap");

    def setObjectElementBRDF(self, object_name, element_name, brdf):
        """
        | Set the BRDF for an element of an object.
        | If 'object_name' = 'element_name' the BRDF is applied to the whole object.
        """
        self._check_connection();
        params = { "" : "setObjectElementBRDF"};
        params["object_name"] = str(object_name);
        params["element_name"] = str(element_name);
        params["brdf"] = str(brdf);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setObjectElementBRDF");

    def setObjectElementProperty(self, name, element_name, property, value):
        """
        | Set property 'property' to 'value' for element 'element_name' in object 'name'.
        | Available properties are:
        | photon_map_sampling_step          Sampling step (distance between samples) for this element in the photon map.
        |                                   If 0, no samples will be generated for this object.
        |                                   If < 0.0, density is inherited from parent node.
        """
        self._check_connection();
        params = { "" : "setObjectElementProperty"};
        params["name"] = str(name);
        params["element_name"] = str(element_name);
        params["property"] = str(property);
        params["value"] = float(value);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setObjectElementProperty");

    def setObjectElementTransform(self, object_name, element_name, matrix, relative):
        """
        | Set the local (relative = true) or global (relative = false) transformation
        | of an element of an object. 'matrix' is a 4x4 matrix representing this transformation.
        """
        self._check_connection();
        params = { "" : "setObjectElementTransform"};
        params["object_name"] = str(object_name);
        params["element_name"] = str(element_name);
        params["matrix"] = self._mat44(matrix);
        params["relative"] = bool(relative);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setObjectElementTransform");

    def setObjectMotion(self, object_name, motion):
        """
        | Set motion parameters (speed & rotation speed) for object 'object_name'.
        """
        self._check_connection();
        params = { "" : "setObjectMotion"};
        params["object_name"] = str(object_name);
        params["motion"] = [ self._vec(motion[0]), self._vec(motion[1]) ];
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setObjectMotion");

    def setObjectPosition(self, object_name, pos):
        """
        | Set the position of object 'object_name'.
        | Use 'camera' as object name to change the position of the camera.
        """
        self._check_connection();
        params = { "" : "setObjectPosition"};
        params["object_name"] = str(object_name);
        params["pos"] = self._vec(pos);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setObjectPosition");

    def setObjectProperty(self, name, property, value):
        """
        | Set property 'property' to 'value' for object 'name'.
        | Available properties are:
        | photon_map (boolean)              If true object will have a photon map to accumulate energy received on its surface.
        | normal_map_object_space (boolean) If true normal maps are read in object frame instead of tangent space.
        | skip_path_tracing (boolean)       If true the object won't be sampled as a secondary light source when pathtracing is enabled.
        """
        self._check_connection();
        params = { "" : "setObjectProperty"};
        params["name"] = str(name);
        params["property"] = str(property);
        params["value"] = float(value);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setObjectProperty");

    def setObjectSamples(self, object_name, nb_samples):
        """
        | Set a quota of samples to cast over an object.
        | Surrender will cast at least that many primary rays toward this object.
        """
        self._check_connection();
        params = { "" : "setObjectSamples"};
        params["object_name"] = str(object_name);
        params["nb_samples"] = float(nb_samples);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setObjectSamples");

    def setPSFSigma(self, sigma):
        """
        | Set the sigma parameter of a gaussian PSF in OpenGL mode. 0.0 means disabled.
        | Disabled by default.
        """
        self._check_connection();
        params = { "" : "setPSFSigma"};
        params["sigma"] = float(sigma);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setPSFSigma");

    def setPhotonMapSamplingStep(self, step):
        """
        | Set the sampling step for generating photon maps (for meshes) in pathtracing.
        | Default value is 1e-1. Reducing this value produces better results but requires more memory and more processing time (more rays).
        """
        self._check_connection();
        params = { "" : "setPhotonMapSamplingStep"};
        params["step"] = float(step);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setPhotonMapSamplingStep");

    def setRessourcePath(self, ressource_path):
        """
        | Set the reference path (server side) to access ressources (models, textures, ...).
        """
        self._check_connection();
        params = { "" : "setRessourcePath"};
        params["ressource_path"] = str(ressource_path);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setRessourcePath");

    def setSelfVisibilitySamplingStep(self, step):
        """
        | Set the sampling step for generating self visibility maps (for meshes) in pathtracing.
        | Default value is 1e-1. Reducing this value produces better results but requires more memory and more preprocessing time.
        """
        self._check_connection();
        params = { "" : "setSelfVisibilitySamplingStep"};
        params["step"] = float(step);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setSelfVisibilitySamplingStep");

    def setShadowMapSize(self, shadow_map_size):
        """
        | Set the size of shadow maps when creating new meshes.
        """
        self._check_connection();
        params = { "" : "setShadowMapSize"};
        params["shadow_map_size"] = shadow_map_size;
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setShadowMapSize");

    def setStarThreshold(self, threshold):
        """
        | Set the lowest value (in W/m^2) for a star to be rendered.
        | If any spectrum component is above this threshold the star will be rendered otherwise it will be ignored.
        | Default is 0.
        | 
        | NB: applies only to raytracing
        | 
        """
        self._check_connection();
        params = { "" : "setStarThreshold"};
        params["threshold"] = float(threshold);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setStarThreshold");

    def setState(self, state):
        """
        | Restores a previously saved state of the scene manager.
        | This will restore position,attitude,motion of all objects in the scene as well as renderer settings.
        | Objects are not created, they must exist in the scene before restoring the scene state.
        """
        self._check_connection();
        params = { "" : "setState"};
        params["state"] = str(state);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setState");

    def setSunPower(self, sun_color):
        """
        | Set the power emitted by the Sun for each wave length simulated.
        | This is expressed in W/sr.
        """
        self._check_connection();
        params = { "" : "setSunPower"};
        params["sun_color"] = self._vec(sun_color);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setSunPower");

    def setSunPowerAtDistance(self, sun_color, distance):
        """
        | Set the received from the Sun for each wave length simulated at a given distance.
        | This is expressed in W/m² for the power and in m for the distance.
        """
        self._check_connection();
        params = { "" : "setSunPowerAtDistance"};
        params["sun_color"] = self._vec(sun_color);
        params["distance"] = float(distance);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("setSunPowerAtDistance");

    def updateDisplay(self):
        """
        | Update viewer window on the server side.
        | This is useful after framebuffer has been modified with a PerPixelProcess
        """
        self._check_connection();
        params = { "" : "updateDisplay"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("updateDisplay");

    def updateDynamicTexture(self, name):
        """
        | Trigger an update of the dynamic texture 'name'.
        """
        self._check_connection();
        params = { "" : "updateDynamicTexture"};
        params["name"] = str(name);
        self._stream.writeQVariantHash(params);
        self._flush(True);
        if not self._async:
            ret = self._read_return("updateDynamicTexture");

    def version(self):
        """
        | Returns the server version number and GIT revision if available.
        """
        self._check_connection();
        params = { "" : "version"};
        self._stream.writeQVariantHash(params);
        self._flush(True);
        ret = self._read_return("version");
        return ret["version"]

