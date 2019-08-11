from PIL import ImageDraw, ImageFont, Image

import shapes
import utils


def render(img, obj):
    draw = ImageDraw.Draw(img)

    if obj.type == 'rectangle':
        draw.rectangle((obj.top_left, obj.bottom_right))

    elif obj.type == 'text':
        draw.text(obj.position, obj.text, font=ImageFont.truetype(obj.font))

    elif obj.type == 'line':
        draw.line(obj.start + obj.end)

    elif obj.type == 'arc':
        x0, y0 = utils.add_points(obj.center, (-obj.radius, -obj.radius))
        x1, y1 = utils.add_points(obj.center, (obj.radius, obj.radius))
        start = utils.rad_to_deg(-obj.end)
        end = utils.rad_to_deg(-obj.start)
        draw.arc((x0, y0, x1, y1), start, end)

    else:
        [render(img, x) for x in obj.primitives]


def main():
    font = 'Ubuntu-R'
    image_size = (500, 500)
    img = Image.new('RGB', image_size)

    rectangle = shapes.Rectangle((0, 0), (100, 100))
    text = shapes.Text('bibek', (50, 50), font)
    arc = shapes.Arc((300, 20), 50, 0, -3.14/3)

    textrect = shapes.TextInRectangle('Pandey', font, (100, 100), padding=20)
    roundedrect = shapes.RoundedRectangle((150, 150), (300, 340), 10)

    render(img, rectangle)
    render(img, text)
    render(img, arc)
    render(img, textrect)
    render(img, roundedrect)

    img.save('text.png')


if __name__ == '__main__':
    main()