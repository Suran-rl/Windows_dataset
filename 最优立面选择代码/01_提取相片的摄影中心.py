import xml.etree.ElementTree as ET


def extract_camera_centers(file_path, output_file_path):
    camera_centers = []

    # 读取XML文件
    tree = ET.parse(file_path)
    root = tree.getroot()

    # 遍历所有的Photo节点
    for photo in root.findall(".//Photo"):
        # 提取摄影中心的坐标
        center_x = float(photo.find('./Pose/Center/x').text)
        center_y = float(photo.find('./Pose/Center/y').text)
        center_z = float(photo.find('./Pose/Center/z').text)

        # 将摄影中心添加到列表中
        camera_centers.append((center_x, center_y, center_z))

    # 将结果输出到文件
    with open(output_file_path, 'w') as output_file:
        for idx, center in enumerate(camera_centers):
            output_file.write(f" {center[0]}, {center[1]}, {center[2]}\n")


# 输入文件路径
input_file_path = r'F:\毕设\p2_LOD3_00_School\local坐标.xml' # 使用原始字符串
output_file_path =  r'F:\毕设\p2_LOD3_00_School\00_local坐标摄影中心.csv' # 输出TXT文件的名称

# 调用函数提取摄影中心并输出到文件
extract_camera_centers(input_file_path, output_file_path)

print(f"摄影中心已提取并保存在 '{output_file_path}' 中。")