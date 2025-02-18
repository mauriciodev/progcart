import numpy as np
from typing import Tuple, List, Union

# Type aliases for clarity
Point = Tuple[float, float]
Shape = List[Point]

def calculate_length(coordinates: Shape) -> float:
    """Calculate the length of a shape (0 for point, sum of segments for lines/polygons)"""
    if len(coordinates) <= 1:
        return 0
    
    points = np.array(coordinates)
    return sum(
        np.linalg.norm(points[i] - points[i-1]) 
        for i in range(1, len(points))
    )

def format_point(coordinates: Shape) -> str:
    """Format a point as string"""
    x, y = coordinates[0]
    return f"PONTO({x}, {y})"

def format_line(coordinates: Shape) -> str:
    """Format a line as string"""
    points_str = ", ".join(f"({x}, {y})" for x, y in coordinates)
    return f"LINHA({points_str})"

def format_polygon(coordinates: Shape) -> str:
    """Format a polygon as string"""
    points_str = ", ".join(f"({x}, {y})" for x, y in coordinates)
    return f"POLIGONO({points_str})"

def create_polygon(coordinates: Shape) -> Shape:
    """Create a polygon by closing the shape (adding first point at the end)"""
    return coordinates + [coordinates[0]]

if __name__ == "__main__":
    # Data definitions (using tuples for immutability)
    point_coords = [(0, 0)]
    line_coords = [(0, 0), (1, 0), (1, 1)]
    polygon_coords = create_polygon([(0, 0), (1, 0), (1, 1), (0, 1)])

    # Calculate and print lengths
    print(calculate_length(point_coords))
    print(calculate_length(line_coords))
    print(calculate_length(polygon_coords))

    # Format and print shapes
    print(format_point(point_coords))
    print(format_line(line_coords))
    print(format_polygon(polygon_coords))