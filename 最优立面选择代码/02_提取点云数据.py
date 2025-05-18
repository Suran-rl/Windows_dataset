import xml.etree.ElementTree as ET
import pandas as pd

# 加载XML文件
xml_file = r'F:\毕设\p2_LOD3_00_School\local坐标.xml'
tree = ET.parse(xml_file)
root = tree.getroot()

# 创建空列表以存储点云数据
points = []

# 遍历每个TiePoint，提取数据
for tie_point in root.findall('.//TiePoint'):
    # 提取位置
    position = tie_point.find('Position')
    x = float(position.find('x').text)
    y = float(position.find('y').text)
    z = float(position.find('z').text)

    # 提取颜色
    color = tie_point.find('Color')
    red = float(color.find('Red').text)
    green = float(color.find('Green').text)
    blue = float(color.find('Blue').text)

    # 提取每个测量
    measurements = []
    for measurement in tie_point.findall('Measurement'):
        photo_id = measurement.find('PhotoId').text
        mx = float(measurement.find('x').text)
        my = float(measurement.find('y').text)
        measurements.append({"PhotoId": photo_id, "mx": mx, "my": my})

    # 将数据添加到列表
    points.append({
        'X': x,
        'Y': y,
        'Z': z,
        'Red': red,
        'Green': green,
        'Blue': blue,
        'Measurements': measurements  # 可以选择是否存储详细的测量
    })

# 创建一个DataFrame来存储提取的数据
data = []
for point in points:
    for measurement in point["Measurements"]:
        data.append({
            'X': point['X'],
            'Y': point['Y'],
            'Z': point['Z'],
            'Red': point['Red'],
            'Green': point['Green'],
            'Blue': point['Blue'],
            'PhotoId': measurement['PhotoId'],
            'mx': measurement['mx'],
            'my': measurement['my']
        })

df = pd.DataFrame(data)

# 保存为CSV文件
output_file = r'F:\毕设\p2_LOD3_00_School\local坐标点云.csv'  # 输出文件名
df.to_csv(output_file, index=False)
print(f'Point cloud data has been exported to {output_file}')