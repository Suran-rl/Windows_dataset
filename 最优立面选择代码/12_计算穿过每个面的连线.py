import pandas as pd
import numpy as np

# 读取房屋模型数据
vertices_file_path = r'F:\\毕设\\p2_LOD3_00_School\\vertices_and_center.csv'
vertices_data = pd.read_csv(vertices_file_path)
vertices = vertices_data[vertices_data['Type'] == 'Vertex'][['X', 'Y', 'Z']].values
vertex_ids = vertices_data[vertices_data['Type'] == 'Vertex']['ID'].values.astype(int)
center_point = vertices_data[vertices_data['Type'] == 'Center'][['X', 'Y', 'Z']].values.flatten()

# 读取摄影中心点数据
photo_centers_file_path = r'F:\\毕设\\p2_LOD3_00_School\\00_local坐标摄影中心.csv'
photo_centers_data = pd.read_csv(photo_centers_file_path)
photo_centers = photo_centers_data[['x', 'y', 'z']].values
photo_ids = photo_centers_data['ID'].values.astype(str)

# 定义四个面
faces_ids = [
    [8, 4, 3, 7],     # 侧面
    [6, 2, 1, 5],     # 侧面
    [6, 12, 8, 7, 5], # 前面
    [4, 10, 2, 1, 3]  # 后面
]

# 创建 ID 到数组索引的映射
id_to_index = {id_: idx for idx, id_ in enumerate(vertex_ids)}

# 将面的顶点 ID 转换为数组索引
faces = [[id_to_index[id_] for id_ in face] for face in faces_ids]

# 判断射线是否与平面相交
def does_ray_intersect_plane(plane_points, ray_start, ray_end):
    # 计算平面法向量
    v1 = plane_points[1] - plane_points[0]
    v2 = plane_points[2] - plane_points[0]
    normal = np.cross(v1, v2)
    if np.linalg.norm(normal) < 1e-6:  # 平面点共线，无法计算法向量
        return False
    # 计算射线方向向量
    ray_dir = ray_end - ray_start
    # 计算射线与平面的交点
    denom = np.dot(normal, ray_dir)
    if abs(denom) < 1e-6:  # 射线与平面平行
        return False
    t = np.dot(normal, plane_points[0] - ray_start) / denom
    if t < 0:  # 交点在射线的反方向
        return False
    # 计算交点
    intersection = ray_start + t * ray_dir
    # 判断交点是否在平面内（使用重心坐标法）
    def point_in_polygon(polygon, point):
        # 将多边形和点投影到二维平面（选择法向量最大的维度忽略）
        abs_normal = np.abs(normal)
        ignore_dim = np.argmax(abs_normal)
        polygon_2d = np.delete(polygon, ignore_dim, axis=1)
        point_2d = np.delete(point, ignore_dim)
        # 计算重心坐标
        def cross(a, b):
            return a[0] * b[1] - a[1] * b[0]
        n = len(polygon_2d)
        inside = False
        for i in range(n):
            a = polygon_2d[i]
            b = polygon_2d[(i + 1) % n]
            if ((a[1] > point_2d[1]) != (b[1] > point_2d[1])) and (
                point_2d[0] < (b[0] - a[0]) * (point_2d[1] - a[1]) / (b[1] - a[1]) + a[0]
            ):
                inside = not inside
        return inside
    return point_in_polygon(plane_points, intersection)

# 遍历每个摄影中心点
results = []
for photo_center, photo_id in zip(photo_centers, photo_ids):
    for face, face_ids in zip(faces, faces_ids):
        plane_points = vertices[face]
        if does_ray_intersect_plane(plane_points, center_point, photo_center):
            results.append(f"{face_ids} + {photo_id}")
            break  # 确保一条射线只与一个面相交

# 导出结果
if results:
    for result in results:
        print(result)
else:
    print("没有找到射线与平面的交点。请检查数据或平面定义。")