# 原神显示设置工具

![运行截图](https://github.com/OrdosX/genshin-resolution-tool/blob/main/screenshot.jpg?raw=true)

为原神自定义任意分辨率和是否全屏，一键傻瓜式操作。

## 使用

### （推荐）下载打包好的exe文件

点击右侧Release栏的链接，或点击[这里](https://github.com/OrdosX/genshin-resolution-tool/releases/latest)下载，双击即可运行

### 从源代码运行

克隆本项目，运行`python dispmgr.py`即可。

若要打包成exe文件，需使用pyinstaller：

```
pip install pyinstaller
pyinstaller dispmgr.spec
```