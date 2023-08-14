# Missing Data Challenge - Paint the Cat!

This challenge is made in conjunction with the [Ph. D. summer school on missing data](https://missing-data.compute.dtu.dk/). The Ph. D. summer school specific information can be found [here](info/InPaint-the-cat-challenge-2023.pdf).

The goal of this challenge is to develop and evaluate algorithms for image inpainting. In this challenge, inpainting is the process of filling in missing parts of an image, where we already know which part that needs to be filled.

In the example below, there is an **original** image that has been *masked* with a **stroke mask** resulting in a **stroke masked** image. The goal is to predict the missing values in the **stroke masked** image, given the mask and the stroked masked image. A simple try on inpainting is shown to the right.

|                 Original                 |                 Stroke Masked                 |                 Stroke Mask                 |                 Inpainted                 |
|:----------------------------------------:|:---------------------------------------------:|:-------------------------------------------:|:-----------------------------------------:|
| <img src="figs/original.jpg" width=200/> | <img src="figs/stroke_masked.png" width=200/> | <img src="figs/stroke_mask.png" width=200/> | <img src="figs/inpainted.png" width=200/> |

## Data

The data consist of aligned cat faces stored as RGB images of size 360 x 360 pixels. The data can be downloaded [here](https://people.compute.dtu.dk/rapa/cats/MissingDataOpenData.zip).

The folder structure:
- **originals** : The original images (only for the training and validation sets)
- **masks** : The masks for all images
- **masked** : The masked images
- **data_splits** : Text files with file ids in the different sets.

The data has been divided into several sets:
- **training**: More than 4900 images with both original and masked images.
- **validation**: Images with both the original and masked images available. Can be used by the teams to run a classic train/validation setup.
- **test**: Images with only the masked image available. Will be used during the challenge to evaluate the challenge teams on the score board.
- **final_test**: Images with only the masked image available. Will be used to compute the final ranking of the teams.

For the validation, test and final_test sets there are several subsets. **validation_200** contains, for example, 200 images. All the image in **validation_200** are also in **validation_500** and so on.

## Dependencies
The code is tested with python 3.8.10 and 3.11.3 and requires installation of the following packages scikit-image, tqdm and requests. You can install the dependencies using pip:
```
pip install -r requirements.txt
```

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
- `submit_inpaintings.py`: Zip a given folder with inpainted images and uploads the inpainted images to the challenge server.

## Getting started

- Download the data [here](https://people.compute.dtu.dk/rapa/cats/MissingDataOpenData.zip) and unpack it a suitable place.
- Clone this repository or download it as a zip and unpack.
- Create a copy of `my_inpaint_config.json` or edit it directly.
- Find a fantastic team name (only using letters and numbers) and put it into the config file.
- Change the data folders in the config file to match your local setup.
- Try to run `train_inpainter.py` with the **training** set.
- Try to run `inpaint_image.py` with the **validation_200** set.
- Try to run `evaluate_inpaintings.py` with the **validation_200** set.
- Try to run `inpaint_image.py` with the **test_200** set.
- Try to run `submit_inpaintings.py` with the **test_200** set.

We encourage you to split the **training**  set into smaller sets for your own purpose (training, validation etc).

**DO NOT** change the image ids in the provided validation, test and final_test sets. They should be fixed by all teams.

## Describing your method in the config file

The JSON config file has a field called `method`. Here you should supply a simple description of your method with no special letters. For example `MeanImageInpaint`, `PCAInpaint`, `MostSimilarInpaint`. This is used on the scoreboard.

## Evaluation of inpaintings

The quality of the inpaintings are evaluated by comparing the original (full) image and the inpainted image:

|                 Original                 |Inpainted                 |
|:----------------------------------------:|:---------------------------------------------:|
| <img src="figs/original.jpg" width=200/> | <img src="figs/inpainted.png" width=200/> |

The images are compared using the following metrics:
- [Mean Squared Error (MSE)](https://scikit-image.org/docs/stable/api/skimage.metrics.html#skimage.metrics.mean_squared_error)
- [Peak signal to noise ratio (PSNR)](https://scikit-image.org/docs/stable/api/skimage.metrics.html#skimage.metrics.peak_signal_noise_ratio)
- [Mean structural similarity index (MSSIM)](https://scikit-image.org/docs/stable/api/skimage.metrics.html#skimage.metrics.structural_similarity)

You can compute these metric using the `evaluate_inpaintings.py` by using a set where you have the original (all the images in the training set).

## The challenge server and the score board

When you submit your inpainted images to the challenge server using `submit_inpaintings.py`, the server will unpack your images and compare them with the original images. A score board is computed that can be seen here: http://fungi.compute.dtu.dk:8080

Start by submitting results from the **test_200** set.

## Inspiration

Inpainting has a long history and there are many ways to approach it. Here are some pointers:

- Inpaint using an average image.
- Inpaint by replacing a masked pixel with the value of the Euclidean closest pixel in the image.
- Inpaint by finding the most similar image in the training set based on the non-masked pixels. Copy the pixels from the similar image to the masked part.
- Build a [generative model using principal component analysis PCA](https://github.com/RasmusRPaulsen/DTUImageAnalysis/tree/main/exercises/ex8-CatsCatsCats) and fit the model to the visible pixels and by then predicting the masked pixels.
- [Inpaint masked points in image with biharmonic equations](https://scikit-image.org/docs/stable/api/skimage.restoration.html#skimage.restoration.inpaint_biharmonic)
- [Inpaint using the fast marching method](https://github.com/olvb/pyheal)
- [Inpaint using the Navier-Stokes equations](https://docs.opencv.org/3.4/df/d3d/tutorial_py_inpainting.html)
- Using [auto encoders](https://towardsdatascience.com/inpainting-with-ai-get-back-your-images-pytorch-a68f689128e5), [more auto encoders](https://wandb.ai/ayush-thakur/image-impainting/reports/An-Introduction-to-Image-Inpainting-Using-Deep-Learning--Vmlldzo3NDU0Nw)


*Please do try at least one non-deep learning based method before going to deep learning based methods.*

## Bad Cats!
If you find images that do not contain a cat face or where the cat face is partial or distorted, then report it to Rasmus.

# Similar competitions
- https://github.com/affromero/NTIRE22_Inpainting

