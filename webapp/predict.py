# %%
import torch
import numpy as np
import cv2
from detection import utils
from torchvision.transforms import functional as F
import imutils

model = torch.load('./saved_model_1.pt', map_location='cpu')
model.eval()

CLASSES = [
    '_______',          # 0
    'APPLE',            # 1
    'BEAN',             # 2
    'BOILED EGG',       # 3
    'CHICKEN BREST',    # 4
    'RICE',             # 5
    'SALAD',            # 6
    'SPAGHETTI',        # 7
    'FRIED EGG',        # 8
    'STEAK',            # 9
]

COLORS = [
    (0, 0, 255),
    (0, 255, 0),
    (255, 0, 0),
    (255, 255, 0),
    (0, 255, 255),
    (255, 0, 255),
    (127, 255, 127),
    (255, 127, 127),
    (127, 127, 255),
]

IOU_THR = 0.4
PRED_THR = 0.6
MASK_THR = 0.8
PREDICT_IMG_SIZE = 512


def decode_results(img, prediction):
    ixs = utils.batched_nms(prediction[0]['boxes'], prediction[0]['scores'], prediction[0]['labels'], IOU_THR)
    prediction[0]['boxes'] = prediction[0]['boxes'][ixs]
    prediction[0]['scores'] = prediction[0]['scores'][ixs]
    prediction[0]['masks'] = prediction[0]['masks'][ixs]
    prediction[0]['labels'] = prediction[0]['labels'][ixs]

    main = np.copy(img)
    idx = np.where(prediction[0]['scores'] >= PRED_THR)[0]
    scores = prediction[0]['scores'][idx]
    label_idx = prediction[0]['labels'][idx]
    masks = prediction[0]['masks'][idx, 0].numpy()
    masks[masks >= MASK_THR] = 1
    masks[masks < MASK_THR] = 0

    results = []
    total_pixels = 0
    mask_dict = {}
    for i, l in enumerate(label_idx):
        try:
            mask_dict[l.item()] += masks[i]
        except:
            mask_dict[l.item()] = masks[i]
        mask_dict[l.item()] = np.clip(mask_dict[l.item()], 0, 1)

    for j, (k, mask) in enumerate(mask_dict.items()):
        s_idx = np.where(prediction[0]['labels'] == k)[0]
        score = np.max(prediction[0]['scores'][s_idx].numpy())
        label = CLASSES[k]
        seg = (np.copy(mask) * 255).astype(np.uint8)
        contours, _ = cv2.findContours(seg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        pixels = mask.sum()
        total_pixels += pixels

        results.append([label, f'{score:.2f}', pixels, COLORS[j % 9]])

        for c in contours:
            mask2 = np.zeros(seg.shape, np.uint8)
            out = cv2.drawContours(mask2, c, -1, 255, -1)
            mean, _, _, _ = cv2.mean(seg, mask=mask2)
            color = COLORS[j % 9]
            cv2.drawContours(main, [c], -1, color, 5)

    for r in results:
        r[2] = int(r[2] / total_pixels * 100)

    return main, results


def prepare_image(img_path):
    im = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)
    idx = np.argmax(im.size)
    maior = np.max(im.size)
    if maior > PREDICT_IMG_SIZE:
        if idx == 0:
            im = imutils.resize(im, width=PREDICT_IMG_SIZE)
        else:
            im = imutils.resize(im, height=PREDICT_IMG_SIZE)
        cv2.imwrite(img_path, im)
    img_tensor = F.to_tensor(im)
    return img_tensor, im
