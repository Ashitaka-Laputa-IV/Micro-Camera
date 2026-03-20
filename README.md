# Micro-Camera

本教程提供了在 ESP32-CAM 开发板上设置 MicroPython 的逐步说明，并将其变成一个可以拍照并将照片保存到 SD 卡的小型数码相机。ESP32-CAM 开发板是 ESP32 的扩展板，配备了一个支持高达 4GB 的 SD 卡插槽、OV2640 摄像头和一个非常明亮的 LED，非常适合这个项目。

![alt text](images/Micro-Camera.jpg)

## 将 MicroPython 刷入 ESP32-CAM

我发现最好的固件版本由 [shariltumin](https://github.com/shariltumin) 维护，可以在[这里](https://github.com/shariltumin/esp32-cam-micropython/tree/master/firmwares)下载。请务必查看他的[博客](https://kopimojo.blogspot.com/)，他在博客中讨论了 MicroPython 摄像头项目的进展。

下载固件后，需要安装 **esptool**：

```shell
pip install esptool
```

将 USB 转 TTL UART 串口转换器连接到 ESP32-CAM 开发板，并将 IO0 引脚接地（绿色所示）进入引导加载程序模式。

![alt text](images/ESPflash.png)

_按下 RST 按钮_

然后，擦除 ESP32 上的闪存：

```shell
esptool.py --port /dev/ttyUSB0 erase_flash
```

进入放置固件的目录：

_按下 RST 按钮_

```shell
esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 ESP32CAM_firmware.bin
```

现在 ESP32-CAM 开发板上已经有 MicroPython 了！

将 IO0 引脚与地断开，然后 _按下 RST 按钮_

## 将 MicroPython 代码放入 ESP32-CAM 开发板

安装 ampy

```shell
pip install adafruit-ampy
```

克隆 Micro-Camera 代码：

```shell
git clone https://github.com/KipCrossing/Micro-Camera
```

进入 Micro-Camera 目录：

```shell
cd Micro-Camera
```

将代码放入开发板

```shell
ampy --port /dev/ttyUSB0 put boot.py
ampy --port /dev/ttyUSB0 put main.py
```

插入 SD 卡，按下 RST 按钮，观察摄像头闪光并拍照。

## 摄像头模块

```python
import camera

# 设置摄像头参数
camera.framesize(12) # 0 到 13 之间
camera.quality(63) # 9 到 64 之间
camera.contrast(0) # -3 到 3 之间
camera.saturation(0) # -3 到 3 之间
camera.brightness(0) # -3 到 3 之间
camera.speffect(3) # 0 到 7 之间
camera.whitebalance(2) # 0 到 5 之间
camera.agcgain(0) # 0 到 30 之间
camera.aelavels(0) # -3 到 3 之间
camera.aecvalue(100) # 0 到 1200 之间
camera.pixformat(0) # 0 表示 JPEG，1 表示 YUV422，2 表示 RGB

# 拍照
camera.init()
buf = camera.capture()
camera.deinit()
```

## 闪光 LED

闪光 LED 由引脚 4 控制

```python
import machine
import time

led = machine.Pin(4, machine.Pin.OUT)
led.on()
time.sleep(0.2)
led.off()
```

## 挂载 SD 卡

```python
import uos
import machine

uos.mount(machine.SDCard(), "/sd")

# 打开 SD 卡中的文件

f = open("sd/" + tfile, 'wb')
```

## 示例图像

这是一个展示图像质量的示例（闪光灯开启）

![alt text](images/example.jpg)
