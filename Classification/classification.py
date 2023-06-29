from samgeo.text_sam import LangSAM
from PIL import Image
import numpy
import torch
from transformers import ViTForImageClassification, AutoImageProcessor

#CHANGE THESE
x = 1660 #width of image in meters
y = 1107 #height of image in meters
c = 100 #side length of tiles to be segmented in meters
filepathstem = "C:/Users/lukes/Desktop/" #location of this directory
image = Image.open(filepathstem + "Building-Classifier/Classification/Sample Image.jpeg").convert("RGB") #input image, may raise error if too large for PIL
#---

prompt = "building"
model = ViTForImageClassification.from_pretrained(filepathstem + "Building-Classifier/Model/", device_map="auto")
imageprocessor = AutoImageProcessor.from_pretrained("google/vit-base-patch16-224")
model.eval()
sam = LangSAM()

def segmentimage(c, x, y, prompt):
    W, H = image.size
    box = (((x%c)*(W/x))/2, ((y%c)*(H/y))/2, W-((x%c)*(W/x))/2, H-((y%c)*(H/y))/2)
    c1 = image.crop(box)
    W, H = c1.size
    xl = int(x/c)
    yl = int(y/c)
    coordlist = numpy.empty((xl, yl), dtype=object)
    for i in range(xl):
        idx = i
        for i in range(yl):
            idy = i
            box = (idx*(W/xl), idy*(H/yl), (idx+1)*(W/xl), (idy+1)*(H/yl))
            c2 = c1.crop(box)
            a = sam.predict(c2, prompt, box_threshold=0.25, text_threshold=0.25, return_coords=True) #may need to adjust thresholds
            coordlist[idx][idy] = a
    return coordlist #requires change to text_sam.py at the end of predict function (see config.txt)

def processimage(coordlist, c, x, y):
    W, H = image.size
    classificationlist = []
    xc = 0
    while xc < len(coordlist):
        yc = 0
        while yc < len(coordlist[xc]):
            tc = 0
            while tc < len(coordlist[xc][yc]):
                centerxi = ((x%c)*(W/x))/2 + coordlist[xc][yc][tc][0] + xc*c*(W/x)
                centeryi = ((y%c)*(H/y))/2 + coordlist[xc][yc][tc][1] + yc*c*(H/y)
                box = (centerxi - 50*(W/x), centeryi - 50*(H/y), centerxi + 50*(W/x), centeryi + 50*(H/y))
                c1 = image.crop(box)
                input = imageprocessor(c1, return_tensors="pt")
                with torch.no_grad():
                    logits = model(**input).logits
                predicted_label = logits.argmax(-1).item()
                classificationlist.append((centerxi, 
                                           centeryi, 
                                           model.config.id2label[predicted_label]))
                tc += 1
            yc += 1
        xc += 1
    return classificationlist

coordlist = segmentimage(c, x, y, prompt)
print(coordlist)
classificationlist = processimage(coordlist, c, x, y)
print(classificationlist)