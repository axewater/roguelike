"""
Surface Math Module - Geometric utilities for creature body surfaces

Provides core mathematical operations for working with sphere and ellipsoid surfaces:
- Surface projection (ray-surface intersection)
- Surface normals (orientation of features)
- Geodesic distance (spacing on curved surfaces)
- Spherical coordinates (angular positioning)

These functions form the foundation for anatomically-correct creature generation.
"""

import math
import random
from ursina import Vec3


class BodyGeometry:
    """
    Represents the geometric properties of a creature body.
    Supports both spherical and ellipsoidal bodies.
    """

    def __init__(self, size=1.0, shape_type='sphere'):
        """
        Initialize body geometry.

        Args:
            size: Base size/radius of body
            shape_type: 'sphere' or 'ellipsoid'
        """
        self.size = size
        self.shape_type = shape_type

        # Define semi-axes for ellipsoid (a, b, c)
        if shape_type == 'ellipsoid':
            self.a = size          # x-axis radius
            self.b = size * 0.7    # y-axis radius (flattened)
            self.c = size          # z-axis radius
        else:  # sphere
            self.a = size
            self.b = size
            self.c = size

    def is_sphere(self):
        """Check if body is a perfect sphere"""
        return abs(self.a - self.b) < 0.001 and abs(self.b - self.c) < 0.001

    def get_axes(self):
        """Get semi-axes as tuple (a, b, c)"""
        return (self.a, self.b, self.c)

    def get_average_radius(self):
        """Get average radius (useful for rough distance calculations)"""
        return (self.a + self.b + self.c) / 3.0


def spherical_to_cartesian(theta, phi, radius=1.0):
    """
    Convert spherical coordinates to Cartesian (x, y, z).

    Args:
        theta: Azimuthal angle in radians (0 to 2π, around y-axis)
        phi: Polar angle in radians (0 to π, from +y axis)
        radius: Radial distance from origin

    Returns:
        Vec3: Cartesian coordinates
    """
    x = radius * math.sin(phi) * math.cos(theta)
    y = radius * math.cos(phi)
    z = radius * math.sin(phi) * math.sin(theta)
    return Vec3(x, y, z)


def cartesian_to_spherical(position):
    """
    Convert Cartesian coordinates to spherical (theta, phi, r).

    Args:
        position: Vec3 or tuple (x, y, z)

    Returns:
        tuple: (theta, phi, radius)
            theta: azimuthal angle (0 to 2π)
            phi: polar angle (0 to π)
            radius: distance from origin
    """
    if isinstance(position, (tuple, list)):
        x, y, z = position
    else:
        x, y, z = position.x, position.y, position.z

    radius = math.sqrt(x*x + y*y + z*z)

    if radius < 0.0001:
        return (0, 0, 0)

    theta = math.atan2(z, x)  # Azimuthal angle
    phi = math.acos(max(-1.0, min(1.0, y / radius)))  # Polar angle (clamped for safety)

    return (theta, phi, radius)


def project_to_sphere(point, center=(0, 0, 0), radius=1.0):
    """
    Project a point onto a sphere surface.

    Args:
        point: Vec3 or tuple to project
        center: Sphere center
        radius: Sphere radius

    Returns:
        Vec3: Projected point on sphere surface
    """
    if isinstance(point, (tuple, list)):
        point = Vec3(*point)
    if isinstance(center, (tuple, list)):
        center = Vec3(*center)

    direction = point - center
    distance = direction.length()

    if distance < 0.0001:
        # Point is at center, return arbitrary point on surface
        return center + Vec3(radius, 0, 0)

    # Normalize and scale to radius
    return center + (direction / distance) * radius


