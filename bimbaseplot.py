from pyp3d import *
import pandas as pd
import os


# 定义参数化模型
class bimbaseplot(Component):
    # 定义各个参数及其默认值
    def __init__(self):
        Component.__init__(self)
        self["顶面半径"] = Attr(0.01, obvious=True)
        # obvious 属性的可见性 True时可见，False为不可见。默认为False
        # readonly 属性的只读性 True时不可调，为置灰状态，False为可调状态。默认为False

    @export
    # 模型造型
    def replace(self):
        # 设置变量，同时调用参数(简化书写过程)

        # 绘制模型
        fds_plot = combine()

        base_square = scale(d) * Section(
            Vec3(0.5, 0.5, 0),
            Vec3(0.5, -0.5, 0),
            Vec3(-0.5, -0.5, 0),
            Vec3(-0.5, 0.5, 0),
        )
        dfs, file_names = self.read_xlsx_files()
        df_merged = pd.concat(dfs, ignore_index=True)
        print(file_names)
        print(len(df_merged))
        for row in df_merged.itertuples(index=True, name="Row"):
            # print(f"Index: {row[0]}, X: {row[1]}, Y: {row[2]}, Temperature: {row[3]}")
            cell = trans(row[1] * 1000, row[2] * 1000, 0) * base_square
            rgb_value = self.color_map(row[3])
            cell.color(rgb_value)
            fds_plot.append(cell)

        self["圆柱体"] = fds_plot

    # 定义函数
    def read_xlsx_files(self, directory=None):
        """
        读取指定文件夹内的所有 .xlsx 文件，并返回一个 DataFrame 列表。

        参数：
        - directory: str，可选，指定文件夹路径，默认为当前脚本所在目录。

        返回：
        - dfs: list，包含所有 Excel 文件的 DataFrame 列表
        - file_names: list，对应每个 DataFrame 的文件名
        """
        if directory is None:
            directory = os.path.dirname(os.path.abspath(__file__))  # 当前脚本目录

        dfs = []  # 存储 DataFrame
        file_names = []  # 存储文件名

        for file_name in os.listdir(directory):
            if file_name.endswith(".xlsx"):
                file_path = os.path.join(directory, file_name)

                # 读取 Excel 文件
                df = pd.read_excel(file_path, engine="openpyxl", header=None)

                dfs.append(df)
                file_names.append(file_name)

                # print(f"读取文件: {file_name}, 记录数: {len(df)}")

        return dfs, file_names  # 返回 DataFrame 列表和文件名列表

    def color_map(self, T):  # 读取温度值返回rgb值
        RGB_value = []
        if T <= 20:
            RGB_value = [0.001, 0.000, 0.014]
        elif 20 < T <= 30:
            RGB_value = [0.183, 0.022, 0.134]
        elif 30 < T <= 40:
            RGB_value = [0.396, 0.057, 0.255]
        elif 40 < T <= 50:
            RGB_value = [0.642, 0.150, 0.366]
        elif 50 < T <= 60:
            RGB_value = [0.901, 0.322, 0.377]
        elif 60 < T <= 70:
            RGB_value = [0.993, 0.611, 0.383]
        elif 70 < T <= 80:
            RGB_value = [0.997, 0.878, 0.565]
        else:
            RGB_value = [0.988, 0.998, 0.645]
        return RGB_value  # 返回RGB值，格式为列表
    
    def color_map_Inferno(self, T):  # 读取温度值返回rgb值 Inferno色图
        RGB_value = []
        if T <= 20:
            RGB_value =[0.0, 0.0, 0.015]
        elif 20 < T <= 28:
            RGB_value = [0.173, 0.043, 0.231]
        elif 28 < T <= 36:
            RGB_value = [0.349, 0.059, 0.369]
        elif 36 < T <= 44:
            RGB_value = [0.498, 0.090, 0.345]
        elif 44 < T <= 52:
            RGB_value = [0.627, 0.149, 0.267]
        elif 52 < T <= 60:
            RGB_value = [0.749, 0.220, 0.188]
        elif 60 < T <= 68:
            RGB_value = [0.855, 0.341, 0.129]
        elif 68 < T <= 76:
            RGB_value = [0.933, 0.498, 0.129]
        elif 76 < T <= 84:
            RGB_value = [0.976, 0.667, 0.243]
        elif 84 < T <= 92:
            RGB_value = [0.992, 0.835, 0.463]
        else:
            RGB_value = [0.988, 1.0, 0.643]
        return RGB_value  # 返回RGB值，格式为列表


# 输出模型
if __name__ == "__main__":
    FinalGeometry = bimbaseplot()
    FinalGeometry.replace()
    place(FinalGeometry)
