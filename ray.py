import numpy as np

from utils import *

"""
Core implementation of the ray tracer.  This module contains the classes (Sphere, Mesh, etc.)
that define the contents of scenes, as well as classes (Ray, Hit) and functions (shade) used in 
the rendering algorithm, and the main entry point `render_image`.

In the documentation of these classes, we indicate the expected types of arguments with a
colon, and use the convention that just writing a tuple means that the expected type is a
NumPy array of that shape.  Implementations can assume these types are preconditions that
are met, and if they fail for other type inputs it's an error of the caller.  (This might 
not be the best way to handle such validation in industrial-strength code but we are adopting
this rule to keep things simple and efficient.)
"""


class Ray:

    def __init__(self, origin, direction, start=0., end=np.inf):
        """Create a ray with the given origin and direction.

        Parameters:
          origin : (3,) -- the start point of the ray, a 3D point
          direction : (3,) -- the direction of the ray, a 3D vector (not necessarily normalized)
          start, end : float -- the minimum and maximum t values for intersections
        """
        # Convert these vectors to double to help ensure intersection
        # computations will be done in double precision
        self.origin = np.array(origin, np.float64)
        self.direction = np.array(direction, np.float64)
        self.start = start
        self.end = end


class Material:

    def __init__(self, k_d, k_s=0., p=20., k_m=0., k_a=None):
        """Create a new material with the given parameters.

        Parameters:
          k_d : (3,) -- the diffuse coefficient
          k_s : (3,) or float -- the specular coefficient
          p : float -- the specular exponent
          k_m : (3,) or float -- the mirror reflection coefficient
          k_a : (3,) -- the ambient coefficient (defaults to match diffuse color)
        """
        self.k_d = k_d
        self.k_s = k_s
        self.p = p
        self.k_m = k_m
        self.k_a = k_a if k_a is not None else k_d


class Hit:

    def __init__(self, t, point=None, normal=None, material=None):
        """Create a Hit with the given data.

        Parameters:
          t : float -- the t value of the intersection along the ray
          point : (3,) -- the 3D point where the intersection happens
          normal : (3,) -- the 3D outward-facing unit normal to the surface at the hit point
          material : (Material) -- the material of the surface
        """
        self.t = t
        self.point = point
        self.normal = normal
        self.material = material


# Value to represent absence of an intersection
no_hit = Hit(np.inf)


class Sphere:

    def __init__(self, center, radius, material):
        """Create a sphere with the given center and radius.

        Parameters:
          center : (3,) -- a 3D point specifying the sphere's center
          radius : float -- a Python float specifying the sphere's radius
          material : Material -- the material of the surface
        """
        self.center = center
        self.radius = radius
        self.material = material

    def intersect(self, ray):
        """Computes the first (smallest t) intersection between a ray and this sphere.

        Parameters:
          ray : Ray -- the ray to intersect with the sphere
        Return:
          Hit -- the hit data
        """
        # TODO A4 implement this function
        D = ray.direction
        E = ray.origin
        C = self.center
        R = self.radius
        B = 2*np.dot(D, E-C)
        A = np.dot(D, D)

        discriminant = B ** 2 - 4 * A * (np.dot(E-C, E-C)-R**2)

        if discriminant < 0:
            return no_hit

        t0 = (-1*B - np.sqrt(discriminant)) / (2*A)
        t1 = (-1*B + np.sqrt(discriminant)) / (2*A)

        if t0 >= 0 and t1 >= 0:
            t = t0
        elif t0 < 0 and t1 >= 0:
            t = t1
        elif t0 < 0 and t1 < 0:
            return no_hit

        P = E + t * D

        unit_normal = (P - C) / R

        return Hit(t, P, unit_normal, self.material)

        """D = ray.direction
        P = ray.origin
        C = self.center
        R = self.radius
        L = C - P
        tca = np.dot(L, D)
        if tca < 0:
            return no_hit
        discriminate = np.dot(L, L) ** 2  - np.dot(tca, tca)
        if discriminate < 0 or discriminate > R:
            return no_hit
        thc = np.sqrt(R**2 - discriminate**2)
        t0 = tca - thc
        t1 = tca + thc
        p0 = P + t0 * D
        p1 = P + t1 * D
        diff0 = np.sum(P - p0)
        diff1 = np.sum(P - p1)
        if diff0 > diff1:
            final_t = t1
            final_p = p1
        else:
            final_t = t0
            final_p = t1
        normal = normalize(final_t)
        return Hit(final_t, final_p, normal, self.material)"""


class Triangle:

    def __init__(self, vs, material):
        """Create a triangle from the given vertices.

        Parameters:
          vs (3,3) -- an arry of 3 3D points that are the vertices (CCW order)
          material : Material -- the material of the surface
        """
        self.vs = vs
        self.material = material

    def intersect(self, ray):
        """Computes the intersection between a ray and this triangle, if it exists.

        Parameters:
          ray : Ray -- the ray to intersect with the triangle
        Return:
          Hit -- the hit data
        """
        # TODO A4 implement this function
        return no_hit


