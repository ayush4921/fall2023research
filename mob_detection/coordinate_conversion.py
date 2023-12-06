import numpy as np
import minedojo
import numpy as np

# Define the functions for projection and view matrix creation, and screen coordinate conversion
# (functions `create_projection_matrix`, `create_view_matrix`, and `convert_to_screen_coordinates` should be defined here as per your provided script)

# Initialize MineDojo environment
env = minedojo.make(task_id="creative:255", image_size=(1920, 1080))  # Example scenario
obs = env.reset()


def create_projection_matrix(fov, aspect_ratio, near, far):
    """Create a perspective projection matrix."""
    # Calculate the scaling factor using the field of view
    f = 1.0 / np.tan(np.radians(fov) / 2)
    # Calculate the range between the near and far clipping planes
    range_inv = 1.0 / (near - far)

    # Define the projection matrix based on the above parameters
    projection_matrix = np.array(
        [
            [f / aspect_ratio, 0, 0, 0],  # Scale the x coordinate
            [0, f, 0, 0],  # Scale the y coordinate
            [0, 0, (near + far) * range_inv, -1],  # Position the z coordinate
            [0, 0, near * far * range_inv * 2, 0],  # Perspective division factor
        ]
    )
    return projection_matrix


def create_view_matrix(position, pitch, yaw):
    """Create a view matrix based on camera position and orientation."""
    # Convert pitch and yaw angles from degrees to radians
    pitch = np.radians(pitch)
    yaw = np.radians(yaw)

    # Calculate the direction vectors based on pitch and yaw
    cos_pitch = np.cos(pitch)
    sin_pitch = np.sin(pitch)
    cos_yaw = np.cos(yaw)
    sin_yaw = np.sin(yaw)

    # Define the axis of rotation
    xaxis = np.array([cos_yaw, 0, -sin_yaw])  # X-axis rotation
    yaxis = np.array(
        [sin_yaw * sin_pitch, cos_pitch, cos_yaw * sin_pitch]
    )  # Y-axis rotation
    zaxis = np.array(
        [sin_yaw * cos_pitch, -sin_pitch, cos_pitch * cos_yaw]
    )  # Z-axis rotation

    # Construct the view matrix from the axis vectors and camera position
    matrix = np.array(
        [
            [xaxis[0], yaxis[0], zaxis[0], 0],  # X, Y, Z axis directions
            [xaxis[1], yaxis[1], zaxis[1], 0],  # X, Y, Z axis directions
            [xaxis[2], yaxis[2], zaxis[2], 0],  # X, Y, Z axis directions
            [
                -np.dot(xaxis, position),  # Camera position offset for X
                -np.dot(yaxis, position),  # Camera position offset for Y
                -np.dot(zaxis, position),  # Camera position offset for Z
                1,
            ],
        ]
    )
    return matrix


def convert_to_screen_coordinates(
    pos_3d, fov, aspect_ratio, near, far, cam_position, cam_pitch, cam_yaw
):
    """Convert 3D game coordinates to 2D screen coordinates."""
    # Generate a projection matrix using the specified parameters
    projection_matrix = create_projection_matrix(fov, aspect_ratio, near, far)
    # Generate a view matrix using the camera's position and orientation
    view_matrix = create_view_matrix(cam_position, cam_pitch, cam_yaw)

    # Transform the 3D coordinates to 4D for matrix multiplication
    pos_4d = np.array([pos_3d[0], pos_3d[1], pos_3d[2], 1.0])
    # Apply the view matrix, then the projection matrix
    transformed_pos = np.dot(projection_matrix, np.dot(view_matrix, pos_4d))

    # Normalize the coordinates if w is not 0 (perspective division)
    if transformed_pos[3] != 0:
        transformed_pos /= transformed_pos[3]

    # Map the normalized coordinates to screen space (0 to 1 range)
    # After perspective division, the coordinates are in NDC, where each component (x, y, z) ranges from -1 to 1. The point (-1, -1) corresponds to the bottom-left corner of the screen, and (1, 1) corresponds to the top-right corner.

    # Mapping to Screen Space: To map these coordinates to a typical screen space (where the coordinates range from 0 to 1), we need to adjust the range. Multiplying by 0.5 scales the range from [-1, 1] to [-0.5, 0.5]. Then, adding 0.5 shifts this range to [0, 1]. After this transformation, the point (0, 0) corresponds to the bottom-left corner of the screen, and (1, 1) to the top-right corner.

    screen_pos = np.array(
        [transformed_pos[0] * 0.5 + 0.5, transformed_pos[1] * 0.5 + 0.5]
    )

    return screen_pos


# Extract camera parameters from observations
fov = 70  # Assuming a fixed field of view
aspect_ratio = 1920 / 1080  # Assuming a fixed aspect ratio

# Use the initial camera position and orientation from the environment
cam_position = np.array(
    [
        obs["location_stats"]["pos"][0],
        obs["location_stats"]["pos"][1],
        obs["location_stats"]["pos"][2],
    ]
)
cam_pitch = obs["location_stats"]["pitch"][0]
cam_yaw = obs["location_stats"]["yaw"][0]

# Set near and far clipping planes
near = 0.1
far = 1000.0

# Sample 3D position to convert (for example, the agent's current position)
pos_3d = cam_position

# Convert to screen coordinates
screen_coords = convert_to_screen_coordinates(
    pos_3d, fov, aspect_ratio, near, far, cam_position, cam_pitch, cam_yaw
)

print("Screen Coordinates:", screen_coords)
