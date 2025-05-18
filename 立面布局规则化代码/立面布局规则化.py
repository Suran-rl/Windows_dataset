import cv2
import numpy as np

class WindowProcessor:
    def __init__(self, img_path: str):
        # 加载输入图片
        self.input_image = cv2.imread(img_path)
        if self.input_image is None:
            raise FileNotFoundError(f"无法读取图片: {img_path}")
        self.width, self.height = self.input_image.shape[:2]

        # 初始化其他变量
        self.standard_binary_image = None
        self.opening = None
        self.windows = []

    def img_preprocess(self):
        """预处理：假设输入图片已经经过语义分割，提取标准二值图"""
        # 示例：假设语义分割后只保留窗户部分（这里用简单阈值分割代替）
        gray = cv2.cvtColor(self.input_image, cv2.COLOR_BGR2GRAY)
        _, self.standard_binary_image = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        cv2.imwrite("standard_binary_image.png", self.standard_binary_image)  # 调试：保存二值化图像

    def apply_morphological_denoising(self):
        """形态学去噪：先腐蚀去除小噪声，再膨胀恢复窗户形状"""
        kernel = np.ones((3, 3), np.uint8)
        eroded = cv2.erode(self.standard_binary_image, kernel, iterations=1)
        dilated = cv2.dilate(eroded, kernel, iterations=2)

        # 开运算去除孤立噪点
        self.opening = cv2.morphologyEx(dilated, cv2.MORPH_OPEN, kernel, iterations=1)
        cv2.imwrite("opening.png", self.opening)  # 调试：保存开运算后的图像

    def extract_windows(self):
        """连通组件分析提取窗户"""
        self.num_labels, self.labels, self.stats, self.centroids = cv2.connectedComponentsWithStats(
            self.opening, connectivity=8
        )

        # 过滤小区域（非窗户）
        min_area = self.width * self.height * 0.0025  # 调整最小窗户面积阈值
        self.windows = []
        for i in range(1, self.num_labels):  # 跳过背景（label=0）
            x, y, w, h, area = self.stats[i]
            if area < min_area:
                continue  # 忽略小区域
            self.windows.append({
                "id": i,
                "x": x, "y": y, "width": w, "height": h,
                "centroid": (int(self.centroids[i][0]), int(self.centroids[i][1]))
            })
        print(f"找到的窗户数量: {len(self.windows)}")  # 调试：打印找到的窗户数量

    def align_horizontally(self, threshold=0.1):
        """按Y坐标分组并水平对齐"""
        if not self.windows:
            return

        y_coords = [w["centroid"][1] for w in self.windows]
        y_coords.sort()

        # 动态计算分组阈值（按图像高度的10%）
        y_threshold = self.height * threshold

        # 分组
        groups = []
        current_group = [self.windows[0]]
        for i in range(1, len(self.windows)):
            if abs(self.windows[i]["centroid"][1] - current_group[0]["centroid"][1]) < y_threshold:
                current_group.append(self.windows[i])
            else:
                groups.append(current_group)
                current_group = [self.windows[i]]
        if current_group:
            groups.append(current_group)

        # 同一层的窗户Y坐标对齐
        for group in groups:
            avg_y = sum(w["centroid"][1] for w in group) // len(group)
            for w in group:
                w["y"] = avg_y - w["height"] // 2  # 调整Y坐标，保持高度不变

    def align_vertically(self, threshold=0.1):
        """按X坐标分组并垂直对齐"""
        if not self.windows:
            return

        x_coords = [w["centroid"][0] for w in self.windows]
        x_coords.sort()

        # 动态计算分组阈值（按图像宽度的10%）
        x_threshold = self.width * threshold

        # 分组
        groups = []
        current_group = [self.windows[0]]
        for i in range(1, len(self.windows)):
            if abs(self.windows[i]["centroid"][0] - current_group[0]["centroid"][0]) < x_threshold:
                current_group.append(self.windows[i])
            else:
                groups.append(current_group)
                current_group = [self.windows[i]]
        if current_group:
            groups.append(current_group)

        # 同一列的窗户X坐标对齐
        for group in groups:
            avg_x = sum(w["centroid"][0] for w in group) // len(group)
            for w in group:
                w["x"] = avg_x - w["width"] // 2  # 调整X坐标，保持宽度不变

    def unify_window_sizes(self):
        """统一窗户大小"""
        if not self.windows:
            return

        # 计算所有窗户的平均宽度和高度
        avg_width = sum(w["width"] for w in self.windows) // len(self.windows)
        avg_height = sum(w["height"] for w in self.windows) // len(self.windows)

        # 调整所有窗户尺寸
        for w in self.windows:
            w["width"] = avg_width
            w["height"] = avg_height

    def generate_semantic_map(self, output_path: str):
        """生成最终语义图"""
        # 创建空白图像用于绘制结果
        semantic_map = np.zeros_like(self.input_image)

        # 绘制每个窗户
        for window in self.windows:
            x, y, w, h = window["x"], window["y"], window["width"], window["height"]
            cv2.rectangle(semantic_map, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)

        # 保存结果
        cv2.imwrite(output_path, semantic_map)
        print(f"结果已保存到: {output_path}")  # 调试：打印保存路径

    def run_pipeline(self, input_path: str, output_path: str):
        """主流程：加载图片 -> 预处理 -> 去噪 -> 提取窗户 -> 规则化 -> 导出结果"""
        self.img_preprocess()
        self.apply_morphological_denoising()
        self.extract_windows()
        self.align_horizontally()
        self.align_vertically()
        self.unify_window_sizes()
        self.generate_semantic_map(output_path)

# 测试代码
if __name__ == "__main__":
    img_path = r"C:\Users\Lenovo\Desktop\14f.png"
    output_path = r"C:\Users\Lenovo\Desktop\14fR.png"

    try:
        processor = WindowProcessor(img_path)
        processor.run_pipeline(img_path, output_path)
    except FileNotFoundError as e:
        print(e)
