"""
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
  ker = np.arange(N, dtype=np.float64) - (N - 1) / 2
  ker = np.meshgrid(ker, ker)
  ker = np.exp(-(ker[0] * ker[0] + ker[1] * ker[1]) / (2 * sigma * sigma))
  ker = ker / np.sum(ker)
  return ker


def vec3(x, y = None, z = None):
  """
  Build a 3 dimensions vector from canonical components
  Args:
   x: (float) First component
   y: (float) Second component
   z: (float) Third component
  Returns: (numpy.array) 3d vector
  """
  if y == None:
    return np.array([x, x, x], dtype=np.float64)
  return np.array([x, y, z], dtype=np.float64)


def vec4(x, y = None, z = None, w = None):
  """
  Build a 4 dimensions vector from canonical components
  Args:
   x: (float) First component
   y: (float) Second component 
   z: (float) Third component
   w: (float) Fourth component
  Returns: (numpy.array) 4d vector
  """
  if y == None:
    return np.array([x, x, x, x], dtype=np.float64)
  return np.array([x, y, z, w], dtype=np.float64)


def quat(axis, angle):
  """
  Get a quaternion from an axis and an oriented angle
  Args:
   axis: (numpy.array or list) Axis vector
   angle: (float) Rotation angle
  Returns: (numpy.array) Quaternion
  """
  axis = normalize(axis) * np.sin(angle / 2)
  return np.array([np.cos(angle / 2), axis[0], axis[1], axis[2]], dtype=np.float64)


def quat_mult(q2, q1):
  """
  Return the product of two quaternions
  NB: the resulting product is the quaternion that first rotates by q1, then by q2 (the order is the same as matrix product or rotation composition)
  :param q1: (1x4 numpy.array)
  :param q2: (1x4 numpy.array)
  :return: (1x4 numpy.array)
  """
  a1, a2 = q1[0], q2[0]
  u1, u2 = q1[1:], q2[1:]
  a = a2 * a1 - np.dot(u2, u1)
  u = a2 * u1 + a1 * u2 + np.cross(u2, u1)
  q = normalize(np.array([a, u[0], u[1], u[2]], dtype=np.float64))

  return q


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
  v = np.array(v, dtype=np.float64)
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

def look_at_star(surrender_client, right_ascension, declination):
  """
  Point the camera towards a star, given its right ascension and declination.
  The camera is assumed to be located at [0, 0, 0], i.e., at the center of the Earth
  NB: In the J2000 frame, the x-axis corresponds to RA = 0h, dec = 0° (vernal equinox), the y-axis corresponds to RA = 6h, dec = 0° et the z-axis to dec = 90°.

  Args:
    surrender_client: (surrender.surrender_client) the SurRender session
    right_ascension: (float|str) if float, angle in radians; if str, must be in the H_M_S[.s] format, e.g., '6_45_8.91728' (6h 45m 8.91728s) for Sirius  
    declination: (float|str) if float, angle in radians; if str, must be in the D_M_S[.s] format, e.g. '-16_42_58.02' (-16 deg 42m 58.02s) for Sirius
  """
  assert isinstance(right_ascension, (float, int, str)), \
    f'Right ascension ({right_ascension}) should be provided either as a number in radians or as a string with H_M_S.s format'
  assert isinstance(declination, (float, int, str)), \
    f'Declination ({declination}) should be provided either as a number in radians or as a string with D_M_S.s format'
  
  DEG_TO_RAD = np.pi / 180
  SECOND_TO_RAD = np.pi / 43200

  # Get RA in rad
  if isinstance(right_ascension, str):
    hms = right_ascension.split('_')
    h, m, s = [float(u) for u in hms]
    ra = ((h * 60 + m) * 60 + s) * SECOND_TO_RAD
  else:
    ra = right_ascension

  # Get dec in rad
  if isinstance(declination, str):
    if declination[0] == '-':
      sign = -1
      dms = declination[1:].split('_')
    else:
      sign = 1
      dms = declination.split('_')
    d, m, s = [float(u) for u in dms]
    dec = sign * ((s / 60 + m) / 60 + d) * DEG_TO_RAD
  else:
    dec = declination

  # Determine LoS of the star
  u = vec3(np.cos(ra) * np.cos(dec), np.sin(ra) * np.cos(dec), np.sin(dec))

  # Compute quaternion to point towards this los
  u_proj = vec3(np.cos(ra), np.sin(ra), 0.)
  q_z_to_x = quat(axis=vec3(0, 1, 0), angle=np.pi / 2)
  q_straighten = quat(axis=vec3(1, 0, 0), angle=-np.pi / 2)
  q_x_to_u_proj = quat(axis=vec3(0, 0, 1), angle=ra)
  q_u_proj_to_u = quat(axis=normalize(np.cross(u_proj, u)), angle=np.abs(dec))
  q_z_to_u = quat_mult(q_u_proj_to_u, quat_mult(q_x_to_u_proj, quat_mult(q_straighten, q_z_to_x)))
  q = q_z_to_u.copy()

  # Store conventions before modifying scene just in case
  conventions = surrender_client.getConventions()
  surrender_client.setConventions(surrender_client.SCALAR_XYZ_CONVENTION, surrender_client.Z_FRONTWARD)
  # Update camera
  surrender_client.setObjectPosition('camera', vec3(0, 0, 0))
  surrender_client.setObjectAttitude('camera', q)
  # Restore conventions
  surrender_client.setConventions(conventions[0], conventions[1])
  