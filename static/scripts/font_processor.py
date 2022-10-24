from PIL import ImageFont, Image, ImageDraw
from io import BytesIO
import ddddocr
from fontTools.ttLib import TTFont
from fontTools.ttLib.woff2 import decompress

def processor():
    # 加载字体文件：
    font = TTFont('woff/cb3159c2.woff')

    # 保存为xml文件：
    font.saveXML('cb3159c2.xml')
    print(font.keys())

    # 获取getGlyphOrder节点的name值，返回为列表
    print(font.getGlyphOrder())
    print(font.getGlyphNames())


    # 获取cmap节点code与name值映射, 返回为字典
    print(font.getBestCmap())

    # 获取glyf节点TTGlyph字体xy坐标信息
    print(font['glyf']['unie003'].coordinates)

    # 获取glyf节点TTGlyph字体xMin,yMin,xMax,yMax坐标信息
    print(font['glyf']['unie003'].xMin, font['glyf']['unie003'].yMin,
          font['glyf']['unie003'].xMax, font['glyf']['unie003'].yMax)


    # 获取glyf节点TTGlyph字体on信息
    print(font['glyf']['unie003'].flags)  # array('B', [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0])

    # 获取GlyphOrder节点GlyphID的id信息, 返回int型
    print(font.getGlyphID('unie003'))  # 237



def font_to_img(_code, filename):
    """将字体画成图片"""
    img_size = 1024
    img = Image.new('1', (img_size, img_size), 255)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(filename, int(img_size * 0.7))
    txt = chr(_code)
    x, y = draw.textsize(txt, font=font)
    draw.text(((img_size - x) // 2, (img_size - y) // 2), txt, font=font, fill=0)
    return img


def identify_word(_ttf_path):
    """识别ttf字体结果"""
    font = TTFont(_ttf_path)
    ocr = ddddocr.DdddOcr()
    for cmap_code, glyph_name in font.getBestCmap().items():
        bytes_io = BytesIO()
        pil = font_to_img(cmap_code, _ttf_path)
        pil.save(bytes_io, format="PNG")
        word = ocr.classification(bytes_io.getvalue())  # 识别字体
        print(cmap_code, glyph_name, word)
        # with open(f"./img/{cmap_code}_{glyph_name}.png", "wb") as f:
        #     f.write(bytes_io.getvalue())

woff2_path = "./woff/cb3159c2.woff"
ttf_path = './woff/cb3159c2.ttf'
xml_path = './woff/cb3159c2.xml'
decompress(woff2_path, ttf_path)  # 将woff2文件转成ttf文件
_font = TTFont(ttf_path)
_font.saveXML(xml_path)
identify_word(ttf_path)