## 墨水屏天气站 
### Raspberry Pi WeatherStation


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
- **修改城市 WeatherStation.py 24行 网址末尾代码** 

``` python
r =requests.get('http://t.weather.sojson.com/api/weather/city/101010100')
```
- **查询城市代码 请查看 city_code.json 文件**
- **编辑 rc.local 文件 在 Exit 0 之前添加开机 启动项**

``` python
su pi -c "exec /home/pi/WeatherStation/startWeather.sh"
``` 
- **重启树莓派 sudo reboot**

### 其他
- **目录中包含PSD文件 方便参考改变布局，
PS 显示标尺  视图 > 标尺 ，在标尺上右键切换单位为 “像素” 
拉出参考线时就可以很容易确定 坐标位置**

- **图片时彩色时将会被驱动自动转换，灰阶会以抖动（dithering）方式显示**

- **有任何问题欢迎给我留言 :)**
