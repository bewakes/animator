from vector3d import Vector3d, Point3d


class Camera:
    def __init__(self, position, facing, up):
        self.position = position
        self.facing = facing
        self.up = up


class Space3d:
    def __init__(self, camera):
        self.camera = camera
