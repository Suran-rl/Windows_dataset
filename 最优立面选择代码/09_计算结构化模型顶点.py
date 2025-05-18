import pandas as pd
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

# 定义中心点
center_point = [3.04358344, -0.13160541, 54.95842676]

# 创建顶点 DataFrame
vertices_df = pd.DataFrame(vertices, columns=['X', 'Y', 'Z'])
vertices_df['Type'] = 'Vertex'

# 创建中心点 DataFrame
center_point_df = pd.DataFrame([center_point], columns=['X', 'Y', 'Z'])
center_point_df['Type'] = 'Center'

# 合并 DataFrame
combined_df = pd.concat([vertices_df, center_point_df], ignore_index=True)

# 导出为 CSV 文件
combined_df.to_csv(r'F:\毕设\p2_LOD3_00_School\vertices_and_center.csv', index=False)
