import cv2
from pyzbar.pyzbar import decode
import numpy as np
import os
import zipfile
import shutil
import tkinter as tk
from tkinter import filedialog
from pyzbar.pyzbar import decode
import qrcode


def detect_and_mask_qr_code(image_path, zip_file_name, icon_path):
    """
    @Author：TaoLuo
    @Department：研发部-java
    @Date: 2024年1月12日22:59:35
    @Description：OpenCV图像识别 动态检测二维码并加入新图片进行遮罩
    """
    # 读取图片

    image_path_bytes = image_path.encode('utf-8')

    image = cv2.imdecode(np.fromfile(image_path_bytes, dtype=np.uint8), cv2.IMREAD_UNCHANGED)

    # 构建相对路径
    relative_path = image_path.split(zip_file_name)[1]
    # 确保 relative_path 不以反斜杠开头
    if relative_path.startswith('\\'):
        relative_path = relative_path[1:]

    relative_path = "img/" + os.path.normpath(relative_path)
    # 获取当前脚本所在的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 将字符串编码为字节序列，指定编码方式为 'utf-8'
    relative_path_bytes = relative_path.encode('utf-8')

    # 构建路径时解码为字符串
    result_path = os.path.join(current_dir, relative_path_bytes.decode('utf-8'))
    result_path_str = str(result_path)
    print("要保存的file", result_path)
    # 确保目标目录存在，如果不存在，则创建
    os.makedirs(os.path.dirname(result_path_str), exist_ok=True)

    if image is None:
        print("Error: Unable to read the image.")
        return
    # 转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 使用 pyzbar 进行二维码检测
    decoded_objects = decode(gray)
    # 如果检测到二维码
    if decoded_objects:
        # 取第一个二维码的位置坐标
        pts = decoded_objects[0].polygon

        # 输出pts的形状和内容
        # print("pts.shape:", pts.shape)
        print("pts:", pts)

        # 在二维码中间添加一个小图片
        icon_bytes = icon_path.encode('utf-8')
        icon = cv2.imdecode(np.fromfile(icon_bytes, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        # icon = cv2.imread("R2.jpg")

        icon_width, icon_height = icon.shape[1], icon.shape[0]

        # 取得二维码的包围盒（Bounding Box）
        rect = cv2.boundingRect(np.array(pts, dtype=int))
        x, y, w, h = rect

        # 调整小图片的大小与包围盒一致
        icon_resized = cv2.resize(icon, (w, h))
        # 获取图像通道数
        channels_image = image[y:y + h, x:x + w].shape[-1]
        channels_icon = icon_resized.shape[-1]
        print("大图通道数：", channels_image, "icon通道数：", channels_icon)
        # 将 icon_resized 调整为3或4通道数
        if channels_icon != 3 and channels_icon != 4:
            # 如果 channels_icon 不等于3或4，将其调整为3
            icon_resized = cv2.cvtColor(icon_resized, cv2.COLOR_BGR2RGB)  # 将图像转为RGB格式，确保通道数为3
        channels_icon = icon_resized.shape[-1]

        # 如果通道数不同，将 image 调整为与 icon_resized 相同的通道数
        if channels_icon != channels_image:
            target_channels = channels_icon

            if channels_image < target_channels:
                # 扩展为目标通道数
                image = np.concatenate(
                    [image, np.ones(image.shape[:-1] + (target_channels - channels_image,), dtype=image.dtype) * 255],
                    axis=-1)
            elif channels_image > target_channels:
                # 裁剪 image 为目标通道数
                image = image[:, :, :target_channels]

        # 将调整大小后的小图片叠加到原始图像上
        image[y:y + h, x:x + w] = icon_resized

        try:
            # uint8
            image = image.astype(np.uint8)
            # success = cv2.imwrite(result_path_str, image)
            # 分离文件名和扩展名
            file_name, extension = os.path.splitext(result_path_str)
            cv2.imencode(extension, image)[1].tofile(result_path_str)
            print("保存路径", result_path_str)
        except Exception as e:
            print("图像保存时出现异常:", str(e))
        # 显示结果图像
        # cv2.imshow("Result", image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
    else:
        # 分离文件名和扩展名
        file_name, extension = os.path.splitext(result_path_str)
        success2 = cv2.imencode(extension, image)[1].tofile(result_path_str)
        print("未检测到二维码或异形的形状，保存的路径", result_path_str)


def process_zip(zip_file_path, icon_path):
    # 创建输出目录
    output_directory = "D:\\workspace\\selfCoding\\pythonProject\\before"
    tempDir = "D:\\temp"
    os.makedirs(output_directory, exist_ok=True)
    # 提取压缩包的文件名（包括扩展名）
    zip_file_name = os.path.basename(zip_file_path)
    # 分离文件名和扩展名
    zip_file_name, extension = os.path.splitext(zip_file_name)
    # 解压缩文件
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # 解压到当前目录
        zip_ref.extractall(tempDir)
    index = 0
    # 遍历解压后的文件夹
    for root, dirs, files in os.walk(tempDir):
        for file in files:
            # 处理图片文件
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(root, file)
                index += 1
                print(image_path)
                detect_and_mask_qr_code(image_path, zip_file_name, icon_path)
                print("处理完成", index)
    # 清理临时文件夹
    shutil.rmtree(tempDir)
    print("处理完成,临时文件夹删除")


def generate_qr_code(data, qr_code_path):
    """
   @Author：TaoLuo
   @Department：研发部-java
    @Date: 2024/1/13
    @Time: 1:05
    @Description：生成二维码
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img.save(qr_code_path)


def get_user_input():
    """
   @Author：TaoLuo
   @Department：研发部-java
    @Date: 2024/1/13
    @Time: 1:11
    @Description：输入文本确认循环事件
    """
    user_input = ""
    while True:
        user_input = input("请输入要生成二维码的信息或网址（输入 'exit' 退出）：")

        if user_input.lower() == 'exit':
            break  # 用户输入 'exit' 时退出循环
        print(f"已保存用户输入：{user_input}")
    return user_input


def main():
    # 创建一个 Tkinter 根窗口
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    # user_input=get_user_input()

    # 生成二维码
    # qr_code_path = "generated_qrcode.png"
    # generate_qr_code(user_input, qr_code_path)
    # 使用文件选择对话框选择压缩包
    zip_file_path = filedialog.askopenfilename(
        title="选择压缩包",
        filetypes=[("Zip 文件", "*.zip")],
    )

    # 使用文件选择对话框选择图标
    icon_path = filedialog.askopenfilename(
        title="选择图标",
        filetypes=[("图像文件", "*.jpg;*.png;*.jpeg")],
    )

    if zip_file_path and icon_path:  # 用户点击了 "取消" 会返回空字符串
        # 执行相应的操作
        process_zip(zip_file_path, icon_path)
        print("处理完成！")


if __name__ == "__main__":
    main()
    # icon_path = "R2.jpg"
    # zip_file_path = "../公司_20240112161930.zip"
    # process_zip(zip_file_path, icon_path)
