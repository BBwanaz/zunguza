
import random
from PIL import Image
import json
import copy
from operator import mod
import numpy as np


class Process():
    """Class to generate NFTs and Metadata"""

    def __init__(self, config):
        self.config = config
        self.nft_name = config["nft_name"]
        self.size = config["nft_count"]
        self.layers = config["layers"]
        self.description = config["description"]
        self.image_url = config["image_url"]
        self.animation_url = config["animation_url"]
        self.external_url = config["external_url"]
        self.category = config["nft_category"]
        self.layer_attributes_len = []

        for layer, attributes in self.layers.items():
            self.layer_attributes_len.append(len(attributes))

    with open('metadata_template.json') as f:
        _metadata_ = json.load(f)

    def merge_images(self):
        combinations = []    # NFT combinations so far
        nft_count = 0
        not_unique_count = 0

        while nft_count < self.size:
            combination = self.generate_combination()

            if combination not in combinations:
                combinations.append(combination)
                nft_count = nft_count + 1
            else:
                not_unique_count = not_unique_count + 1
                pass
        self.generate_multiple_nfts(combinations)

    def generate_combination(self):
        attr = list(np.random.randint(low = 0,high=max(self.layer_attributes_len),size=len(self.layers)))
        res = list(map(mod, attr, self.layer_attributes_len))
        return res

    def calculate_max(self):
        prod = 1
        for layer, attr in self.layers.items():
            prod = prod * len(attr)

        return prod

    def generate_multiple_nfts(self, combinations):

        layer_keys = list(self.layers.keys())

        for index in range(len(combinations)):
            self.generate_single_nft(layer_keys, combinations[index], index)

    def generate_single_nft(self, layer_keys, combination, nft_number):
        image_paths = []
        nft_name = "{} #{}".format(self.nft_name, str(nft_number))
        metadata_path = 'assets/{}.json'.format(nft_name)
        metadata_temp = copy.deepcopy(self._metadata_)

        for index in range(len(combination)):
            image_path = "layers/" + layer_keys[index] + "/" + layer_keys[index]\
                 + "_{}.png".format(str(combination[index]))
            image_paths.append(image_path)

        images = [Image.open(img_path) for img_path in image_paths]
        background_image = images[0]

        for image in images:
            if image.mode == "RGBA":
                background_image.paste(image, (0, 0), image)
            else:
                background_image.paste(image)

        background_image.save('assets/{}.png'.format(nft_name))

        metadata_temp["name"] = nft_name
        metadata_temp["description"] = self.description
        metadata_temp["image"] = self.image_url
        metadata_temp["animation_url"] = self.animation_url
        metadata_temp["external_url"] = self.external_url
        metadata_temp["category"] = self.category

        for index in range(len(combination)):
            metadata_dict = {
                "trait_type": layer_keys[index],
                "value": self.layers[layer_keys[index]][combination[index]]
            }
            metadata_temp["attributes"].append(metadata_dict)

        with open(metadata_path, "w") as file:
            file.write(json.dumps(metadata_temp, indent=4))
