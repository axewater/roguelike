"""
Constraint Solver - Intelligent placement of creature parts

Implements Constraint Satisfaction Problem (CSP) solver for anatomically-correct
part placement. Uses priority-based greedy placement with backtracking.

Constraints enforced:
1. Parts must be in valid zones
2. Minimum spacing between parts (geodesic distance)
3. Exclusion zones around existing parts
4. Maximum part counts
5. Collision avoidance
"""

import random
from ursina import Vec3
from surface_math import (
    BodyGeometry,
    geodesic_distance_sphere,
    geodesic_distance_ellipsoid,
    project_to_sphere,
    project_to_ellipsoid,
    get_surface_normal,
    fibonacci_sphere,
    fibonacci_ellipsoid
)
from anatomy_graph import CreatureAnatomyGraph, AttachmentPoint
from poisson_sampling import PoissonSampler, generate_hemisphere_samples, generate_ring_samples


class ConstraintSolver:
    """
    Solves creature anatomy constraints to generate valid attachment points.

    Uses multi-phase approach:
    1. Generate candidate positions (Fibonacci + Poisson sampling)
    2. Filter by zones
    3. Apply constraints (spacing, exclusions)
    4. Place parts in priority order
    """

    def __init__(self, anatomy_graph, seed=None):
        """
        Initialize constraint solver.

        Args:
            anatomy_graph: CreatureAnatomyGraph instance
            seed: Random seed for reproducibility
        """
        self.graph = anatomy_graph
        self.body_geometry = anatomy_graph.body_geometry
        self.seed = seed
        self.rng = random.Random(seed)

        # Solver state
        self.placed_points = []  # List of placed AttachmentPoints
        self.exclusion_zones = []  # List of {center, radius} dicts

    def _geodesic_distance(self, point1, point2):
        """
        Calculate geodesic distance between two points.

        Args:
            point1, point2: Vec3 points on surface

        Returns:
            float: Geodesic distance
        """
        if self.body_geometry.is_sphere():
            return geodesic_distance_sphere(
                point1,
                point2,
                self.body_geometry.a
            )
        else:
            return geodesic_distance_ellipsoid(
                point1,
                point2,
                self.body_geometry.get_axes()
            )

    def _is_in_exclusion_zone(self, point):
        """
        Check if point is in any exclusion zone.

        Args:
            point: Vec3 point to check

        Returns:
            bool: True if in exclusion zone
        """
        for zone in self.exclusion_zones:
            dist = self._geodesic_distance(point, zone['center'])
            if dist < zone['radius']:
                return True
        return False

    def _add_exclusion_zone(self, center, radius):
        """
        Add an exclusion zone.

        Args:
            center: Vec3 center
            radius: Geodesic radius
        """
        self.exclusion_zones.append({
            'center': center,
            'radius': radius
        })

    def _check_spacing_constraint(self, point, part_type, min_spacing):
        """
        Check if point respects minimum spacing from existing parts.

        Args:
            point: Vec3 point to check
            part_type: Type of part
            min_spacing: Minimum required spacing

        Returns:
            bool: True if spacing is valid
        """
        # Check against all placed points of same type
        for placed in self.placed_points:
            if placed.part_type == part_type:
                dist = self._geodesic_distance(point, placed.position)
                if dist < min_spacing:
                    return False

        # Check exclusion zones
        if self._is_in_exclusion_zone(point):
            return False

        return True

    def _generate_candidate_positions(self, part_type, target_count):
        """
        Generate candidate positions for a part type.

        Uses different strategies based on part type.

        Args:
            part_type: Type of part
            target_count: Target number of positions

        Returns:
            list: List of Vec3 candidate positions
        """
        rule = self.graph.get_rule(part_type)
        if not rule:
            return []

        candidates = []

        # Strategy depends on part type
        if part_type == 'tentacle':
            # Tentacles: Use hemisphere sampling (lower hemisphere)
            candidates = generate_hemisphere_samples(
                self.body_geometry,
                hemisphere='lower',
                min_distance=rule.min_spacing * 0.8,  # Slightly tighter for more candidates
                max_samples=target_count * 3,  # Generate extra candidates
                seed=self.seed
            )

        elif part_type == 'eye':
            # Eyes: Use Poisson sampling on upper/front hemisphere
            sampler = PoissonSampler(
                self.body_geometry,
                min_distance=rule.min_spacing * 0.8,
                seed=self.seed
            )

            # Add exclusion for bottom hemisphere
            for i in range(8):
                angle = (2 * 3.14159 / 8) * i
                import math
                x = self.body_geometry.a * 0.5 * math.cos(angle)
                z = self.body_geometry.c * 0.5 * math.sin(angle)
                y = -self.body_geometry.b * 0.8
                sampler.add_exclusion_zone(Vec3(x, y, z), self.body_geometry.get_average_radius() * 0.6)

            candidates = sampler.generate_samples(target_count=target_count * 3)

        elif part_type == 'spike':
            # Spikes: Use Fibonacci distribution (even coverage)
            if self.body_geometry.is_sphere():
                candidates = fibonacci_sphere(
                    target_count * 2,  # Generate extra
                    self.body_geometry.a
                )
            else:
                candidates = fibonacci_ellipsoid(
                    target_count * 2,
                    self.body_geometry.get_axes()
                )

        else:
            # Generic: Fibonacci distribution
            if self.body_geometry.is_sphere():
                candidates = fibonacci_sphere(target_count * 2, self.body_geometry.a)
            else:
                candidates = fibonacci_ellipsoid(target_count * 2, self.body_geometry.get_axes())

        # Filter by zones
        valid_candidates = []
        for candidate in candidates:
            if self.graph.is_point_in_valid_zone(candidate, part_type):
                valid_candidates.append(candidate)

        return valid_candidates

    def _select_best_candidate(self, candidates, part_type, rule):
        """
        Select best candidate from list based on constraints.

        Args:
            candidates: List of Vec3 candidates
            part_type: Type of part
            rule: AttachmentRule

        Returns:
            Vec3: Best candidate or None
        """
        valid_candidates = []

        for candidate in candidates:
            # Check spacing constraint
            if self._check_spacing_constraint(candidate, part_type, rule.min_spacing):
                valid_candidates.append(candidate)

        if not valid_candidates:
            return None

        # Return random valid candidate
        return self.rng.choice(valid_candidates)

    def solve_tentacles(self, target_count):
        """
        Solve tentacle placement.

        Args:
            target_count: Target number of tentacles

        Returns:
            list: List of AttachmentPoint instances
        """
        part_type = 'tentacle'
        rule = self.graph.get_rule(part_type)

        if not rule:
            print(f"Warning: No rule for {part_type}")
            return []

        # Generate candidates
        candidates = self._generate_candidate_positions(part_type, target_count)

        if not candidates:
            print(f"Warning: No candidates for {part_type}")
            return []

        # Place tentacles
        attachment_points = []
        attempts = 0
        max_attempts = target_count * 10

        while len(attachment_points) < target_count and attempts < max_attempts:
            attempts += 1

            # Select best candidate
            candidate = self._select_best_candidate(candidates, part_type, rule)

            if candidate is None:
                break

            # Project onto surface (ensure exact surface position)
            if self.body_geometry.is_sphere():
                position = project_to_sphere(candidate, (0, 0, 0), self.body_geometry.a)
            else:
                position = project_to_ellipsoid(candidate, (0, 0, 0), self.body_geometry.get_axes())

            # Calculate surface normal
            normal = get_surface_normal(position, (0, 0, 0), self.body_geometry.get_axes())

            # Create attachment point
            point = AttachmentPoint(position, normal, part_type)
            attachment_points.append(point)
            self.placed_points.append(point)

            # Add exclusion zone
            self._add_exclusion_zone(position, rule.exclusion_radius)

            # Remove candidate and nearby candidates
            candidates = [
                c for c in candidates
                if self._geodesic_distance(c, position) > rule.min_spacing
            ]

        print(f"✓ Placed {len(attachment_points)} tentacles (target: {target_count})")
        return attachment_points

    def solve_eyes(self, target_count, eye_pattern='dual'):
        """
        Solve eye placement.

        Args:
            target_count: Target number of eyes
            eye_pattern: Pattern type ('dual', 'spider', 'ring')

        Returns:
            list: List of AttachmentPoint instances
        """
        part_type = 'eye'
        rule = self.graph.get_rule(part_type)

        if not rule:
            return []

        attachment_points = []

        # Special handling for patterns
        if eye_pattern == 'ring' and target_count >= 4:
            # Use ring sampling
            ring_positions = generate_ring_samples(
                self.body_geometry,
                y_position=0.3,  # Upper body
                num_samples=target_count,
                seed=self.seed
            )

            for position in ring_positions:
                normal = get_surface_normal(position, (0, 0, 0), self.body_geometry.get_axes())

                # Apply embedding (eyes sink into surface)
                embedded_position = position - normal * (rule.embedding_depth * self.body_geometry.get_average_radius() * 0.1)

                point = AttachmentPoint(embedded_position, normal, part_type, {'pattern': eye_pattern})
                attachment_points.append(point)
                self.placed_points.append(point)

        else:
            # Use general candidate generation
            candidates = self._generate_candidate_positions(part_type, target_count)

            attempts = 0
            max_attempts = target_count * 10

            while len(attachment_points) < target_count and attempts < max_attempts:
                attempts += 1

                candidate = self._select_best_candidate(candidates, part_type, rule)

                if candidate is None:
                    break

                # Project and get normal
                if self.body_geometry.is_sphere():
                    position = project_to_sphere(candidate, (0, 0, 0), self.body_geometry.a)
                else:
                    position = project_to_ellipsoid(candidate, (0, 0, 0), self.body_geometry.get_axes())

                normal = get_surface_normal(position, (0, 0, 0), self.body_geometry.get_axes())

                # Apply embedding
                embedded_position = position - normal * (rule.embedding_depth * self.body_geometry.get_average_radius() * 0.1)

                point = AttachmentPoint(embedded_position, normal, part_type)
                attachment_points.append(point)
                self.placed_points.append(point)

                # Add exclusion zone
                self._add_exclusion_zone(position, rule.exclusion_radius)

                # Remove nearby candidates
                candidates = [
                    c for c in candidates
                    if self._geodesic_distance(c, position) > rule.min_spacing
                ]

        print(f"✓ Placed {len(attachment_points)} eyes (target: {target_count})")
        return attachment_points

    def solve_spikes(self, target_count):
        """
        Solve spike placement.

        Args:
            target_count: Target number of spikes

        Returns:
            list: List of AttachmentPoint instances
        """
        part_type = 'spike'
        rule = self.graph.get_rule(part_type)

        if not rule:
            return []

        # Generate candidates
        candidates = self._generate_candidate_positions(part_type, target_count)

        attachment_points = []
        attempts = 0
        max_attempts = target_count * 10

        while len(attachment_points) < target_count and attempts < max_attempts:
            attempts += 1

            candidate = self._select_best_candidate(candidates, part_type, rule)

            if candidate is None:
                break

            # Project onto surface
            if self.body_geometry.is_sphere():
                position = project_to_sphere(candidate, (0, 0, 0), self.body_geometry.a)
            else:
                position = project_to_ellipsoid(candidate, (0, 0, 0), self.body_geometry.get_axes())

            normal = get_surface_normal(position, (0, 0, 0), self.body_geometry.get_axes())

            point = AttachmentPoint(position, normal, part_type)
            attachment_points.append(point)
            self.placed_points.append(point)

            # Smaller exclusion zone for spikes
            self._add_exclusion_zone(position, rule.exclusion_radius)

            # Remove nearby candidates
            candidates = [
                c for c in candidates
                if self._geodesic_distance(c, position) > rule.min_spacing
            ]

        print(f"✓ Placed {len(attachment_points)} spikes (target: {target_count})")
        return attachment_points

    def solve_all(self, tentacle_count, eye_count, spike_count, eye_pattern='dual'):
        """
        Solve all constraints and generate complete attachment layout.

        Places parts in priority order:
        1. Tentacles (highest priority - establish structure)
        2. Eyes (medium priority - avoid tentacles)
        3. Spikes (lowest priority - fill remaining space)

        Args:
            tentacle_count: Number of tentacles
            eye_count: Number of eyes
            spike_count: Number of spikes
            eye_pattern: Eye pattern type

        Returns:
            dict: {
                'tentacles': [AttachmentPoint, ...],
                'eyes': [AttachmentPoint, ...],
                'spikes': [AttachmentPoint, ...]
            }
        """
        # Reset solver state
        self.placed_points.clear()
        self.exclusion_zones.clear()

        print("\n=== Solving Creature Anatomy Constraints ===")

        # Phase 1: Tentacles (highest priority)
        tentacles = self.solve_tentacles(tentacle_count)

        # Phase 2: Eyes (medium priority)
        eyes = self.solve_eyes(eye_count, eye_pattern)

        # Phase 3: Spikes (lowest priority)
        spikes = self.solve_spikes(spike_count)

        print(f"=== Constraint Solving Complete ===\n")

        return {
            'tentacles': tentacles,
            'eyes': eyes,
            'spikes': spikes
        }
