import json
from process import Process
import os


# Import Config
with open('config.json') as f:
    config = json.load(f)

img_processor = Process(config)

max_nft_size = img_processor.calculate_max()

if max_nft_size >= config["nft_count"]:
    print("Processing.....")
    current_dir = os.getcwd()
    try:
        os.mkdir(current_dir + "/assets")
    except FileExistsError:
        print("Assets directory already exists")

    img_processor.merge_images()
else:
    print("Not enough variations to get as many NFTs.\
    Only {} NFTs can be generated atm".format(str(max_nft_size)))
