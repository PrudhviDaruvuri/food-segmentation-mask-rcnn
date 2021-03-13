# Food Detection and Segmentation using Mask-RCNN

This repository implements a new project I am starting now, where the goal is to identify the kinds of foods inside a dish.
<img src=img/img1.jpg>
<hr>
<img src=img/img2.jpg>

## Tools
- [Mask-RCNN]() implementation with pre-trained weigths available at [PyTorch Vision Models](https://pytorch.org/vision/stable/models.html#object-detection-instance-segmentation-and-person-keypoint-detection).
- [MyFood Dataset](https://zenodo.org/record/4041488#.YEzSwy2708Z) with 1250 pictures anotated in 9 kinds of food (rice, beans, boiled egg, fried egg, pasta, salad, roasted meat, apple, and chicken breast)
- [FastAPI](https://fastapi.tiangolo.com): to build a web application to try the fine tuned model.


# Install
1. Clone this repository
```bash
git clone https://github.com/renatoviolin/food-segmentation-mask-rcnn.git
cd food-segmentation-mask-rcnn
```

2. Train you model using this [notebook](train.ipynb). Make sure to download the dataset and adjust the paths inside the it. At end, it will be generated the fine tuned weights named 'saved_model.pt'. Copy this file in the root directory 'food-segmentation-mask-rcnn'.


3. Create the container with the command:
```bash
docker-compose build
```

4. Run 
```bash
docker-compose up
```

5. Open the demo webapp.
http://localhost:8000/
<img src=img/demo.gif>


## To-do
- use other dataset to increase the kinds of food.
- improve accuracy of detection and segmentation.
- try another models (Deeplab-V3, FCN)

# Credits
- [Mask-RCNN](https://arxiv.org/pdf/1703.06870.pdf)
- [Torchvision Object Detection Finetuning Tutorial](https://pytorch.org/tutorials/intermediate/torchvision_tutorial.html)
- [MyFood: A Food Segmentation and Classification System to Aid Nutritional Monitoring](https://arxiv.org/pdf/2012.03087v1.pdf)
- [FastAPI](https://fastapi.tiangolo.com)