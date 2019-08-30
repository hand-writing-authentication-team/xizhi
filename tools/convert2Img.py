import os,base64 

img_base64 = os.environ.get("IMG")

imgdata = base64.b64decode(img_base64)
file = open('1.jpg','wb')
file.write(imgdata)
file.close()