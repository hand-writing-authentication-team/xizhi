import os,base64 

img_file = os.environ.get("IMG_FILE")

with open(img_file,"rb") as f:
    base64_data = base64.b64encode(f.read())
    print(base64_data)
