import trimesh
import numpy as np

def calculate_centroid(obj_file_path):
    """
    计算 .obj 文件的几何中心（质心）。
    """
    mesh = trimesh.load(obj_file_path)  # 加载模型
    vertices = mesh.vertices  # 获取所有顶点
    centroid = np.mean(vertices, axis=0)  # 计算几何中心
    return centroid

def visualize_with_trimesh(obj_file_path, centroid):
    """
    使用 trimesh 可视化模型和几何中心点。
    """
    # 加载模型
    mesh = trimesh.load(obj_file_path)

    # 创建几何中心点
    centroid_point = trimesh.primitives.Sphere(radius=0.1, center=centroid)

    # 创建场景并添加模型和中心点
    scene = trimesh.Scene([mesh, centroid_point])

    # 显示场景
    scene.show()

# 示例使用
obj_file_path = r'F:\毕设\p2_LOD3_00_School\school.obj'
centroid = calculate_centroid(obj_file_path)
print(f"几何中心点坐标: {centroid}")

# 可视化
visualize_with_trimesh(obj_file_path, centroid)