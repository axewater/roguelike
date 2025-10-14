"""
Anatomy Graph System - Define creature structure as graph

Represents creature anatomy as a graph:
- Nodes = body parts (body, tentacles, eyes, spikes)
- Edges = attachment relationships
- Zones = regions where parts can attach
- Rules = constraints for valid creature anatomy

This provides the structural foundation for constraint-based creature generation.
"""

from ursina import Vec3
from surface_math import BodyGeometry, get_hemisphere_region


class AttachmentPoint:
    """
    Represents a point where a body part can attach to the body.
    """

    def __init__(self, position, normal, part_type, metadata=None):
        """
        Initialize attachment point.

        Args:
            position: Vec3 position on body surface
            normal: Vec3 surface normal (outward direction)
            part_type: Type of part ('tentacle', 'eye', 'spike')
            metadata: Optional dict with additional data
        """
        self.position = position if isinstance(position, Vec3) else Vec3(*position)
        self.normal = normal if isinstance(normal, Vec3) else Vec3(*normal)
        self.part_type = part_type
        self.metadata = metadata or {}

        # State
        self.occupied = False
        self.part_id = None  # ID of part attached here

    def mark_occupied(self, part_id):
        """Mark this attachment point as occupied"""
        self.occupied = True
        self.part_id = part_id

    def clear(self):
        """Clear occupation"""
        self.occupied = False
        self.part_id = None

    def get_position(self):
        """Get position as Vec3"""
        return self.position

    def get_normal(self):
        """Get normal as Vec3"""
        return self.normal

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'position': (self.position.x, self.position.y, self.position.z),
            'normal': (self.normal.x, self.normal.y, self.normal.z),
            'part_type': self.part_type,
            'occupied': self.occupied,
            'part_id': self.part_id,
            'metadata': self.metadata
        }


class AnatomicalZone:
    """
    Defines a region on the body where certain parts can attach.

    Examples:
    - Tentacle zone: Lower hemisphere
    - Eye zone: Upper/front hemisphere
    - Spike zone: Anywhere except where tentacles attach
    """

    def __init__(self, name, allowed_parts, region_filter, priority=0):
        """
        Initialize anatomical zone.

        Args:
            name: Zone name (e.g., 'tentacle_zone', 'eye_zone')
            allowed_parts: List of allowed part types
            region_filter: Function(point) -> bool that returns True if point is in zone
            priority: Zone priority (higher = placed first)
        """
        self.name = name
        self.allowed_parts = allowed_parts
        self.region_filter = region_filter
        self.priority = priority

    def contains_point(self, point):
        """Check if point is in this zone"""
        return self.region_filter(point)

    def allows_part_type(self, part_type):
        """Check if this zone allows a part type"""
        return part_type in self.allowed_parts


class AttachmentRule:
    """
    Defines constraints for attaching a type of part.

    Examples:
    - Tentacles: min_spacing=0.5, max_count=12, zones=['tentacle_zone']
    - Eyes: min_spacing=0.3, max_count=8, zones=['eye_zone'], embedding_depth=0.5
    - Spikes: min_spacing=0.2, max_count=30, zones=['spike_zone']
    """

    def __init__(self, part_type, min_spacing, max_count, allowed_zones,
                 embedding_depth=0.0, exclusion_radius=0.0):
        """
        Initialize attachment rule.

        Args:
            part_type: Type of part
            min_spacing: Minimum geodesic distance between parts of this type
            max_count: Maximum number of parts
            allowed_zones: List of zone names where part can attach
            embedding_depth: How far into surface part is embedded (0 to 1)
            exclusion_radius: Radius around part where other parts can't attach
        """
        self.part_type = part_type
        self.min_spacing = min_spacing
        self.max_count = max_count
        self.allowed_zones = allowed_zones
        self.embedding_depth = embedding_depth
        self.exclusion_radius = exclusion_radius

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'part_type': self.part_type,
            'min_spacing': self.min_spacing,
            'max_count': self.max_count,
            'allowed_zones': self.allowed_zones,
            'embedding_depth': self.embedding_depth,
            'exclusion_radius': self.exclusion_radius
        }


