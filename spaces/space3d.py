import sys
sys.path.append('/home/bibek/projects/animator/')

from vector3d import Vector3d, Point3d
from utils.matrix import Matrix


class Projection:
    """
    Projection params in camera coordinate
    Assumption: projection plane is parallel to xy plane, and centers z axis
    @plane_distance: distance of plane from origin i.e plane's z coordinate
    @plane_width: width of plane in one direction, total width is 2 times
    @plane_height: height of plane in one direction, total height is 2 times
    """
    def __init__(self, plane_distance, plane_width, plane_height):
        self.plane_distance = plane_distance
        self.plane_width = plane_width
        self.plane_height = plane_height
        self.__matrix = None

    @property
    def matrix(self):
        if self.__matrix is not None:
            return self.__matrix
        d = self.plane_distance
        projection = [
            [d, 0, 0, 0],
            [0, d, 0, 0],
            [0, 0, d, 0],
            # we want w coordinate of projected point to be the z coordinate
            [0, 0, 1, 0],
        ]
        self.__matrix = Matrix.new(projection)
        return self.__matrix


class Camera:
    def __init__(self, position, target, up_dir, projection):
        """Initialize a camera with its position, target point, and up_dir
        @position: Point3d
        @target: Point3d [this is the point towards it is facing
        @up_dir: Vector3d
        """
        self.position = position
        self.target = target
        self.up_dir = up_dir
        self.facing_dir = Vector3d.new(self.position, self.target)
        # check if facing_dir and up_dir are perpendicular
        if self.facing_dir.dot(self.up_dir) != 0.0:
            raise Exception("facing dir and up dir are not perpendicular")
        self.__matrix = None
        self.projection = projection

    @property
    def matrix(self):
        """Get the camera matrix to convert object from world coordinate
        to camera coordinate
        """
        if self.__matrix is not None:
            return self.__matrix

        # calculate matrices
        translation = [
            [1, 0, 0, -self.position.x],
            [0, 1, 0, -self.position.y],
            [0, 0, 1, -self.position.z],
            [0, 0, 0, 1]
        ]
        trans_mat = Matrix.new(translation)
        camera_zaxis = self.facing_dir.unit_vector
        camera_yaxis = self.up_dir.unit_vector
        camera_xaxis = camera_yaxis.cross(camera_zaxis).unit_vector
        alignment = [
            [*camera_xaxis.to_list(), 0],
            [*camera_yaxis.to_list(), 0],
            [*camera_zaxis.to_list(), 0],
            [0, 0, 0, 1]
        ]
        alignment_mat = Matrix.new(alignment)
        # now, we have our world coordinate aligned with camera coordinate
        # calculate projection matrix
        proj_mat = self.projection.matrix
        self.__matrix = proj_mat * alignment_mat * trans_mat
        return self.__matrix


class Space3d:
    def __init__(self, camera):
        self.camera = camera


if __name__ == '__main__':
    projection = Projection(5, 5, 5)
    pos = Point3d(0, 0, -5)
    target = Point3d(1, 1, 1)
    up = Vector3d.new(Point3d.origin(), Point3d(1, -1, 0))
    camera = Camera(pos, target, up, projection)
    print(camera.matrix)
