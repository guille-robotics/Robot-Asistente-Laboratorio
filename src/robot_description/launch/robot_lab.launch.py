import os, xacro
from pathlib import Path
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

robot_model = 'robot_lab' # Cambiado al nombre de tu xacro
robot_ns = 'r1' # Robot namespace
pose = ['0.0', '0.0', '0.0', '0.0'] # Initial robot pose: x,y,z,th
robot_base_color = '0.0 0.0 1.0 0.95' 
world_file = 'empty.sdf' 

def generate_launch_description():

    # Cambiado al paquete donde guardarás tu robot
    this_pkg_path = os.path.join(get_package_share_directory('robot_description'))

    simu_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='True',
        description='Use simulation (Gazebo) clock if true')
    
    ign_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=[
            os.path.join(this_pkg_path, 'worlds'), ':' + str(Path(this_pkg_path).parent.resolve())
        ]
    )

    open_ign = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('ros_gz_sim'), 'launch'), '/gz_sim.launch.py']),
            launch_arguments=[
                ('gz_args', [this_pkg_path+"/worlds/"+world_file, ' -v 4', ' -r'])
        ]
    )

    xacro_file = os.path.join(this_pkg_path, 'urdf', robot_model+'.xacro')

    doc = xacro.process_file(xacro_file, mappings={'base_color' : robot_base_color, 'ns' : robot_ns})
    robot_desc = doc.toprettyxml(indent='  ')
    
    gz_spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=['-string', robot_desc,
                   '-x', pose[0], '-y', pose[1], '-z', pose[2],
                   '-R', '0.0', '-P', '0.0', '-Y', pose[3],
                   '-name', robot_ns,
                   '-allow_renaming', 'false'],
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        namespace=robot_ns,
        output="screen",
        parameters=[{'robot_description': robot_desc, 'use_sim_time': True}]
    )

    # Bridge para ROS 2 <-> Gazebo Ignition
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[             
            '/model/'+robot_ns+'/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
            '/model/'+robot_ns+'/odometry@nav_msgs/msg/Odometry@gz.msgs.Odometry',
            '/world/empty/model/'+robot_ns+'/joint_state@sensor_msgs/msg/JointState[gz.msgs.Model',
            
            # Sensores agregados
            '/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan',
            '/camera/image_raw@sensor_msgs/msg/Image@gz.msgs.Image',
            '/camera/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo',
        ],
        parameters=[{'qos_overrides./model/'+robot_ns+'.subscriber.reliability': 'reliable'}],
        output='screen',
        remappings=[            
            ('/model/'+robot_ns+'/cmd_vel', '/'+robot_ns+'/cmd_vel'),
            ('/model/'+robot_ns+'/odometry', '/'+robot_ns+'/odom'),
            ('/world/empty/model/'+robot_ns+'/joint_state', '/'+robot_ns+'/joint_states'),
            ('/scan', '/'+robot_ns+'/scan'),
            ('/camera/image_raw', '/'+robot_ns+'/camera/image_raw'),
        ]
    )

    return LaunchDescription(
        [
            simu_time,
            ign_resource_path,
            open_ign,
            gz_spawn_entity,
            robot_state_publisher,
            bridge
        ]
    )