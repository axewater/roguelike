"""
Poisson Disk Sampling - Even distribution on curved surfaces

Implements Bridson's algorithm adapted for spherical and ellipsoidal surfaces.
Ensures features (spikes, eyes, etc.) are evenly spaced with minimum distance constraints.

This prevents clustering and creates natural-looking distributions.
"""

import math
import random
from ursina import Vec3
from surface_math import (
    geodesic_distance_sphere,
    geodesic_distance_ellipsoid,
    random_point_on_sphere,
    random_point_on_ellipsoid,
    spherical_to_cartesian,
    cartesian_to_spherical,
    BodyGeometry
)


class PoissonSampler:
    """
    Generates Poisson disk samples on sphere/ellipsoid surfaces.

    Uses Bridson's algorithm adapted for curved surfaces with geodesic distance.
    """

    def __init__(self, body_geometry, min_distance, max_attempts=30, seed=None):
        """
        Initialize Poisson sampler.

        Args:
            body_geometry: BodyGeometry instance defining the surface
            min_distance: Minimum geodesic distance between samples
            max_attempts: Maximum attempts to place each sample
            seed: Random seed for reproducibility
        """
        self.body_geometry = body_geometry
        self.min_distance = min_distance
        self.max_attempts = max_attempts
        self.seed = seed
        self.rng = random.Random(seed)

        # Spatial grid for fast neighbor lookups
        # Grid cells in spherical coordinates (theta, phi)
        avg_radius = body_geometry.get_average_radius()
        self.cell_size = min_distance / avg_radius  # Angular size in radians
        self.grid = {}  # (theta_idx, phi_idx) -> list of points

        # Active list for sampling
        self.active_list = []
        self.samples = []
        self.exclusion_zones = []  # List of {center, radius} dicts

    def add_exclusion_zone(self, center, radius):
        """
        Add an exclusion zone where samples cannot be placed.

        Args:
            center: Vec3 center of exclusion zone
            radius: Geodesic radius of exclusion zone
        """
        self.exclusion_zones.append({
            'center': center if isinstance(center, Vec3) else Vec3(*center),
            'radius': radius
        })

    def _get_grid_cell(self, point):
        """
        Get grid cell index for a point.

        Args:
            point: Vec3 on surface

        Returns:
            tuple: (theta_idx, phi_idx)
        """
        theta, phi, _ = cartesian_to_spherical(point)

        # Normalize to 0-2π and 0-π
        theta = theta % (2 * math.pi)
        if theta < 0:
            theta += 2 * math.pi

        theta_idx = int(theta / self.cell_size)
        phi_idx = int(phi / self.cell_size)

        return (theta_idx, phi_idx)

    def _get_nearby_cells(self, point, radius_cells=2):
        """
        Get nearby grid cells within radius.

        Args:
            point: Vec3 on surface
            radius_cells: Number of cells to search in each direction

        Returns:
            list: List of (theta_idx, phi_idx) tuples
        """
        center_theta_idx, center_phi_idx = self._get_grid_cell(point)

        nearby_cells = []
        for dt in range(-radius_cells, radius_cells + 1):
            for dp in range(-radius_cells, radius_cells + 1):
                nearby_cells.append((center_theta_idx + dt, center_phi_idx + dp))

        return nearby_cells

    def _is_valid_sample(self, point):
        """
        Check if a sample is valid (respects minimum distance and exclusion zones).

        Args:
            point: Vec3 on surface

        Returns:
            bool: True if valid
        """
        # Check exclusion zones
        for zone in self.exclusion_zones:
            if self.body_geometry.is_sphere():
                dist = geodesic_distance_sphere(
                    point,
                    zone['center'],
                    self.body_geometry.a
                )
            else:
                dist = geodesic_distance_ellipsoid(
                    point,
                    zone['center'],
                    self.body_geometry.get_axes()
                )

            if dist < zone['radius']:
                return False

        # Check minimum distance to existing samples
        nearby_cells = self._get_nearby_cells(point, radius_cells=2)

        for cell in nearby_cells:
            if cell in self.grid:
                for existing_point in self.grid[cell]:
                    # Calculate geodesic distance
                    if self.body_geometry.is_sphere():
                        dist = geodesic_distance_sphere(
                            point,
                            existing_point,
                            self.body_geometry.a
                        )
                    else:
                        dist = geodesic_distance_ellipsoid(
                            point,
                            existing_point,
                            self.body_geometry.get_axes()
                        )

                    if dist < self.min_distance:
                        return False

        return True

    def _add_sample(self, point):
        """
        Add a valid sample to the grid and lists.

        Args:
            point: Vec3 on surface
        """
        self.samples.append(point)
        self.active_list.append(point)

        # Add to grid
        cell = self._get_grid_cell(point)
        if cell not in self.grid:
            self.grid[cell] = []
        self.grid[cell].append(point)

    def _generate_candidate(self, reference_point):
        """
        Generate a candidate point near a reference point.

        Args:
            reference_point: Vec3 reference point on surface

        Returns:
            Vec3: Candidate point (may not be valid)
        """
        # Convert to spherical coordinates
        theta, phi, _ = cartesian_to_spherical(reference_point)

        # Generate random offset (between min_distance and 2*min_distance)
        avg_radius = self.body_geometry.get_average_radius()
        angular_min = self.min_distance / avg_radius
        angular_max = 2.0 * angular_min

        offset_angle = self.rng.uniform(angular_min, angular_max)
        offset_direction = self.rng.uniform(0, 2 * math.pi)

        # Apply offset in spherical coordinates
        new_theta = theta + offset_angle * math.cos(offset_direction)
        new_phi = phi + offset_angle * math.sin(offset_direction)

        # Clamp phi to valid range [0, π]
        new_phi = max(0, min(math.pi, new_phi))

        # Generate point at these coordinates
        if self.body_geometry.is_sphere():
            return spherical_to_cartesian(new_theta, new_phi, self.body_geometry.a)
        else:
            # For ellipsoid, first generate on unit sphere then project
            sphere_point = spherical_to_cartesian(new_theta, new_phi, 1.0)
            from surface_math import project_to_ellipsoid
            return project_to_ellipsoid(
                sphere_point,
                (0, 0, 0),
                self.body_geometry.get_axes()
            )

    def generate_samples(self, target_count=None, initial_point=None):
        """
        Generate Poisson disk samples on the surface.

        Args:
            target_count: Target number of samples (None = fill surface)
            initial_point: Initial seed point (None = random)

        Returns:
            list: List of Vec3 sample points
        """
        # Reset state
        self.active_list.clear()
        self.samples.clear()
        self.grid.clear()

        # Generate initial point
        if initial_point is None:
            if self.body_geometry.is_sphere():
                initial_point = random_point_on_sphere(
                    self.body_geometry.a,
                    seed=self.rng.randint(0, 999999)
                )
            else:
                initial_point = random_point_on_ellipsoid(
                    self.body_geometry.get_axes(),
                    seed=self.rng.randint(0, 999999)
                )

        # Validate and add initial point
        if self._is_valid_sample(initial_point):
            self._add_sample(initial_point)

        # Main Poisson loop
        while self.active_list and (target_count is None or len(self.samples) < target_count):
            # Pick random active point
            active_idx = self.rng.randint(0, len(self.active_list) - 1)
            reference_point = self.active_list[active_idx]

            # Try to generate a valid candidate
            found_valid = False
            for _ in range(self.max_attempts):
                candidate = self._generate_candidate(reference_point)

                if self._is_valid_sample(candidate):
                    self._add_sample(candidate)
                    found_valid = True
                    break

            # If no valid candidate found, remove from active list
            if not found_valid:
                self.active_list.pop(active_idx)

        return self.samples.copy()


