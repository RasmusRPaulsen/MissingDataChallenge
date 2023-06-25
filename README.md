# Missing Data Challenge - with cats 2023

The goal of this challenge is to develop and evaluate algorithms for image inpainting. In this challenge, inpainting is the process of filling in missing parts of an image, where we already know which part that needs to be filled.

In the example below, there is an **original** image that has been *masked* with a **stroke mask** resulting in a **stroke masked** image. The goal is to predict the missing values in the **stroke masked** image, given the mask and the stroked masked image. A simple try on inpainting is shown to the right.

|                 Original                 |                 Stroke Masked                 |                 Stroke Mask                 |                 Inpainted                 |
|:----------------------------------------:|:---------------------------------------------:|:-------------------------------------------:|:-----------------------------------------:|
| <img src="figs/original.jpg" width=200/> | <img src="figs/stroke_masked.png" width=200/> | <img src="figs/stroke_mask.png" width=200/> | <img src="figs/inpainted.png" width=200/> |

## Data

The data consist of aligned cat faces stored as RGB images of size 360 x 360 pixels. The data can be downloaded here: TBD.

The folder structure:
- **originals** : The original images (only for the training set)
- **masks** : The masks for all images
- **masked** : The masked images
- **data_splits** : Text files with file ids in the different sets.

The data has been divided into several sets:
- **training** : More than 5000 images with both original and masked images
- **validation** : Images with only the masked image available. Will be used during the challenge to evaluate challenge teams on the score board.
- **test** : Images with only the masked image avalaible. Will be evaluated once and be used for the final team score.

## Supplied Python scripts

All the supplied scripts take two arguments, the config file and the dataset to use. For example:

```
train_inpainter.py -c rasmus_pc_config.json -d validation_200
```

Will use the configuration settings in `rasmus_pc_config.json` and train on the `validation_200` set.

The following scripts, should be seen as simple templates that you can use as a basis for your own inpainting framework:

- `train_inpainter.py`: will compute an average image that can be used to fill out masks in when inpainting.
- `inpaint_images.py`: will compute inpainted images in the given set using an average image, to estimate the missing values.
- `evaluate_inpaintings.py`: will compute similarity metrics (MSE, PSNR, SSIM, etc) between the original image and the inpainted image. Will only work for the sets where you have the original image (training.)
- `submit_inpaintings.py`: Zip a given folder with inpainted images. This zip file can be uploaded to the challenge server: TBD.

## Getting started

- Download the data and unpack it a suitable place.
- Clone this repository or download it as a zip and unpack.
- Create a copy of `my_inpaint_config.json` or edit it directly.
- Find a fantastic team name (only using letters and numbers) and put it into the config file.
- Change the data folders in the config file to match your local setup.
- Try to run `train_inpainter.py` with the **training** set.
- Try to run `inpaint_image.py` with the **training** set.
- Try to run `evaluate_inpaintings.py` with the **training** set.
- Try to run `inpaint_image.py` with the **validation_200** set.
- Try to run `submit_inpaintings.py` with the **validation_200** set.
- Upload the generated zip file to the challenge server: TBD

We encourge you to split the **training** set into smaller sets for your own purpose (training, validation etc).

**DO NOT** change the image ids in the provided validation and test sets. They should be fixed by all teams.

## Evaluation of inpaintings

## The challenge server and the score board

## Bad Cats!
If you find images that do not contain a cat face or where the cat face is partial or distorted, then report it to Rasmus.

# References

- https://github.com/affromero/NTIRE22_Inpainting
