import trimesh
import numpy as np

# 1. 加载OBJ文件
mesh = trimesh.load(r'F:\毕设\p2_LOD3_00_School\school.obj')

# 2. 检查 mesh 的类型
if isinstance(mesh, trimesh.Scene):
    # 如果 mesh 是 Scene 对象，提取其中的几何体
    mesh = mesh.dump().concatenate()  # 将所有几何体合并为一个 Trimesh 对象
elif not isinstance(mesh, trimesh.Trimesh):
    raise ValueError("加载的对象不是 Trimesh 或 Scene 类型")

# 3. 计算法向量
# trimesh 会自动计算每个顶点的法向量，存储在 mesh.vertex_normals 中
vertex_normals = mesh.vertex_normals

# 4. 计算法向量的终点坐标
normal_length = 5.0  # 法向量的长度为 5
normal_end_points = mesh.vertices + vertex_normals * normal_length

# 5. 创建法向量线段
# 将顶点和法向量终点配对，形成线段的起点和终点
lines = np.hstack([mesh.vertices, normal_end_points]).reshape(-1, 2, 3)

# 使用 trimesh.path.Path3D 来绘制法向量线段
entities = [trimesh.path.entities.Line(points=[i, i + 1]) for i in range(0, len(lines) * 2, 2)]
normal_lines = trimesh.path.Path3D(entities=entities, vertices=np.vstack(lines), colors=np.tile([255, 0, 0], (len(lines), 1)))  # 红色线段

# 6. 加载点云数据
# 使用 skiprows=1 跳过表头
point_cloud_data = np.loadtxt(
    r'F:\毕设\p2_LOD3_00_School\local坐标点云.csv',
    delimiter=',',  # 假设CSV文件是逗号分隔的
    skiprows=1,     # 跳过第一行表头
    usecols=(0, 1, 2, 3, 4, 5)  # 只读取 X, Y, Z, Red, Green, Blue 列
)

# 提取点的坐标 (X, Y, Z)
points = point_cloud_data[:, :3]

# 提取点的颜色 (Red, Green, Blue)
colors = point_cloud_data[:, 3:6]

# 将点云数据转换为 trimesh.PointCloud 对象，并传入颜色信息
point_cloud = trimesh.PointCloud(points, colors=colors)

# 7. 创建一个场景
scene = trimesh.Scene()

# 添加原始模型
scene.add_geometry(mesh)

# 添加点云
scene.add_geometry(point_cloud)

# 添加法向量线段
scene.add_geometry(normal_lines)

# 8. 可视化场景
scene.show()