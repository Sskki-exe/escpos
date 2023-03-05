from escpos.printer import Usb
from PIL import Image, ImageFilter, ImageOps
from flask import Flask, request, render_template
import textwrap

# Variables
maxW = 384

# Define Functions
def printImage(ar,fl):
    print("Printing Image!")
    im = Image.open("out.gif")
    # If don't auto rotate option select
    if ar:
        try:
            print("    Auto Rotating")
            if ars:
                # Rotate Image if Portrait
                if im.width < im.height:
                    print("    Rotating")
                    im = im.rotate(90, expand=True)
            else:
                # Rotate Imafe if Landscape
                if im.width > im.height:
                    print("    Rotating")
                    im = im.rotate(90, expand=True)
        except:
            print("    Failed to rotate")
    if fl:
        try:
            print("    Filtering Color")
            im = im.filter(ImageFilter.EDGE_ENHANCE_MORE).filter(ImageFilter.EDGE_ENHANCE_MORE).filter(ImageFilter.EDGE_ENHANCE_MORE)
            newIm = []
            for px in im.getdata():
                if sum(px[:3]) > 200 and sum(px[:3]) < 300:
                    newIm.append((255,255,255,255))
                else:
                    newIm.append((0,0,0,0))
            mask = Image.new('RGBA', im.size)
            mask.putdata(newIm)
            im.pase(mask, (0,0), mask)
        except:
            print("Failed to filter color")
    # Resize Image if too wide
    if im.width > maxW:
        try:
            print("    Resizing")
            h = int(maxW * im.height / im.width)
            im = im.resize((maxW, h))
        except:
            print("    Failed to resize")
    # Save Image
    im.save('out.gif')
    # Print Image
    if False:
        try:
            im = ImageOps.grayscale(im)
            im.save('static/preview.gif')
            print("    Supressing print")
        except:
            print("    Failed to save preview")
    else:
        try:
            p.text("\n")
            p.image("out.gif",impl=u'bitImageColumn')
            p.text("\n")
        except:
            print("Failed to print")
def printText(line):
    if line == '':
        return
    #line = line.replace('')
    for i in line.split('\n'):
        for ii in textwrap.TextWrapper(width=32).wrap(text=i):
            p.text("\n"+ii)
    p.text("\n")
    print("Text: "+line)

# Printing
p = Usb(0x0456, 0x0808, 0, 0x81, 0x03)
print("Printer Connected!")
p.text("\n")

app = Flask(__name__, template_folder="template")

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cahce"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/', methods=["GET","POST"])
def clickPrint():
    if request.method == "POST":
        print("Print button clicked!")
        printText(request.form.get("text_input"))
        try:
            file = request.files['image_input']
            if file != None:
                print("Saving: "+str(file))
                file.save('out.gif')
                print("saved")
                ar = request.form.get("autoRotate")
                fl = request.form.get("colorFilter")
                printImage(ar,fl)
        except:
            pass
    return render_template('index.html')

if __name__=="__main__":
    app.run(host="0.0.0.0", port=80)
