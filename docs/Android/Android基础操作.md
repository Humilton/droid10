Android基础操作.md

### 1 工具：[开发工具箱](https://isk.app/)

### 2 编译替换
```bash
C:\Users\hamilton\Desktop\file>adb root
restarting adbd as root

C:\Users\hamilton\Desktop\file>adb remount
remount succeeded

C:\Users\hamilton\Desktop\file>adb push services.jar /system/framework/
....

C:\Users\hamilton\Desktop\file>adb push framework.jar /system/framework/
C:\Users\hamilton\Desktop\file>adb shell rm -rf /system/framework/oat/
C:\Users\hamilton\Desktop\file>adb shell rm -rf /system/framework/arm/
C:\Users\hamilton\Desktop\file>adb shell rm -rf /system/framework/arm64/
....
C:\Users\hamilton\Desktop\file>adb push CarService.apk /system/priv-app/CarService/CarService.apk
....
C:\Users\hamilton\Desktop\file>adb push android.hardware.automotive.audiocontrol@1.0-service /vendor/bin/hw/android.hardware.automotive.audiocontrol@1.0-service
....

C:\Users\hamilton\Desktop\file>adb reboot
```

<https://blog.csdn.net/superlee1125/article/details/115491698>
编译出framework.jar后，先用下面的命令remount：

``adb root;adb remount``

然后把`framework.jar` push到`system/framework/`下面，同时还要**删除**这个目录下面的`oat`，`arm`，`arm64`三个目录(不删除会一直卡在开机动画)，最后再运行下面的命令重启zygote，这样新替换的`framework.jar`就生效了。

``adb shell stop;adb shell start;``

**替换后的文件在`/mnt/scratch/overlay/`下面**
```
D:\tmp>adb shell ls /mnt/scratch/overlay/
product
system
vendor
```

### 3 挂载img文件: 

###### system.img
首先，需要用``simg2img``工具把``system.img``转为为``ext4``文件格式，该工具位于``out/host/linux-x86/bin/simg2img``，可以使用apt-get安装:
```
apt-get install simg2img
```
再使用工具进行转换：
```
simg2img system.img system_new.img
```
会得到一个``system_new.img``，它是 raw 格式的完整镜像:


用Linux挂载命令进行挂载：
```
sudo mount -t ext4 system_new.img XXX
```

挂载完检查全编的镜像中是否有自己的apk.

###### super.img
1. 编译 lpunpack 工具 (生成文件所在目录：`out_sys/host/linux-x86/bin`)
```
source build/envsetup.sh
make lpunpack
```
2. 将 super.img 从 Android sparse image 转换为 raw image
```
simg2img super.img super.img_raw
```
3. 从 raw image 解包出分区镜像文件
```
./lpunpack -p system super.img_raw  system   # 这里 sytem 是目标目录，可以自己创建
```
4. 用Linux挂载命令进行挂载：
```
sudo mount -t ext4 system.img XXX
```

### 4 抓日志
`getLogs.bat`
```bat
adb root
adb shell ps -A > ps.txt
::
::adb shell am dumpheap 1051 /data/local/tmp/system-server.hprof
:: 安装GitBash, 并将C:\Program Files\Git\usr\bin 加到环境变量 
grep system_server ps.txt | awk "{print $2}" | xargs -I {} echo adb shell am dumpheap {} /data/local/tmp/system-server.hprof > tmp.bat
echo adb pull /data/local/tmp/system-server.hprof >> tmp.bat
echo adb shell rm /data/local/tmp/system-server.hprof >> tmp.bat

grep mediaserver ps.txt | awk "{print $2}" |xargs -I {} echo adb shell debuggerd -b {} "> mediaserver.txt"  >> tmp.bat

echo exit >> tmp.bat
start tmp.bat 
cat tmp.bat

adb pull /data/log
adb pull /data/anr
adb pull /data/tombstones
adb pull /data/system/dropbox
adb pull /sys/kernel/debug/binder

md _dump
cd _dump

adb shell uiautomator dump /data/local/tmp/app.uix 
adb pull /data/local/tmp/app.uix
adb shell screencap -p /sdcard/app.png
adb pull /sdcard/app.png

adb shell top -n 1 > top.txt
adb shell free -m > free.txt
adb shell procrank > procrank.txt
adb shell dumpsys > dumpsys.txt
adb shell dumpsys car_service  > dumpsys_car_service.txt
adb shell dumpsys meminfo system_server > system_server_mem.txt
adb shell dumpsys meminfo mediaserver > mediaserver_mem.txt
adb shell dmesg > dmsg.txt
cd ..

adb shell perfetto -o /data/misc/perfetto-traces/trace_file.perfetto-trace -t 30s sched freq idle am wm gfx view binder_driver hal dalvik camera input res memory
adb pull /data/misc/perfetto-traces/trace_file.perfetto-trace

del tmp.bat

pause

```

[Systrace 简介](https://www.androidperformance.com/2019/05/28/Android-Systrace-About/#/%E6%AD%A3%E6%96%87)

``adb shell perfetto -o /data/misc/perfetto-traces/trace_file.perfetto-trace -t 20s sched freq idle am wm gfx view binder_driver hal dalvik camera input res memory``

网站: ``https://ui.perfetto.dev/#!/``

```
做系统稳定性问题分析，当遇到系统卡死时，我们经常要使用“kill -3 pid”来打印System_Server进程各个线程的Java调用栈，根据线程状态及调用栈来更进一步定位问题点，当然某个应该界面卡顿时间长时也可以通过这个命令来抓取Java调用栈进行分析。
注意native进程是不能用kill -3来打trace的，而是使用debuggerd.
```


```
adb shell dumpsys car_service  --help
adb shell dumpsys car_service  --services CarAudioService > CarAudioService.txt  # dump CarAudioService
```

