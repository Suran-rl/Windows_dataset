import open3d as o3d
import pandas as pd
import numpy as np

# 读取CSV文件
file_path = r'F:\毕设\p2_LOD3_00_School\local坐标点云.csv'
data = pd.read_csv(file_path)

# 提取点云坐标和颜色
points = data[['X', 'Y', 'Z']].to_numpy()  # 提取X, Y, Z坐标
colors = data[['Red', 'Green', 'Blue']].to_numpy()  # 提取RGB颜色

# 创建点云对象
point_cloud = o3d.geometry.PointCloud()
point_cloud.points = o3d.utility.Vector3dVector(points)  # 设置点云坐标
point_cloud.colors = o3d.utility.Vector3dVector(colors)  # 设置点云颜色

# 可视化点云
o3d.visualization.draw_geometries([point_cloud])