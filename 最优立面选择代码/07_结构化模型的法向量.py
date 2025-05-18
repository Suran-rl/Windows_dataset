import trimesh
import numpy as np
import pandas as pd

# 1. 加载OBJ文件
mesh = trimesh.load(r'F:\毕设\p2_LOD3_00_School\school.obj')

# 2. 检查 mesh 的类型
if isinstance(mesh, trimesh.Scene):
    # 如果 mesh 是 Scene 对象，提取其中的几何体
    mesh = mesh.dump().concatenate()  # 将所有几何体合并为一个 Trimesh 对象
elif not isinstance(mesh, trimesh.Trimesh):
    raise ValueError("加载的对象不是 Trimesh 或 Scene 类型")

# 3. 提取唯一的法向量
# 从 mesh.vertex_normals 中提取唯一的法向量
unique_normals = np.unique(mesh.vertex_normals, axis=0)

# 4. 将唯一的法向量保存为 CSV 文件
# 创建一个 DataFrame，包含唯一的法向量
columns = ['NX', 'NY', 'NZ']  # 列名
df = pd.DataFrame(unique_normals, columns=columns)

# 5. 导出为 CSV 文件
output_csv_path = r'F:\毕设\p2_LOD3_00_School\vertex_normals1.csv'
df.to_csv(output_csv_path, index=False)

print(f"唯一的法向量已导出到 {output_csv_path}")
print("唯一的法向量数量:", len(unique_normals))