class Camera:

    def __init__(self, eye=vec([0, 0, 0]), target=vec([0, 0, -1]), up=vec([0, 1, 0]),
                 vfov=90.0, aspect=1.0):
        """Create a camera with given viewing parameters.

        Parameters:
          eye : (3,) -- the camera's location, aka viewpoint (a 3D point)
          target : (3,) -- where the camera is looking: a 3D point that appears centered in the view
          up : (3,) -- the camera's orientation: a 3D vector that appears straight up in the view
          vfov : float -- the full vertical field of view in degrees
          aspect : float -- the aspect ratio of the camera's view (ratio of width to height)
        """
        self.eye = eye
        self.aspect = aspect
        # TODO A4 implement this constructor to store whatever you need for ray generation
        self.up = up
        self.vfov = vfov
        self.target = target

    def generate_ray(self, img_point):
        """Compute the ray corresponding to a point in the image.

        Parameters:
          img_point : (2,) -- a 2D point in [0,1] x [0,1], where (0,0) is the lower left 
                      corner of the image and (1,1) is the upper right
        Return:
          Ray -- The ray corresponding to that image location (not necessarily normalized)
        """
        # TODO A4 implement this function
        i = img_point[0]
        j = img_point[1]
        left = -0.5
        right = 0.5
        bottom = -0.5
        top = 0.5
        eye = self.eye
        up = self.up
        vert_angle = np.radians(self.vfov)
        view_direction = self.target
        height = top - bottom  # figure out
        width = right - left  # figure out
        proj_dist = height // 2.0 // np.tan(vert_angle // 2.0)  # figure out
        look_at_pt = self.target  # figure out
        w_vec = normalize(eye - look_at_pt)  # figure out
        u_vec = normalize(np.cross(up, w_vec))
        v_vec = np.cross(w_vec, u_vec)

        ray_origin = eye
        ray_direction = ((-1) * proj_dist * w_vec) + i * u_vec + j * v_vec
        return Ray(ray_origin, ray_direction)


class PointLight:

    def __init__(self, position, intensity):
        """Create a point light at given position and with given intensity

        Parameters:
          position : (3,) -- 3D point giving the light source location in scene
          intensity : (3,) or float -- RGB or scalar intensity of the source
        """
        self.position = position
        self.intensity = intensity

    def illuminate(self, ray, hit, scene):
        """Compute the shading at a surface point due to this light.

        Parameters:
          ray : Ray -- the ray that hit the surface
          hit : Hit -- the hit data
          scene : Scene -- the scene, for shadow rays
        Return:
          (3,) -- the light reflected from the surface
        """
        # TODO A4 implement this function
        return vec([0, 0, 0])


class AmbientLight:

    def __init__(self, intensity):
        """Create an ambient light of given intensity

        Parameters:
          intensity (3,) or float: the intensity of the ambient light
        """
        self.intensity = intensity

    def illuminate(self, ray, hit, scene):
        """Compute the shading at a surface point due to this light.

        Parameters:
          ray : Ray -- the ray that hit the surface
          hit : Hit -- the hit data
          scene : Scene -- the scene, for shadow rays
        Return:
          (3,) -- the light reflected from the surface
        """
        # TODO A4 implement this function
        return vec([0, 0, 0])


class Scene:

    def __init__(self, surfs, bg_color=vec([0.2, 0.3, 0.5])):
        """Create a scene containing the given objects.

        Parameters:
          surfs : [Sphere, Triangle] -- list of the surfaces in the scene
          bg_color : (3,) -- RGB color that is seen where no objects appear
        """
        self.surfs = surfs
        self.bg_color = bg_color

    def intersect(self, ray):
        """Computes the first (smallest t) intersection between a ray and the scene.

        Parameters:
          ray : Ray -- the ray to intersect with the scene
        Return:
          Hit -- the hit data
        """
        # TODO A4 implement this function
        return no_hit


MAX_DEPTH = 4


def shade(ray, hit, scene, lights, depth=0):
    """Compute shading for a ray-surface intersection.

    Parameters:
      ray : Ray -- the ray that hit the surface
      hit : Hit -- the hit data
      scene : Scene -- the scene
      lights : [PointLight or AmbientLight] -- the lights
      depth : int -- the recursion depth so far
    Return:
      (3,) -- the color seen along this ray
    When mirror reflection is being computed, recursion will only proceed to a depth
    of MAX_DEPTH, with zero contribution beyond that depth.
    """
    # TODO A4 implement this function
    return vec([0, 0, 0])


def render_image(camera, scene, lights, nx, ny):
    """Render a ray traced image.

    Parameters:
      camera : Camera -- the camera defining the view
      scene : Scene -- the scene to be rendered
      lights : Lights -- the lights illuminating the scene
      nx, ny : int -- the dimensions of the rendered image
    Returns:
      (ny, nx, 3) float32 -- the RGB image
    """
    # TODO A4 implement this function
    return np.zeros((ny, nx, 3), np.float32)
