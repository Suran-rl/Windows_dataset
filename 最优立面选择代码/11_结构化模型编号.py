import pandas as pd
import numpy as np

# 读取 CSV 文件
csv_file_path = r'F:\\\\毕设\\\\p2_LOD3_00_School\\\\vertices_and_center.csv'
data = pd.read_csv(csv_file_path)

# 提取顶点和中心点
vertices = data[data['Type'] == 'Vertex'][['X', 'Y', 'Z']].values
vertex_ids = data[data['Type'] == 'Vertex']['ID'].values.astype(int)  # 提取顶点 ID
center_point = data[data['Type'] == 'Center'][['X', 'Y', 'Z']].values.flatten()

# 创建 ID 到数组索引的映射
id_to_index = {id_: idx for idx, id_ in enumerate(vertex_ids)}

# 定义面的顶点 ID 和名称
faces_info = [
    {"face": [4, 8, 12, 10], "name": "屋顶"},
    {"face": [2, 6, 12, 10], "name": "屋顶的另一部分"},
    {"face": [8, 4, 3, 7], "name": "侧面"},
    {"face": [6, 2, 1, 5], "name": "侧面"},
    {"face": [6, 12, 8, 7, 5], "name": "前面"},
    {"face": [4, 10, 2, 1, 3], "name": "后面"},
    {"face": [1, 3, 7, 5], "name": "底面"}
]

# 将面的顶点 ID 转换为数组索引
faces = [[id_to_index[id_] for id_ in info["face"]] for info in faces_info]

# 计算每个面的法向量
def calculate_face_normal(face_vertices):
    # 取面的前三个顶点计算法向量
    A, B, C = face_vertices[:3]
    AB = B - A
    AC = C - A
    normal = np.cross(AB, AC)
    normal = normal / np.linalg.norm(normal)  # 归一化
    return normal

# 调整法向量方向，使其朝外
def adjust_normal_direction(normal, face_center, model_center):
    to_center = model_center - face_center
    if np.dot(normal, to_center) > 0:
        normal = -normal  # 如果法向量指向内部，取反
    return normal

# 计算每个面的法向量并导出结果
results = []
for face, info in zip(faces, faces_info):
    face_vertices = [vertices[v_idx] for v_idx in face]
    face_center = np.mean(face_vertices, axis=0)  # 面的中心点
    normal = calculate_face_normal(face_vertices)
    normal = adjust_normal_direction(normal, face_center, center_point)
    results.append({
        "face": info["face"],
        "name": info["name"],
        "normal": normal
    })

# 导出结果
for result in results:
    print(f"{result['face']}, {result['name']}, 法向量: {result['normal']}")