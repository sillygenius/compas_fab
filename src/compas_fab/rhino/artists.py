from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time

import compas
import compas_rhino

from compas_fab.robots.artists import BaseRobotArtist

try:
    import Rhino.Geometry
    import rhinoscriptsyntax as rs
    import scriptcontext as sc

except ImportError:
    compas.raise_if_ironpython()

__all__ = [
    'RobotArtist',
]


class RobotArtist(BaseRobotArtist):
    """Visualizer for robots inside a Rhino environment."""

    # TODO: Add layer (e.g. __init__(self, robot, layer=None))
    def __init__(self, robot): #, layer=None):
        super(RobotArtist, self).__init__(robot)

    def transform(self, native_mesh, transformation):
        T = xform_from_transformation(transformation)
        native_mesh.Transform(T)

    def draw_mesh(self, compas_mesh):
        mesh = Rhino.Geometry.Mesh()
        vertices = compas_mesh.get_vertices_attributes('xyz')
        faces = [compas_mesh.face_vertices(fkey) for fkey in compas_mesh.faces()]

        for v in vertices:
            mesh.Vertices.Add(*v)
        for f in faces:
            mesh.Faces.AddFace(*f)

        mesh.Normals.ComputeNormals()
        mesh.Compact()

        return mesh

    def draw_collision(self):
        collisions = super(RobotArtist, self).draw_collision()
        collisions = list(collisions)

        for mesh in collisions:
            sc.doc.Objects.Add(mesh)

    def draw_visual(self):
        visuals = super(RobotArtist, self).draw_visual()
        visuals = list(visuals)
        for mesh in visuals:
            sc.doc.Objects.Add(mesh)

    def redraw(self, timeout=None):
        """Redraw the Rhino view.

        Parameters
        ----------
        timeout : float, optional
            The amount of time the artist waits before updating the Rhino view.
            The time should be specified in seconds.
            Default is ``None``.

        """
        if timeout:
            time.sleep(timeout)
        rs.EnableRedraw(True)
        rs.Redraw()

    # def clear_layer(self):
    #     """Clear the main layer of the artist."""
    #     if self.layer:
    #         compas_rhino.clear_layer(self.layer)
    #     else:
    #         compas_rhino.clear_current_layer()

    # def clear(self):
    #     """Clear the robot."""
    #     self.clear_robot()

# TODO: Move to compas_rhino.geometry
def xform_from_transformation(transformation):
    """Creates a Rhino Transform instance from a :class:`Transformation`.

    Args:
        transformation (:class:`Transformation`): the transformation.

    Returns:
        (:class:`Rhino.Geometry.Transform`)
    """
    transform = Rhino.Geometry.Transform(1.0)
    for i in range(0, 4):
        for j in range(0, 4):
            transform[i, j] = transformation[i, j]
    return transform
