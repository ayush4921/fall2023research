## Mathematics Behind the Transformation

### 1. Projection Matrix

The projection matrix is used to convert 3D coordinates into a 2D plane, considering perspective. This transformation is governed by the camera's field of view (FOV), aspect ratio, and the distances to the near and far clipping planes.

- **Field of View (FOV)**: Determines how wide the camera can see. A larger FOV allows the camera to see more of the scene.
- **Aspect Ratio**: Ratio of the screen's width to its height.
- **Near and Far Clipping Planes**: Define the depth range of the scene that the camera can see.

The projection matrix is a 4x4 matrix defined as follows:

```plaintext
| f/aspect_ratio  0                0                              0 |
| 0               f                0                              0 |
| 0               0                (near+far)*range_inv          -1 |
| 0               0                near*far*range_inv*2           0 |
```

Where `f = 1.0 / tan(FOV / 2)` and `range_inv = 1.0 / (near - far)`.

### 2. View Matrix

The view matrix represents the camera's position and orientation in the world. It's derived from the camera's pitch (up-down rotation) and yaw (left-right rotation), as well as its position in the world.

- **Pitch**: Rotation around the camera's x-axis.
- **Yaw**: Rotation around the camera's y-axis.

The view matrix is constructed using the camera's orientation to create a coordinate system (x-axis, y-axis, z-axis) and then applying a translation based on the camera's position.

### 3. Conversion Process

To convert a 3D point to a 2D screen coordinate, the following steps are performed:

1. **Apply View Matrix**: Transform the 3D point from world coordinates to camera view space.
2. **Apply Projection Matrix**: Project the point from view space to clip space.
3. **Normalization**: Convert from clip space to normalized device coordinates (NDC). This involves dividing by the w-component of the resulting vector.
4. **Screen Mapping**: Map the NDC to screen coordinates. The NDC range (-1 to 1) is mapped to the screen dimensions.

## Python Implementation

The Python tool uses `numpy` for matrix and vector operations. The core functions are:

- `create_projection_matrix()`: Constructs the projection matrix.
- `create_view_matrix()`: Constructs the view matrix.
- `convert_to_screen_coordinates()`: Applies the above matrices to transform a 3D point to 2D screen coordinates.
