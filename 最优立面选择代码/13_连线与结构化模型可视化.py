import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

# ==================== 1. 读取 CSV 数据 ====================
# 读取房屋结构数据
house_csv_path = r'F:\毕设\p2_LOD3_00_School\vertices_and_center.csv'
house_data = pd.read_csv(house_csv_path)

# 读取摄影中心点数据
photo_csv_path = r'F:\毕设\p2_LOD3_00_School\00_local坐标摄影中心.csv'
photo_data = pd.read_csv(photo_csv_path)

# 读取 face 和 ID 的对应关系表格
face_id_csv_path = r'F:\毕设\p2_LOD3_00_School\每个面可以拍到的摄影中心.csv'
face_id_table = pd.read_csv(face_id_csv_path)

# ==================== 2. 提取房屋结构数据 ====================
# 提取顶点和中心点
vertices = house_data[house_data['Type'] == 'Vertex'][['X', 'Y', 'Z']].values
vertex_ids = house_data[house_data['Type'] == 'Vertex']['ID'].values.astype(int)  # 提取顶点 ID
house_center = house_data[house_data['Type'] == 'Center'][['X', 'Y', 'Z']].values.flatten()

# 创建 ID 到数组索引的映射
id_to_index = {id_: idx for idx, id_ in enumerate(vertex_ids)}

# 定义房屋结构的面（通过顶点 ID）
faces_ids = [
    [4, 8, 12, 10],  # 屋顶
    [2, 6, 12, 10],   # 屋顶的另一部分
    [8, 4, 3, 7],     # 侧面
    [6, 2, 1, 5],     # 侧面
    [6, 12, 8, 7, 5], # 前面
    [4, 10, 2, 1, 3], # 后面
    [1, 3, 7, 5]      # 底面
]

# 将面的顶点 ID 转换为数组索引
faces = [[id_to_index[id_] for id_ in face] for face in faces_ids]

# ==================== 3. 提取摄影中心点数据 ====================
photo_centers = photo_data[['x', 'y', 'z']].values
photo_ids = photo_data['ID'].values.astype(str)  # 确保 ID 为字符串
photo_center = [3.04358344, -0.13160541, 54.95842676]  # 手动定义中心点

# ==================== 4. 创建颜色映射 ====================
# 为每个 face 分配一个颜色
unique_faces = list(set(tuple(map(int, face.strip('[]').split(','))) for face in face_id_table['face'].unique()))
face_to_color = {face: plt.cm.tab20(i) for i, face in enumerate(unique_faces)}

# 将摄影中心点的 ID 映射到对应的 face 和颜色
id_to_face = {row['ID']: tuple(map(int, row['face'].strip('[]').split(','))) for _, row in face_id_table.iterrows()}
id_to_color = {id_: face_to_color[face] for id_, face in id_to_face.items()}

# ==================== 5. 创建 3D 可视化 ====================
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')

# ----- 绘制房屋结构 -----
# 绘制房屋顶点
ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], color='blue', s=50, label='House Vertices', zorder=5)

# 绘制房屋中心点
ax.scatter(*house_center, color='red', s=100, label='House Center', zorder=10)

# 绘制房屋面的几何形状
for face in faces:
    face_vertices = [vertices[v_idx] for v_idx in face]
    ax.add_collection3d(Poly3DCollection([face_vertices], color='lightblue', edgecolor='black', alpha=0.5))

# 添加房屋顶点的 ID 标签
for point, id_str in zip(vertices, vertex_ids):
    ax.text(point[0] + 0.02, point[1] + 0.02, point[2], str(id_str),
            color='black', fontsize=8, ha='left', va='bottom',
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=0.3))

# ----- 绘制摄影中心点数据 -----
# 绘制摄影中心点，并根据 face 着色
for point, id_str in zip(photo_centers, photo_ids):
    color = id_to_color[int(id_str)]  # 根据 ID 获取颜色
    ax.scatter(point[0], point[1], point[2], color=color, s=50, zorder=5)

# 绘制摄影中心点的中心
ax.scatter(*photo_center, color='orange', s=100, label='Photo Center', zorder=10)

# 连接摄影中心点到中心点
for point in photo_centers:
    ax.plot([photo_center[0], point[0]],
            [photo_center[1], point[1]],
            [photo_center[2], point[2]],
            color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

# 添加摄影中心点 ID 标签
for point, id_str in zip(photo_centers, photo_ids):
    ax.text(point[0] + 0.02, point[1] + 0.02, point[2], id_str,
            color='black', fontsize=8, ha='left', va='bottom',
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=0.3))

# ==================== 6. 设置图形属性 ====================
ax.set_xlabel('X (m)', labelpad=12)
ax.set_ylabel('Y (m)', labelpad=12)
ax.set_zlabel('Z (m)', labelpad=12)
ax.set_title('House Structure & Photogrammetric Centers', pad=20)
ax.legend(loc='upper right', fontsize=9)
ax.grid(True, alpha=0.3)

# 优化显示
plt.tight_layout()
plt.show()