def generate_hemisphere_samples(body_geometry, hemisphere='lower', min_distance=0.5,
                                 max_samples=None, seed=None):
    """
    Generate Poisson samples constrained to a hemisphere.

    Args:
        body_geometry: BodyGeometry instance
        hemisphere: 'upper', 'lower', or 'equator'
        min_distance: Minimum geodesic distance
        max_samples: Maximum number of samples
        seed: Random seed

    Returns:
        list: Vec3 sample points
    """
    sampler = PoissonSampler(body_geometry, min_distance, seed=seed)

    # Add exclusion zones for opposite hemisphere
    if hemisphere == 'lower':
        # Exclude upper hemisphere (y > 0.3)
        # Create multiple exclusion zones to cover top
        for i in range(8):
            angle = (2 * math.pi / 8) * i
            x = body_geometry.a * 0.5 * math.cos(angle)
            z = body_geometry.c * 0.5 * math.sin(angle)
            y = body_geometry.b * 0.8
            sampler.add_exclusion_zone(Vec3(x, y, z), body_geometry.get_average_radius() * 0.6)

    elif hemisphere == 'upper':
        # Exclude lower hemisphere (y < -0.3)
        for i in range(8):
            angle = (2 * math.pi / 8) * i
            x = body_geometry.a * 0.5 * math.cos(angle)
            z = body_geometry.c * 0.5 * math.sin(angle)
            y = -body_geometry.b * 0.8
            sampler.add_exclusion_zone(Vec3(x, y, z), body_geometry.get_average_radius() * 0.6)

    # Generate samples
    return sampler.generate_samples(target_count=max_samples)


def generate_ring_samples(body_geometry, y_position=0, y_tolerance=0.3,
                          num_samples=8, seed=None):
    """
    Generate evenly-spaced samples in a ring around the body.

    Args:
        body_geometry: BodyGeometry instance
        y_position: Height of ring (-1 to 1, relative to body)
        y_tolerance: Vertical tolerance
        num_samples: Number of samples in ring
        seed: Random seed

    Returns:
        list: Vec3 sample points
    """
    rng = random.Random(seed)
    samples = []

    for i in range(num_samples):
        angle = (2 * math.pi / num_samples) * i
        # Add slight random variation
        angle += rng.uniform(-0.1, 0.1)

        # For sphere, use simple circular placement
        if body_geometry.is_sphere():
            # Calculate radius at this y position
            y = y_position * body_geometry.b
            radius_at_y = math.sqrt(max(0, body_geometry.a**2 - y**2))

            x = radius_at_y * math.cos(angle)
            z = radius_at_y * math.sin(angle)

            samples.append(Vec3(x, y, z))
        else:
            # For ellipsoid, use parametric form
            from surface_math import spherical_to_cartesian, project_to_ellipsoid

            # Calculate phi from y_position
            phi = math.acos(max(-1, min(1, y_position)))

            # Generate point
            sphere_point = spherical_to_cartesian(angle, phi, 1.0)
            ellipsoid_point = project_to_ellipsoid(
                sphere_point,
                (0, 0, 0),
                body_geometry.get_axes()
            )
            samples.append(ellipsoid_point)

    return samples


def filter_samples_by_region(samples, body_geometry, region_filter):
    """
    Filter samples by hemisphere region.

    Args:
        samples: List of Vec3 points
        body_geometry: BodyGeometry instance
        region_filter: Function that takes (point) -> bool

    Returns:
        list: Filtered Vec3 points
    """
    filtered = []
    for sample in samples:
        if region_filter(sample):
            filtered.append(sample)
    return filtered
