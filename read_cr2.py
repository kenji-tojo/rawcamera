import rawpy
import imageio
import os
import numpy as np
import cv2


UINT16_MAX = np.iinfo(np.uint16).max


def linear_rgb_to_linear_y(img_rgb: np.ndarray) -> np.ndarray:
    assert img_rgb.ndim == 3 and img_rgb.shape[2] == 3
    return .2126 * img_rgb[:,:,0] + .7152 * img_rgb[:,:,1] + .0722 * img_rgb[:,:,2]


def read_cr2(path: str) -> np.ndarray:
    raw = rawpy.imread(path)
    rgb = raw.postprocess(gamma=(1,1), no_auto_bright=True, output_bps=16)
    return np.array(rgb, dtype=np.uint16)


if __name__ == '__main__':
    OUTPUT_DIR = './output'
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    rgb = read_cr2('./data/cup.CR2')
    rgb = rgb.astype(np.float64) / UINT16_MAX

    luminosity = linear_rgb_to_linear_y(rgb)
    luminosity = (luminosity*UINT16_MAX).clip(0,UINT16_MAX).astype(np.uint16)

    imageio.imsave(os.path.join(OUTPUT_DIR, 'cup_luminosity.tiff'), luminosity)
