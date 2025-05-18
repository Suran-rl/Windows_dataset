import open3d as o3d
import pandas as pd
import numpy as np
from scipy.spatial.transform import Rotation as R

# 参数设置
translation_distance = 5  # 法向量长度，可以自由调整
pyramid_base_size = 1 # 金字塔底部大小
pyramid_height = 2.5 # 金字塔高度

# 1. 读取稀疏点云数据
point_cloud_file = r'F:\毕设\p2_LOD3_00_School\local坐标点云.csv'
point_cloud_data = pd.read_csv(point_cloud_file)
# 提取点云的坐标和颜色
points = point_cloud_data[['X', 'Y', 'Z']].to_numpy()
colors = point_cloud_data[['Red', 'Green', 'Blue']].to_numpy()
# 创建点云对象
point_cloud = o3d.geometry.PointCloud()
point_cloud.points = o3d.utility.Vector3dVector(points)
point_cloud.colors = o3d.utility.Vector3dVector(colors)

# 2. 计算法向量终点
# 读取摄影中心数据
photogrammetry_center_path = r'F:\毕设\p2_LOD3_00_School\00_local坐标摄影中心.csv'
photogrammetry_center_df = pd.read_csv(photogrammetry_center_path)
# 读取法向量数据
normal_vector_path = r'F:\毕设\p2_LOD3_00_School\指向中心的法向量(改).csv'
normal_vector_df = pd.read_csv(normal_vector_path)
# 确保数据对齐
assert len(photogrammetry_center_df) == len(normal_vector_df), "摄影中心和法向量数据长度不一致"
# 提取x, y, z坐标和法向量
photogrammetry_center = photogrammetry_center_df[['x', 'y', 'z']].values
normal_vector = normal_vector_df[['x', 'y', 'z']].values
# 沿着法向量方向平移指定距离
translated_center = photogrammetry_center + normal_vector * translation_distance


# 3. 创建金字塔表示相机朝向
def create_pyramid(base_center, tip_point, base_size=0.5, height=1.0):
    # 计算方向向量
    direction = tip_point - base_center
    direction_normalized = direction / np.linalg.norm(direction)

    # 创建基础金字塔(朝z轴正方向)
    vertices = [
        [base_size, base_size, 0],  # 0: 底面右下
        [-base_size, base_size, 0],  # 1: 底面左下
        [-base_size, -base_size, 0],  # 2: 底面左上
        [base_size, -base_size, 0],  # 3: 底面右上
        [0, 0, height]  # 4: 顶点
    ]
    triangles = [
        [0, 1, 4],  # 右面
        [1, 2, 4],  # 后面
        [2, 3, 4],  # 左面
        [3, 0, 4],  # 前面
        [0, 3, 2],  # 底面
        [0, 2, 1]  # 底面
    ]

    # 计算旋转使金字塔朝向方向向量
    z_axis = np.array([0, 0, 1])
    rotation_axis = np.cross(z_axis, direction_normalized)
    rotation_axis_norm = np.linalg.norm(rotation_axis)
    if rotation_axis_norm > 1e-6:
        rotation_axis = rotation_axis / rotation_axis_norm
        rotation_angle = np.arccos(np.dot(z_axis, direction_normalized))
        rotation_vector = rotation_axis * rotation_angle
        rotation = R.from_rotvec(rotation_vector)
        vertices = rotation.apply(vertices)

    # 平移金字塔到正确位置
    vertices = np.array(vertices) * (height / np.linalg.norm(direction))  # 缩放金字塔
    vertices += base_center  # 平移金字塔

    # 创建网格
    pyramid = o3d.geometry.TriangleMesh()
    pyramid.vertices = o3d.utility.Vector3dVector(vertices)
    pyramid.triangles = o3d.utility.Vector3iVector(triangles)

    # 设置颜色 (红色半透明)
    pyramid.paint_uniform_color([0, 0, 1])
    pyramid.compute_vertex_normals()

    return pyramid


# 创建所有金字塔
pyramids = []
for i in range(len(photogrammetry_center)):
    pyramid = create_pyramid(
        base_center=photogrammetry_center[i],
        tip_point=translated_center[i],
        base_size=pyramid_base_size,
        height=pyramid_height
    )
    pyramids.append(pyramid)


# 4. 可视化函数
def visualize_geometries():
    # 创建可视化窗口
    vis = o3d.visualization.Visualizer()
    vis.create_window(width=1200, height=800, window_name=f"点云和相机朝向金字塔 (长度={translation_distance})")

    # 添加几何体
    vis.add_geometry(point_cloud)
    for pyramid in pyramids:
        vis.add_geometry(pyramid)

    # 设置渲染选项
    render_opt = vis.get_render_option()
    render_opt.point_size = 5.0  # 点云大小
    render_opt.mesh_show_back_face = True  # 显示背面

    # 获取所有点的边界框
    all_points = np.vstack([points, photogrammetry_center, translated_center])
    bbox = o3d.geometry.AxisAlignedBoundingBox.create_from_points(
        o3d.utility.Vector3dVector(all_points))

    # 设置视角
    ctr = vis.get_view_control()
    ctr.set_lookat(bbox.get_center())  # 看向中心点
    ctr.set_up([0, 0, 1])  # Z轴向上
    ctr.set_front([0, -1, 0])  # 从前方看
    ctr.set_zoom(0.6)  # 缩放级别

    # 打印调试信息
    print("===== 可视化信息 =====")
    print(f"点云点数: {len(points)}")
    print(f"相机数量: {len(photogrammetry_center)}")
    print(f"法向量长度: {translation_distance}")
    print("金字塔参数: 底部大小=", pyramid_base_size, "高度=", pyramid_height)
    print("显示范围:", bbox.get_min_bound(), "to", bbox.get_max_bound())

    # 运行可视化
    vis.run()
    vis.destroy_window()


# 执行可视化
visualize_geometries()