def project_to_ellipsoid(point, center=(0, 0, 0), semi_axes=(1.0, 1.0, 1.0), max_iterations=10):
    """
    Project a point onto an ellipsoid surface using iterative method.

    For an ellipsoid: (x/a)² + (y/b)² + (z/c)² = 1

    Args:
        point: Vec3 or tuple to project
        center: Ellipsoid center
        semi_axes: Tuple (a, b, c) - semi-axes lengths
        max_iterations: Maximum Newton-Raphson iterations

    Returns:
        Vec3: Projected point on ellipsoid surface
    """
    if isinstance(point, (tuple, list)):
        point = Vec3(*point)
    if isinstance(center, (tuple, list)):
        center = Vec3(*center)

    a, b, c = semi_axes

    # Check if it's actually a sphere
    if abs(a - b) < 0.001 and abs(b - c) < 0.001:
        return project_to_sphere(point, center, a)

    # Translate to ellipsoid-centered coordinates
    p = point - center

    # Handle degenerate case (point at center)
    if p.length() < 0.0001:
        return center + Vec3(a, 0, 0)

    # Use iterative method: scale point to surface along ray from center
    # Start with spherical approximation
    direction = p.normalized()

    # Newton-Raphson to find intersection parameter t
    # We want to find t such that: (tx/a)² + (ty/b)² + (tz/c)² = 1
    t = (a + b + c) / 3.0  # Initial guess (average radius)

    for _ in range(max_iterations):
        # Current point on ray
        x, y, z = direction.x * t, direction.y * t, direction.z * t

        # Evaluate ellipsoid equation
        f = (x/a)**2 + (y/b)**2 + (z/c)**2 - 1.0

        # Derivative
        df_dt = 2 * ((direction.x * x) / (a*a) +
                     (direction.y * y) / (b*b) +
                     (direction.z * z) / (c*c))

        if abs(df_dt) < 0.0001:
            break

        # Newton step
        t_new = t - f / df_dt

        # Check convergence
        if abs(t_new - t) < 0.0001:
            t = t_new
            break

        t = t_new

    # Compute final surface point
    surface_point = center + direction * t
    return surface_point


def get_surface_normal(point, center=(0, 0, 0), semi_axes=(1.0, 1.0, 1.0)):
    """
    Calculate surface normal at a point on an ellipsoid.

    For ellipsoid (x/a)² + (y/b)² + (z/c)² = 1,
    the gradient (normal) is: (2x/a², 2y/b², 2z/c²)

    Args:
        point: Vec3 or tuple on the surface
        center: Ellipsoid center
        semi_axes: Tuple (a, b, c)

    Returns:
        Vec3: Normalized surface normal (pointing outward)
    """
    if isinstance(point, (tuple, list)):
        point = Vec3(*point)
    if isinstance(center, (tuple, list)):
        center = Vec3(*center)

    a, b, c = semi_axes

    # Translate to ellipsoid-centered coordinates
    p = point - center

    # Compute gradient (unnormalized normal)
    normal = Vec3(
        2.0 * p.x / (a * a),
        2.0 * p.y / (b * b),
        2.0 * p.z / (c * c)
    )

    # Normalize
    length = normal.length()
    if length < 0.0001:
        return Vec3(0, 1, 0)  # Degenerate case

    return normal / length


def geodesic_distance_sphere(point1, point2, radius=1.0):
    """
    Calculate geodesic distance between two points on a sphere.

    Uses great circle distance formula.

    Args:
        point1, point2: Vec3 or tuples on sphere surface
        radius: Sphere radius

    Returns:
        float: Arc length distance along sphere surface
    """
    if isinstance(point1, (tuple, list)):
        point1 = Vec3(*point1)
    if isinstance(point2, (tuple, list)):
        point2 = Vec3(*point2)

    # Convert to unit vectors
    v1 = point1.normalized()
    v2 = point2.normalized()

    # Dot product (clamped to avoid numerical errors)
    dot = max(-1.0, min(1.0, v1.dot(v2)))

    # Angle between vectors
    angle = math.acos(dot)

    # Arc length = radius * angle
    return radius * angle


def geodesic_distance_ellipsoid(point1, point2, semi_axes=(1.0, 1.0, 1.0)):
    """
    Approximate geodesic distance between two points on an ellipsoid.

    Uses numerical approximation (true geodesic is complex).
    Approximates as: straight-line distance * correction factor

    Args:
        point1, point2: Vec3 or tuples on ellipsoid surface
        semi_axes: Tuple (a, b, c)

    Returns:
        float: Approximate arc length distance
    """
    if isinstance(point1, (tuple, list)):
        point1 = Vec3(*point1)
    if isinstance(point2, (tuple, list)):
        point2 = Vec3(*point2)

    a, b, c = semi_axes

    # Check if it's actually a sphere
    if abs(a - b) < 0.001 and abs(b - c) < 0.001:
        return geodesic_distance_sphere(point1, point2, a)

    # Use average radius for rough approximation
    avg_radius = (a + b + c) / 3.0

    # Approximate as spherical geodesic with average radius
    # This is not exact but good enough for spacing constraints
    v1 = point1.normalized()
    v2 = point2.normalized()
    dot = max(-1.0, min(1.0, v1.dot(v2)))
    angle = math.acos(dot)

    return avg_radius * angle


