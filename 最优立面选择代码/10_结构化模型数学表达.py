import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

def parse_obj(file_path):
    vertices = []
    normals = []
    texcoords = []
    faces = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith('v '):
                _, x, y, z = line.split()
                vertices.append((float(x), float(y), float(z)))
            elif line.startswith('vn '):
                _, nx, ny, nz = line.split()
                normals.append((float(nx), float(ny), float(nz)))
            elif line.startswith('vt '):
                _, u, v = line.split()
                texcoords.append((float(u), float(v)))
            elif line.startswith('f '):
                face = []
                for vertex in line.split()[1:]:
                    parts = vertex.split('/')
                    v_index = int(parts[0]) - 1
                    t_index = int(parts[1]) - 1 if len(parts) > 1 and parts[1] else None
                    n_index = int(parts[2]) - 1 if len(parts) > 2 else None
                    face.append((v_index, t_index, n_index))
                faces.append(face)

    return np.array(vertices), np.array(normals), np.array(texcoords), faces

# 读取 OBJ 文件
file_path = r'F:\毕设\p2_LOD3_00_School\school.obj'
vertices, normals, texcoords, faces = parse_obj(file_path)

# 提取数据
photo_centers = np.array([
    [-1.137535, 5.280116, 50.220249],
    [-1.137535, 5.280116, 58.394634],
    [7.543259, 5.039203, 50.220249],
    [7.543259, 5.039203, 58.394634],
    [-1.437579, -5.302928, 50.220249],
    [-1.437579, -5.302928, 58.394634],
    [7.243215, -5.543840, 50.220249],
    [7.243215, -5.543840, 58.394634],
    [3.171390, 5.160533, 50.220249],
    [3.171390, 5.160533, 60.721153],
    [2.871346, -5.422511, 50.220249],
    [2.871345, -5.422511, 60.721153]
])
ids = np.array([str(i+1) for i in range(len(photo_centers))])

# 定义中心点
center_point = [3.04358344, -0.13160541, 54.95842676]

# 创建 3D 图形
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')

# 绘制中心点
ax.scatter(*center_point, color='red', s=100, label='Center Point', zorder=10)

# 绘制摄影中心点并添加ID标签
scatter = ax.scatter(photo_centers[:, 0],
                     photo_centers[:, 1],
                     photo_centers[:, 2],
                     color='blue',
                     s=50,
                     label='Photo Centers',
                     zorder=5)

# 添加ID文本标签
for point, id_str in zip(photo_centers, ids):
    ax.text(point[0]+0.02,  # X坐标微调
            point[1]+0.02,  # Y坐标微调
            point[2],
            id_str,
            color='black',
            fontsize=8,
            ha='left',
            va='bottom',
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=0.3))

# 连接中心点到每个摄影中心点
for point in photo_centers:
    ax.plot([center_point[0], point[0]],
            [center_point[1], point[1]],
            [center_point[2], point[2]],
            color='gray',
            linestyle='--',
            linewidth=0.5,
            alpha=0.7)

# 绘制OBJ模型
for face in faces:
    face_vertices = [vertices[v_idx] for v_idx, _, _ in face]
    ax.add_collection3d(Poly3DCollection([face_vertices], color='lightblue', edgecolor='black', alpha=0.5))

# 设置图形属性
ax.set_xlabel('X (m)', labelpad=12)
ax.set_ylabel('Y (m)', labelpad=12)
ax.set_zlabel('Z (m)', labelpad=12)
ax.set_title('Photogrammetric Centers with ID Labels and Intersection Points', pad=20)
ax.legend(loc='upper right', fontsize=9)
ax.grid(True, alpha=0.3)

# 优化显示
plt.tight_layout()
plt.show()
