## Outlook墨水屏台历 WeatherStation by RaspberryPi
![image](https://github.com/ShaderFallback/RaspberryPi-WeatherStation/blob/master/photo/demo0.jpg)
![image](https://github.com/ShaderFallback/RaspberryPi-WeatherStation/blob/master/photo/demo1.jpg)
![image](https://github.com/ShaderFallback/RaspberryPi-WeatherStation/blob/master/photo/demo2.jpg)

### Display Time, Weather Forecast, and RSS News

- **By default, it displays RSS news. The news source can be modified in the code at line 316.**
- **To switch back to the schedule, uncomment lines 446 and 447, and comment out lines 448 and 449.**

### Hardware List

- **Raspberry Pi Zero W**
- **Waveshare 7.5inch e-Paper Display (Black and White)**
- **e-Paper Driver HAT**

    e-Paper Related Information:
[http://www.waveshare.net/wiki/7.5inch_e-Paper_HAT](http://www.waveshare.net/wiki/7.5inch_e-Paper_HAT)

### Raspberry Pi

- **It is recommended to use the official Raspbian OS**
[https://www.raspberrypi.org/downloads/](https://www.raspberrypi.org/downloads/)
- **Python 3.0 or above**
- **Enable GPIO**
- **Install sudo**

### Usage

- **Extract the files to the home directory.**
- **Modify the city in `scripts/WeatherStation.py` at line 24 with the code at the end of the URL.**

```python
r = requests.get('http://t.weather.sojson.com/api/weather/city/101010100')
```
- **To find city codes, please refer to the `scripts/city_code.json` file.(this WeatherAPI only China City)**
- **Edit the `rc.local` file and add the startup item before `Exit 0`.**
``` python
su pi -c "exec /home/pi/WeatherStation/startWeather.sh"
``` 
- **Reboot the Raspberry Pi with sudo reboot**


### 3D Printed Case
- **The model in the pictures was printed using an FDM printer. In northern winters, please adjust the PLA nozzle temperature appropriately to prevent extrusion difficulties.**
- **The model is measured in centimeters (CM, scaled to 10 in Cura). Please pay attention to the print size.**
- **There are two versions of the model with thicknesses of 1.9CM and 2.5CM. If the driver board is directly plugged in, use the 2.5CM thick version (refer to internal details in the photos).**
- **The Model folder contains Maya source files (2014 and above). Modify them as needed.**
- **The base is available in versions with and without logos, choose according to your preference.**

### Others
- **The directory includes PSD files for easy reference and layout changes.**
- **To display rulers in Photoshop, go to View > Rulers, then right-click on the ruler to change the unit to "pixels". This makes it easy to set coordinate positions when pulling out guidelines.**
  

### 显示时间天气预报和RSS 新闻
- **默认显示RSS新闻,新闻源可以修改代码316 行** 
- **如果想改回日程,取消注释446，447 行,并注释448,449行** 

### 硬件清单
- **树莓派 ZeroW** 
- **微雪7.5inch e-Paper 墨水屏(黑白)** 
- **e-Paper Driver HAT 驱动板** 

墨水屏相关资料
[http://www.waveshare.net/wiki/7.5inch_e-Paper_HAT](http://www.waveshare.net/wiki/7.5inch_e-Paper_HAT)

### 树莓派

- **建议使用 官方的 Raspbian 系统** 
[https://www.raspberrypi.org/downloads/](https://www.raspberrypi.org/downloads/)
- **Python 3.0 以上**
- **开启 gpio**
- **安装 sudo**

### 使用
- **解压文件到 home 目录下** 
- **修改城市 scripts/ WeatherStation.py 24行 网址末尾代码** 

``` python
r =requests.get('http://t.weather.sojson.com/api/weather/city/101010100')
```
- **查询城市代码 请查看 scripts/ city_code.json 文件**
- **编辑 rc.local 文件 在 Exit 0 之前添加开机 启动项**

``` python
su pi -c "exec /home/pi/WeatherStation/startWeather.sh"
``` 
- **重启树莓派 sudo reboot**

### 3D打印外壳
- **图片中模型使用FDM 打印机，北方冬天请适当提升PLA喷嘴温度，防止挤出困难**
- **模型制作的单位为厘米CM(在Cura中缩放为10) 请注意打印尺寸**
- **模型分为两种厚度版，1.9CM厚/2.5CM厚 两个版本，驱动板直插的话需要使用2.5CM 厚的版本(内部细节请看photo中图片)**
- **Model文件夹中已包含maya(2014及以上)模型源文件,如有特殊需求请自行修改**
- **底座有Logo 版和无Logo版 可自行选择**

![image](https://github.com/ShaderFallback/RaspberryPi-WeatherStation/blob/master/photo/demo3.jpg)

- **打印参数参考**
![image](https://github.com/ShaderFallback/RaspberryPi-WeatherStation/blob/master/photo/Pla1.png)
![image](https://github.com/ShaderFallback/RaspberryPi-WeatherStation/blob/master/photo/Pla2.png)
![image](https://github.com/ShaderFallback/RaspberryPi-WeatherStation/blob/master/photo/Pla3.png)
![image](https://github.com/ShaderFallback/RaspberryPi-WeatherStation/blob/master/photo/Pla4.png)

### 其他
- **目录中包含PSD文件 方便参考改变布局，
PS 显示标尺  视图 > 标尺 ，在标尺上右键切换单位为 “像素” 
拉出参考线时就可以很容易确定 坐标位置**


- **有任何问题欢迎给我留言 :)**
