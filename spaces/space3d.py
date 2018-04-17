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


class Object3d:
    def __init__(self):
        pass


class Space3d:
    def __init__(self, camera, width, height, depth, cell_size=20):
        # NOTE: origin will be in the center of the cube
        #  defined by width, height, depth
        self.camera = camera
        self.width = width
        self.height = height
        self.depth = depth
        self.cell_size = cell_size 
        # TODO: add generic objects later
        self.lines = []  # [(Point3d, Point3d), ...]

    def add_axes(self):
        # add x axis
        self.lines.append((
            Point3d(-self.width, 0, 0),
            Point3d(self.width, 0, 0)
        ))
        # add y axis
        self.lines.append((
            Point3d(0, -self.height, 0),
            Point3d(0, self.height, 0))
        )
        # add z axis
        self.lines.append((
            Point3d(0, 0, -self.depth),
            Point3d(0, 0, self.depth))
        )

    def add_cells(self):
        w, h, d, cs = self.width, self.height, self.depth, self.cell_size
        # lines parallel to x axis in xy plane (+y)
        for x in range(cs, w, cs):
            self.lines.append((
                Point3d(-w, x, 0.),
                Point3d(w, x, 0.)
            ))
        # lines parallel to x axis in xz plane (+z)
        for z in range(cs, d, cs):
            self.lines.append((
                Point3d(-w, 0., z),
                Point3d(w, 0., z)
            ))
        # lines parallel to y axis in xy plane (+x)
        for x in range(cs, w, cs):
            self.lines.append((
                Point3d(x, -h, 0.),
                Point3d(x, h, 0.)
            ))
        # lines parallel to y axis in yz plane (+z)
        for z in range(cs, d, cs):
            self.lines.append((
                Point3d(0, -h, z),
                Point3d(0, h, z)
            ))
        # lines parallel to z axis in xz plane (+x)
        for x in range(cs, w, cs):
            self.lines.append((
                Point3d(x, 0, -d),
                Point3d(x, 0, d)
            ))
        # lines parallel to z axis in yz plane (+y)
        for y in range(cs, d, cs):
            self.lines.append((
                Point3d(0, y, -d),
                Point3d(0, y, d)
            ))
        # negative direction
        # lines parallel to x axis in xy plane (-y)
        for x in range(cs, w, cs):
            self.lines.append((
                Point3d(-w, -x, 0.),
                Point3d(w, -x, 0.)
            ))
        # lines parallel to x axis in xz plane (-z)
        for z in range(cs, d, cs):
            self.lines.append((
                Point3d(-w, 0., -z),
                Point3d(w, 0., -z)
            ))
        # lines parallel to y axis in xy plane (-x)
        for x in range(cs, w, cs):
            self.lines.append((
                Point3d(-x, -h, 0.),
                Point3d(-x, h, 0.)
            ))
        # lines parallel to y axis in yz plane (+-)
        for z in range(cs, d, cs):
            self.lines.append((
                Point3d(0, -h, -z),
                Point3d(0, h, -z)
            ))
        # lines parallel to z axis in xz plane (-x)
        for x in range(cs, w, cs):
            self.lines.append((
                Point3d(-x, 0, -d),
                Point3d(-x, 0, d)
            ))
        # lines parallel to z axis in yz plane (-y)
        for y in range(cs, d, cs):
            self.lines.append((
                Point3d(0, -y, -d),
                Point3d(0, -y, d)
            ))

    def transform_point(self, point3d):
        pointarr = [*point3d.to_list(), 1.]
        pointmatrix = Matrix.new([[x] for x in pointarr])
        result = self.camera.matrix * pointmatrix
        z = result.array[-1][0]
        x = result.array[0][0]
        y = result.array[1][0]
        try:
            return [x/z, y/z]
        except:
            return None


if __name__ == '__main__':
    projection = Projection(5, 5, 5)
    # camera properties
    pos = Point3d(0, 0, -5)
    target = Point3d(2, 3, 7)
    up = Vector3d.new(Point3d.origin(), Point3d(3, -2, 0))
    camera = Camera(pos, target, up, projection)
    size = 20
    space = Space3d(camera, size, size, size, 2)
    space.add_axes()
    space.add_cells()
    print(len(space.lines))

    from spaces.space2d import Space2d
    from spaces.vector import Point

    g = Space2d(400, 400, 200, 200, 25)
    # g.render()
    for x in space.lines:
        p1tx = space.transform_point(x[0])
        p2tx = space.transform_point(x[1])
        if p1tx is None or p2tx is None:
            continue
        p1 = Point(*p1tx)
        p2 = Point(*p2tx)
        g.line(p1, p2)
    g.save('test.png')