class CreatureAnatomyGraph:
    """
    Graph representation of creature anatomy.

    Structure:
    - Root node: Body
    - Child nodes: Tentacles, eyes, spikes
    - Edges: Attachment relationships
    """

    def __init__(self, body_geometry):
        """
        Initialize anatomy graph.

        Args:
            body_geometry: BodyGeometry instance
        """
        self.body_geometry = body_geometry
        self.zones = {}
        self.rules = {}
        self.attachment_points = []
        self.parts = {}  # part_id -> part_data

        # Initialize default zones and rules
        self._initialize_default_anatomy()

    def _initialize_default_anatomy(self):
        """
        Set up default anatomical zones and rules for tentacle horrors.
        """
        # Define zones
        self.add_zone(
            'tentacle_zone',
            allowed_parts=['tentacle'],
            region_filter=lambda p: get_hemisphere_region(p)['vertical'] == 'lower',
            priority=1  # High priority - place tentacles first
        )

        self.add_zone(
            'eye_zone',
            allowed_parts=['eye'],
            region_filter=lambda p: (
                get_hemisphere_region(p)['vertical'] in ['upper', 'equator'] and
                get_hemisphere_region(p)['horizontal'] == 'front'
            ),
            priority=2  # Medium priority
        )

        self.add_zone(
            'spike_zone',
            allowed_parts=['spike'],
            region_filter=lambda p: True,  # Spikes can go anywhere
            priority=0  # Low priority - place last
        )

        # Define rules
        avg_radius = self.body_geometry.get_average_radius()

        self.add_rule(
            'tentacle',
            min_spacing=avg_radius * 0.4,  # Tentacles need good spacing
            max_count=12,
            allowed_zones=['tentacle_zone'],
            embedding_depth=0.0,  # Tentacles attach at surface
            exclusion_radius=avg_radius * 0.3  # Keep other parts away
        )

        self.add_rule(
            'eye',
            min_spacing=avg_radius * 0.25,  # Eyes can be closer together
            max_count=8,
            allowed_zones=['eye_zone'],
            embedding_depth=0.5,  # Eyes are half-embedded in surface
            exclusion_radius=avg_radius * 0.15
        )

        self.add_rule(
            'spike',
            min_spacing=avg_radius * 0.15,  # Spikes can be dense
            max_count=30,
            allowed_zones=['spike_zone'],
            embedding_depth=0.0,
            exclusion_radius=avg_radius * 0.1
        )

    def add_zone(self, name, allowed_parts, region_filter, priority=0):
        """
        Add an anatomical zone.

        Args:
            name: Zone name
            allowed_parts: List of allowed part types
            region_filter: Function(point) -> bool
            priority: Placement priority
        """
        self.zones[name] = AnatomicalZone(name, allowed_parts, region_filter, priority)

    def add_rule(self, part_type, min_spacing, max_count, allowed_zones,
                 embedding_depth=0.0, exclusion_radius=0.0):
        """
        Add an attachment rule.

        Args:
            part_type: Type of part
            min_spacing: Minimum spacing
            max_count: Maximum count
            allowed_zones: List of zone names
            embedding_depth: Embedding depth (0 to 1)
            exclusion_radius: Exclusion radius
        """
        self.rules[part_type] = AttachmentRule(
            part_type,
            min_spacing,
            max_count,
            allowed_zones,
            embedding_depth,
            exclusion_radius
        )

    def get_rule(self, part_type):
        """
        Get attachment rule for part type.

        Args:
            part_type: Type of part

        Returns:
            AttachmentRule or None
        """
        return self.rules.get(part_type)

    def get_zones_for_part(self, part_type):
        """
        Get zones that allow a part type.

        Args:
            part_type: Type of part

        Returns:
            list: List of AnatomicalZone instances
        """
        valid_zones = []
        rule = self.get_rule(part_type)

        if rule:
            for zone_name in rule.allowed_zones:
                if zone_name in self.zones:
                    valid_zones.append(self.zones[zone_name])

        return valid_zones

    def is_point_in_valid_zone(self, point, part_type):
        """
        Check if point is in a valid zone for part type.

        Args:
            point: Vec3 position
            part_type: Type of part

        Returns:
            bool: True if valid
        """
        zones = self.get_zones_for_part(part_type)

        for zone in zones:
            if zone.contains_point(point):
                return True

        return False

    def add_attachment_point(self, position, normal, part_type, metadata=None):
        """
        Add an attachment point to the graph.

        Args:
            position: Vec3 position
            normal: Vec3 surface normal
            part_type: Type of part
            metadata: Optional metadata dict

        Returns:
            AttachmentPoint: Created attachment point
        """
        point = AttachmentPoint(position, normal, part_type, metadata)
        self.attachment_points.append(point)
        return point

    def get_attachment_points_by_type(self, part_type):
        """
        Get all attachment points for a part type.

        Args:
            part_type: Type of part

        Returns:
            list: List of AttachmentPoint instances
        """
        return [p for p in self.attachment_points if p.part_type == part_type]

    def get_available_attachment_points(self, part_type):
        """
        Get unoccupied attachment points for a part type.

        Args:
            part_type: Type of part

        Returns:
            list: List of available AttachmentPoint instances
        """
        return [
            p for p in self.attachment_points
            if p.part_type == part_type and not p.occupied
        ]

    def add_part(self, part_id, part_type, attachment_point, part_data=None):
        """
        Add a part to the graph.

        Args:
            part_id: Unique part identifier
            part_type: Type of part
            attachment_point: AttachmentPoint where part attaches
            part_data: Optional additional data
        """
        self.parts[part_id] = {
            'type': part_type,
            'attachment_point': attachment_point,
            'data': part_data or {}
        }

        attachment_point.mark_occupied(part_id)

    def get_part_count(self, part_type):
        """
        Get number of parts of a type.

        Args:
            part_type: Type of part

        Returns:
            int: Count
        """
        return sum(1 for p in self.parts.values() if p['type'] == part_type)

    def clear_attachment_points(self):
        """Clear all attachment points"""
        self.attachment_points.clear()
        self.parts.clear()

    def get_stats(self):
        """
        Get graph statistics.

        Returns:
            dict: Statistics
        """
        stats = {
            'zones': len(self.zones),
            'rules': len(self.rules),
            'attachment_points': len(self.attachment_points),
            'parts': len(self.parts)
        }

        # Count by type
        for part_type in self.rules.keys():
            stats[f'{part_type}_count'] = self.get_part_count(part_type)
            stats[f'{part_type}_points'] = len(self.get_attachment_points_by_type(part_type))

        return stats

    def to_dict(self):
        """
        Export graph to dictionary.

        Returns:
            dict: Serializable graph data
        """
        return {
            'body_geometry': {
                'size': self.body_geometry.size,
                'shape_type': self.body_geometry.shape_type,
                'axes': self.body_geometry.get_axes()
            },
            'zones': {name: {'allowed_parts': zone.allowed_parts, 'priority': zone.priority}
                      for name, zone in self.zones.items()},
            'rules': {name: rule.to_dict() for name, rule in self.rules.items()},
            'attachment_points': [p.to_dict() for p in self.attachment_points],
            'parts': self.parts
        }