def get_hemisphere_region(point, center=(0, 0, 0)):
    """
    Determine which hemisphere region a point is in.

    Args:
        point: Vec3 or tuple
        center: Sphere/ellipsoid center

    Returns:
        dict: {
            'vertical': 'upper' | 'equator' | 'lower',
            'horizontal': 'front' | 'side' | 'back',
            'y_ratio': float (-1 to 1, -1=bottom, 1=top)
        }
    """
    if isinstance(point, (tuple, list)):
        point = Vec3(*point)
    if isinstance(center, (tuple, list)):
        center = Vec3(*center)

    relative = point - center

    # Vertical classification
    y_threshold_upper = 0.3
    y_threshold_lower = -0.3

    if relative.y > y_threshold_upper:
        vertical = 'upper'
    elif relative.y < y_threshold_lower:
        vertical = 'lower'
    else:
        vertical = 'equator'

    # Horizontal classification (based on z-axis, forward is +z in Ursina)
    z_threshold = 0.3

    if relative.z > z_threshold:
        horizontal = 'front'
    elif relative.z < -z_threshold:
        horizontal = 'back'
    else:
        horizontal = 'side'

    # Normalized y ratio
    length = relative.length()
    y_ratio = relative.y / length if length > 0.0001 else 0

    return {
        'vertical': vertical,
        'horizontal': horizontal,
        'y_ratio': y_ratio
    }


def random_point_on_sphere(radius=1.0, seed=None):
    """
    Generate a uniformly random point on a sphere surface.

    Args:
        radius: Sphere radius
        seed: Random seed for reproducibility

    Returns:
        Vec3: Random point on sphere
    """
    if seed is not None:
        rng = random.Random(seed)
    else:
        rng = random

    # Use spherical coordinates with correct distribution
    theta = rng.uniform(0, 2 * math.pi)
    phi = math.acos(2 * rng.uniform(0, 1) - 1)  # Uniform distribution on sphere

    return spherical_to_cartesian(theta, phi, radius)


def random_point_on_ellipsoid(semi_axes=(1.0, 1.0, 1.0), seed=None):
    """
    Generate a random point on an ellipsoid surface.

    Args:
        semi_axes: Tuple (a, b, c)
        seed: Random seed

    Returns:
        Vec3: Random point on ellipsoid
    """
    if seed is not None:
        rng = random.Random(seed)
    else:
        rng = random

    # Generate random spherical coordinates
    theta = rng.uniform(0, 2 * math.pi)
    phi = math.acos(2 * rng.uniform(0, 1) - 1)

    # Convert to unit sphere point
    sphere_point = spherical_to_cartesian(theta, phi, 1.0)

    # Project onto ellipsoid
    return project_to_ellipsoid(sphere_point, (0, 0, 0), semi_axes)


def fibonacci_sphere(num_samples, radius=1.0):
    """
    Generate evenly distributed points on a sphere using Fibonacci spiral.

    This is the gold standard for even sphere sampling.

    Args:
        num_samples: Number of points to generate
        radius: Sphere radius

    Returns:
        list: List of Vec3 points on sphere
    """
    points = []
    phi_golden = math.pi * (3.0 - math.sqrt(5.0))  # Golden angle in radians

    for i in range(num_samples):
        y = 1 - (i / float(num_samples - 1)) * 2  # y goes from 1 to -1
        radius_at_y = math.sqrt(1 - y * y)  # Radius at y

        theta = phi_golden * i

        x = math.cos(theta) * radius_at_y
        z = math.sin(theta) * radius_at_y

        points.append(Vec3(x * radius, y * radius, z * radius))

    return points


def fibonacci_ellipsoid(num_samples, semi_axes=(1.0, 1.0, 1.0)):
    """
    Generate evenly distributed points on an ellipsoid.

    Uses Fibonacci sphere then projects onto ellipsoid.

    Args:
        num_samples: Number of points
        semi_axes: Tuple (a, b, c)

    Returns:
        list: List of Vec3 points on ellipsoid
    """
    # Generate Fibonacci sphere
    sphere_points = fibonacci_sphere(num_samples, 1.0)

    # Project each point onto ellipsoid
    ellipsoid_points = []
    for point in sphere_points:
        projected = project_to_ellipsoid(point, (0, 0, 0), semi_axes)
        ellipsoid_points.append(projected)

    return ellipsoid_points


# Utility function for distance calculations
def euclidean_distance(point1, point2):
    """
    Calculate straight-line Euclidean distance between two points.

    Args:
        point1, point2: Vec3 or tuples

    Returns:
        float: Distance
    """
    if isinstance(point1, (tuple, list)):
        point1 = Vec3(*point1)
    if isinstance(point2, (tuple, list)):
        point2 = Vec3(*point2)

    return (point2 - point1).length()
