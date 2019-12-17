"""
# (C) 2019 Airbus copyright all rights reserved
Geometry handling functions
"""

__author__ = 'berjaoui'
__date__ = '10/07/2018'

import numpy as np

def gaussian(N, sigma):
  """
  Generate a 2D gaussian kernel

  Args:
    N: (int) Kernel size
    sigma: (float) Kernel std
  Returns: (numpy.array) Gaussian kernel
  """
  ker = np.arange(N) - (N - 1) / 2
  ker = np.meshgrid(ker, ker)
  ker = np.exp(-(ker[0] * ker[0] + ker[1] * ker[1]) / (2 * sigma * sigma))
  ker = ker / np.sum(ker)
  return ker


def vec3(x, y, z):
  """
    Build a 4 dimensions vector from canonical components
    Args:
     x: (float) First component
     y: (float) Second component
     z: (float) Third component
    Returns: (numpy.array) 4d vector
    """
  return np.array([x, y, z])


def vec4(x, y, z, w):
  """
  Build a 4 dimensions vector from canonical components
  Args:
   x: (float) First component
   y: (float) Second component 
   z: (float) Third component
   w: (float) Fourth component
  Returns: (numpy.array) 4d vector
  """
  return np.array([x, y, z, w])


def quat(axis, angle):
  """
  Get a quaternion from an axis and an oriented angle
  Args:
   axis: (numpy.array or list) Axis vector
   angle: (float) Rotation angle
  Returns: (numpy.array) Quaternion
  """
  axis = normalize(axis) * np.sin(angle / 2)
  return np.array([np.cos(angle / 2), axis[0], axis[1], axis[2]])


def norm(v):
  """
  Get the L2 canonical norm of a vector
  Args:
    v: (numpy.array) Vector
  Returns: (float) Norm
  """
  return np.sqrt(np.dot(v, v))


def normalize(v):
  """
  Normalize an array
  Args:
   v: (numpy.array) Numpy array to normalize
  Returns:
    (numpy.array) Normalized array
  """
  v = np.array(v)
  nv = norm(v)
  if nv > 1e-16:
    return v / nv
  return v


def QuatToMat(q):
  """
  Convert a quaternion into a rotation matrix
  Args
   q: (numpy.array) quaternion
  Returns:
    (numpy.array) Rotation matrix
  """
  q = normalize(q)
  W = q[0]
  X = q[1]
  Y = q[2]
  Z = q[3]

  M = np.zeros((3, 3))
  M[0, 0] = 1.0 - 2.0 * Y * Y - 2.0 * Z * Z
  M[0, 1] = 2.0 * X * Y - 2.0 * Z * W
  M[0, 2] = 2.0 * X * Z + 2.0 * Y * W
  M[1, 0] = 2.0 * X * Y + 2.0 * Z * W
  M[1, 1] = 1.0 - 2.0 * X * X - 2.0 * Z * Z
  M[1, 2] = 2.0 * Y * Z - 2.0 * X * W
  M[2, 0] = 2.0 * X * Z - 2.0 * Y * W
  M[2, 1] = 2.0 * Y * Z + 2.0 * X * W
  M[2, 2] = 1.0 - 2.0 * X * X - 2.0 * Y * Y
  return M


def MatToQuat(R):
  """
  Convert a rotation matrix to a quaternion

  Args:
    R: (numpy.array) Rotation matrix

  Returns: (numpy.array) quaternion
  """
  angle_axis = vec3(R[2, 1] - R[1, 2],
                    R[0, 2] - R[2, 0],
                    R[1, 0] - R[0, 1])
  sin_theta = np.sqrt(np.dot(angle_axis, angle_axis)) * 0.5
  cos_theta = (R[0, 0] + R[1, 1] + R[2, 2]) * 0.5 - 0.5
  angle_axis = normalize(angle_axis)
  theta = np.arctan2(sin_theta, cos_theta)
  return quat(angle_axis, theta)

def quaternion_from_vec_to_vec(a, b):
  """
  Compute a quaternion which transforms normalize(a) in normalize(b)

  Args:
    a: (numpy.array) 3D vector
    b: (numpy.array) 3D vector

  Returns: (numpy.array) quaternion
  """
  ab = np.cross(a, b);
  if norm(ab) > 1e-16:
      ab = normalize(ab);
  else:
      ab = vec3(1,0,0);
  return quat(ab, np.arccos(np.dot(normalize(b), normalize(a))))

def look_at(s, eye_pos, target_pos):
  """
  Set the camera at eye_pos and an attitude such that viewing direction is looking to target_pos.

  Args:
    s: (surrender.surrender_client) The SurRender session
    eye_pos: (numpy.array) 3D vector
    target_pos: (numpy.array) 3D vector
  """
  conventions = s.getConventions()
  s.setConventions(s.SCALAR_XYZ_CONVENTION, s.Z_BACKWARD);
      
  s.setObjectPosition("camera", eye_pos)
  s.setObjectAttitude("camera", quaternion_from_vec_to_vec(vec3(0,0,-1), target_pos - eye_pos))
  s.setConventions(conventions[0], conventions[1]);
