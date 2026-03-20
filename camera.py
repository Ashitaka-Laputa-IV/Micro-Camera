# 相机类
# 功能：封装相机操作，包括 SD 卡挂载、拍照、文件管理和深度睡眠

import uos
import machine
import camera
import time

class Camera:
    """相机类，封装 ESP32-CAM 的核心功能"""
    
    def __init__(self):
        """初始化相机"""
        self.led = machine.Pin(4, machine.Pin.OUT, value=0)  # 初始化闪光灯，默认关闭
        self.sd_mounted = False
        self._mount_sd()
    
    def _mount_sd(self):
        """挂载 SD 卡"""
        try:
            uos.mount(machine.SDCard(), "/sd")
            self.sd_mounted = True
        except Exception as e:
            self.sd_mounted = False
    
    def _get_next_number(self, prefix):
        """获取下一个编号
        
        直接从文件中读取下次要使用的编号，使用后更新文件
        
        Args:
            prefix: 文件前缀，用于区分不同类型的文件
        """
        filename = f'{prefix}_number.txt'
        try:
            # 读取当前存储的编号（下次要使用的）
            with open(filename, 'r') as f:
                num = int(f.read().strip())
        except (OSError, ValueError):
            # 文件不存在或内容无效，从 999 开始
            num = 999
        
        # 更新文件为下一个编号
        try:
            with open(filename, 'w') as f:
                f.write(str(num + 1))
        except Exception as e:
            pass
        
        return num
    
    def _get_next_image_number(self):
        """获取下一个图像编号"""
        return self._get_next_number('image')
    
    def _get_next_video_number(self):
        """获取下一个视频编号"""
        return self._get_next_number('video')
    
    def capture(self, filename=None):
        """拍照并保存
        
        Args:
            filename: 可选，指定保存的文件名
            
        Returns:
            str: 保存的文件路径，失败返回 None
        """
        if not self.sd_mounted:
            return None
        
        # 生成文件名
        if filename is None:
            num = self._get_next_image_number()
            filename = f'sd/Image{num}.jpg'
        
        try:
            # 初始化相机
            camera.init()
            
            # 打开闪光灯
            self.led.on()
            time.sleep(0.3)  # 短暂延迟，确保闪光灯完全开启
            
            # 拍照
            buf = camera.capture()
            
            # 关闭闪光灯
            self.led.off()
            
            # 释放相机资源
            camera.deinit()
            
            # 保存图片
            with open(filename, 'wb') as f:
                f.write(buf)
            
            return filename
            
        except Exception as e:
            # 确保资源释放
            try:
                camera.deinit()
                self.led.off()
            except:
                pass
            return None
    
    def sleep(self):
        """进入深度睡眠模式"""
        machine.deepsleep()
    
    def record(self, filename=None, duration=10):
        """录制视频并保存
        
        Args:
            filename: 可选，指定保存的文件名
            duration: 录制时长（秒），默认10秒
            
        Returns:
            str: 保存的文件路径，失败返回 None
        """
        if not self.sd_mounted:
            return None
        
        # 生成文件名
        if filename is None:
            num = self._get_next_video_number()
            filename = f'sd/Video{num}.avi'
        
        try:
            # 初始化相机
            camera.init()
            
            # 打开闪光灯
            self.led.on()
            time.sleep(0.3)  # 短暂延迟，确保闪光灯完全开启
            
            # 打开文件准备写入
            with open(filename, 'wb') as f:
                # 开始时间
                start_time = time.time()
                
                # 持续录制直到达到指定时长
                while time.time() - start_time < duration:
                    # 捕获一帧
                    buf = camera.capture()
                    # 写入文件
                    f.write(buf)
                    # 短暂延迟，控制帧率
                    time.sleep(0.1)  # 约10fps
            
            # 关闭闪光灯
            self.led.off()
            
            # 释放相机资源
            camera.deinit()
            
            return filename
            
        except Exception as e:
            # 确保资源释放
            try:
                camera.deinit()
                self.led.off()
            except:
                pass
            return None
    
    def run(self):
        """执行完整的拍照流程"""
        # 拍照
        self.capture()
        # 进入深度睡眠
        self.sleep()
    
    def run_video(self):
        """执行完整的录像流程"""
        # 录像
        self.record()
        # 进入深度睡眠
        self.sleep()

# 使用示例
if __name__ == "__main__":
    cam = Camera()
    # 拍照
    # cam.run()
    # 录像
    cam.run_video()
