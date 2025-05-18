import xml.etree.ElementTree as ET
import numpy as np
import csv

# 解析 XML 文件
def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    return root


# 提取相机的旋转矩阵并计算法向量
def extract_normal_vectors(root, building_center):
    normal_vectors = []
    camera_centers = []

    for photo in root.findall('.//Photo'):
        pose = photo.find('Pose')
        rotation = pose.find('Rotation')

        # 提取旋转矩阵的元素
        m00 = float(rotation.find('M_00').text)
        m01 = float(rotation.find('M_01').text)
        m02 = float(rotation.find('M_02').text)
        m10 = float(rotation.find('M_10').text)
        m11 = float(rotation.find('M_11').text)
        m12 = float(rotation.find('M_12').text)
        m20 = float(rotation.find('M_20').text)
        m21 = float(rotation.find('M_21').text)
        m22 = float(rotation.find('M_22').text)

        # 构建旋转矩阵
        rotation_matrix = np.array([
            [m00, m01, m02],
            [m10, m11, m12],
            [m20, m21, m22]
        ])

        # 提取 Z 轴方向（法向量）
        normal_vector = rotation_matrix[:, 2]  # 第三列是 Z 轴

        # 提取相机中心坐标
        center_x = float(pose.find('Center/x').text)
        center_y = float(pose.find('Center/y').text)
        center_z = float(pose.find('Center/z').text)
        camera_center = np.array([center_x, center_y, center_z])

        # 调整法向量方向，使其指向建筑物结构中心
        to_building = building_center - camera_center
        if np.dot(normal_vector, to_building) < 0:
            normal_vector = -normal_vector  # 如果方向相反，取反法向量

        # 将法向量和相机中心添加到列表中
        normal_vectors.append(normal_vector)
        camera_centers.append(camera_center)

    return normal_vectors, camera_centers


# 将法向量和相机中心写入 CSV 文件
def write_to_csv(output_file, normal_vectors, camera_centers):
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # 写入表头
        writer.writerow(['Photo ID', 'Center X', 'Center Y', 'Center Z', 'Normal Vector X', 'Normal Vector Y', 'Normal Vector Z'])
        # 写入数据
        for i, (normal_vector, camera_center) in enumerate(zip(normal_vectors, camera_centers)):
            writer.writerow([i + 1, camera_center[0], camera_center[1], camera_center[2], normal_vector[0], normal_vector[1], normal_vector[2]])


# 主函数
if __name__ == '__main__':
    input_file_path = r'F:\毕设\p2_LOD3_00_School\local坐标.xml'  # 输入 XML 文件路径
    output_file_path = r'F:\毕设\p2_LOD3_00_School\指向中心的法向量.csv'  # 输出 CSV 文件路径

    # 建筑物结构中心
    building_center = np.array([3.04358344, -0.13160541, 54.95842676])

    # 解析 XML 文件
    root = parse_xml(input_file_path)

    # 提取法向量和相机中心
    normal_vectors, camera_centers = extract_normal_vectors(root, building_center)

    # 将法向量和相机中心写入 CSV 文件
    write_to_csv(output_file_path, normal_vectors, camera_centers)

    print(f"法向量和相机中心已成功导出到: {output_file_path}")