#Autolabelme-2017a说明  
11/8/2017 7:17:42 AM   
DO:  
labelme软件自动标注功能的稳定版本：  
目前实现功能如下：  
1. 自动保存标记的lif文件。（原来需要命名以及制定位置）  
2. 文件标记过程中的跳转等功能的优化，便于操作。（文件按规定格式命名，+1跳转到下一张）  
3. 文件快捷键的设置，很多改为单键操作。  
4. 文件根据FCN检测结果（缺陷区域）实现自动标记并保存为lif文件。（可以手动修正自动标记结果）  
5. 

TODO:  
后期预计增加或者修改的功能：  
1. 一键生成VOC格式的数据集。   
2. 标记结果的handwrite功能，显示生成的标记在原图中画出来。  
3. 与深度学习算法或者传统算法结合，在label软件中调用模型或者算法处理生成缺陷区域图，与edgepoint.py对接。（优先考虑传统算法，速度快）  


---------------------------------------------------------------------------

# Labelme

Labelme is a graphical image annotation tool inspired by
http://labelme.csail.mit.edu.

It is written in Python and uses Qt for its graphical interface.

# Dependencies

Labelme requires at least [Python 2.6](http://www.python.org/getit/) and
has been tested with [PyQt
4.8](http://www.riverbankcomputing.co.uk/software/pyqt/intro).

# Usage

After cloning the code you should first run `make` to generate the
resource file (a Python module containing all the icons).

You can then start annotating by running `./labelme.py`. For usage
instructions you can view the screencast tutorial from the `Help` menu.

At the moment annotations are saved as a [JSON](http://www.json.org/) file.
The file includes the image itself. In the feature support for XML
output or possibly even [SVG](http://www.w3.org/Graphics/SVG/) will be added.

# TODO

- Refactor into a Python package.
- Add installation script.

