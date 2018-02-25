
import json
import os.path

from base64 import b64encode, b64decode


def saveLabels(self, filename):
    lf = LabelFile()

    def format_shape(s):
        return dict(label=unicode(s.label),
                    line_color=s.line_color.getRgb() \
                        if s.line_color != self.lineColor else None,
                    fill_color=s.fill_color.getRgb() \
                        if s.fill_color != self.fillColor else None,
                    points=[(p.x(), p.y()) for p in s.points])

    shapes = [format_shape(shape) for shape in self.canvas.shapes]

    contours_txt = open("shapes.txt", 'w')
    contours_txt.write(str(shapes))
    contours_txt.close()

    try:  ### TODO: save labels
        # lf.save(filename, shapes, unicode(self.filename), self.imageData,
        #     self.lineColor.getRgb(), self.fillColor.getRgb())
        lf.save(filename, shapes, unicode(self.filename), '',
                self.lineColor.getRgb(), self.fillColor.getRgb())
        self.labelFile = lf
        self.filename = filename
        return True
    except LabelFileError, e:
        self.errorMessage(u'Error saving label data',
                          u'<b>%s</b>' % e)
        return False



class LabelFile(object):  # save format as '.lif'
    suffix = '.lif'

    def __init__(self, filename=None):
        self.shapes = ()
        self.imagePath = None
        self.imageData = None
        if filename is not None:
            self.load(filename)

    def load(self, filename):
        try:
            with open(filename, 'rb') as f:
                data = json.load(f)
                imagePath = data['imagePath']
                imageData = b64decode(data['imageData'])
                lineColor = data['lineColor']
                fillColor = data['fillColor']
                shapes = ((s['label'], s['points'], s['line_color'], s['fill_color'])\
                        for s in data['shapes'])
                # Only replace data after everything is loaded.
                self.shapes = shapes
                self.imagePath = imagePath
                self.imageData = imageData
                self.lineColor = lineColor
                self.fillColor = fillColor
        except Exception, e:
            raise LabelFileError(e)

    def save(self, filename, shapes, imagePath, imageData,
            lineColor=None, fillColor=None):
        try:
            with open(filename, 'wb') as f:
                json.dump(dict(
                    shapes=shapes,
                    lineColor=lineColor, fillColor=fillColor,
                    imagePath=imagePath,
                    imageData=b64encode(imageData)),
                    f, ensure_ascii=True, indent=2)
        except Exception, e:
            raise LabelFileError(e)

class LabelFileError(Exception):
    pass

class writeEdgeLif():

    # TODO:
    # 1. 写一个在当前图像新建画布的函数。
    # 2. 写一个处理点的函数
    # 3. 写一个把点读入到画布上的函数。
    # 4. 写一个显示点的函数。
    def creatCanvas(self):
        return 0

    def dealPoints(self):
        return 0

    def paintPoints(self):
        return 0

