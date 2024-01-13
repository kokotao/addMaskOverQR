这是一个用OpenCV计算机视觉库结合python对带有二维码的图片或者电子票据进行识别并处理的项目；
现在只做了对原有二维码进行批量识别并替换的功能；
其他的功能可以在改项目基础上进行扩展、改进。

### **二维码算法调优：**

加入：
##### 亮度和对比度调整
    alpha = 1.8  # 对比度因子
    beta = -35  # 亮度因子
    adjusted_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    # cv2.imshow('Adjusted Image', adjusted_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
#### 转换为灰度图像
    gray = cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('Grayscale Image', gray)
    # cv2.waitKey(0)
#### 双边滤波
    filter_image = cv2.bilateralFilter(gray, 13, 26, 6)
    # cv2.imshow('Filtered Image', filter_image)
    # cv2.waitKey(0)
#### 反二值化
    _, binary_image = cv2.threshold(filter_image, 210, 255, cv2.THRESH_BINARY_INV)
    # cv2.imshow('Binary Image', binary_image)
    # cv2.waitKey(0)

#### **效果图**：

![业务票据1.jpg](1705117413img
/556/业务票据.jpg)
