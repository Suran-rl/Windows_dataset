import numpy as np
import pandas as pd

# 1. 加载结构化模型的法向量
vertex_normals_path = r'F:\毕设\p2_LOD3_00_School\vertex_normals1.csv'
vertex_normals_data = pd.read_csv(vertex_normals_path, encoding='gbk')  # 指定编码为 gbk
vertex_normals = vertex_normals_data[['NX', 'NY', 'NZ']].to_numpy()  # 提取法向量
vertex_faces = vertex_normals_data['face'].tolist()  # 提取面的顶点 ID

# 2. 加载相片的法向量
photo_normals_path = r'F:\毕设\p2_LOD3_00_School\指向中心的法向量.csv'
photo_normals_data = pd.read_csv(photo_normals_path, encoding='gbk')  # 指定编码为 gbk
photo_normals = photo_normals_data[['x', 'y', 'z']].to_numpy()  # 提取相片的法向量
photo_names = photo_normals_data['ID'].tolist()  # 提取相片名称

# 3. 加载每个面可以拍到的摄影中心表格
face_photo_path = r'F:\毕设\p2_LOD3_00_School\每个面可以拍到的摄影中心.csv'
face_photo_data = pd.read_csv(face_photo_path, encoding='gbk')  # 指定编码为 gbk

# 将 face 列转换为字符串（确保格式一致）
face_photo_data['face'] = face_photo_data['face'].astype(str)

# 4. 计算夹角
def compute_angle(v1, v2):
    """计算两个向量之间的夹角（弧度）"""
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    cos_theta = dot_product / (norm_v1 * norm_v2)
    return np.arccos(np.clip(cos_theta, -1.0, 1.0))  # 防止数值误差

# 初始化结果列表
results = []

# 遍历每个结构化模型的法向量
for i, (vertex_normal, face) in enumerate(zip(vertex_normals, vertex_faces)):
    # 获取当前面可以拍到的摄影中心 ID
    valid_photo_ids = face_photo_data[face_photo_data['face'] == face]['ID'].tolist()

    # 筛选出与当前面相关的相片法向量
    valid_photo_indices = [j for j, photo_name in enumerate(photo_names) if int(photo_name) in valid_photo_ids]

    if not valid_photo_indices:
        # 如果没有相关相片，记录为未找到
        results.append({
            'Face': face,
            'Best Photo Name': '未找到',
            'Min Angle (Degrees)': None
        })
        continue

    min_angle = float('inf')  # 初始化最小夹角
    best_photo_name = None    # 初始化最佳相片名称

    # 遍历与当前面相关的相片法向量
    for j in valid_photo_indices:
        # 调整相片法向量方向（如果需要）
        photo_normal = photo_normals[j]
        angle = compute_angle(vertex_normal, photo_normal)

        # 如果夹角大于 90 度，取反法向量重新计算
        if angle > np.pi / 2:
            photo_normal = -photo_normal
            angle = compute_angle(vertex_normal, photo_normal)

        if angle < min_angle:
            min_angle = angle
            best_photo_name = photo_names[j]

    # 记录结果
    results.append({
        'Face': face,
        'Best Photo Name': best_photo_name,
        'Min Angle (Degrees)': np.degrees(min_angle)
    })

# 5. 输出结果
for result in results:
    print(f"面 {result['Face']}:")
    print(f"  最佳相片名称: {result['Best Photo Name']}")
    if result['Min Angle (Degrees)'] is not None:
        print(f"  最小夹角: {result['Min Angle (Degrees)']:.2f} 度")
    else:
        print("  最小夹角: 未找到")
    print()

# 6. 将结果保存为 CSV 文件
results_df = pd.DataFrame(results)
output_csv_path = r'F:\毕设\p2_LOD3_00_School\新匹配相片3.csv'
results_df.to_csv(output_csv_path, index=False, encoding='gbk')  # 指定编码为 gbk
print(f"结果已保存到 {output_csv_path}")