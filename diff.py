from read_cr2 import *


def save_img_u16(img: np.array, OUTPUT_DIR: str, name: str) -> None:
    img = (img*UINT16_MAX).clip(0,UINT16_MAX).astype(np.uint16) 
    imageio.imsave(os.path.join(OUTPUT_DIR, name+'_diff.tiff'), img)

def save_img_u8(img: np.array, OUTPUT_DIR: str, name: str) -> None:
    img = (img*255).clip(0,255).astype(np.uint8) 
    imageio.imsave(os.path.join(OUTPUT_DIR, name+'_diff.png'), img)


if __name__ == '__main__':
    OUTPUT_DIR = './output'
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    dir = os.path.dirname(args.path)
    file = os.path.basename(args.path)
    name, ext = file.split('.')

    img = read_cr2(args.path)
    ref = read_cr2(os.path.join(dir,name+'_ref.'+ext))

    img = linear_rgb_to_linear_y(img.astype(np.float64)/UINT16_MAX)
    ref = linear_rgb_to_linear_y(ref.astype(np.float64)/UINT16_MAX)
    img = (img-ref).clip(min=0,max=None)

    save_img_u16(img,OUTPUT_DIR,name)

    from matplotlib import cm
    img = (img*1e1).clip(0,1)
    width, height = img.shape[:2]
    cmap = cm.get_cmap('viridis')
    img = cmap(img)
    
    save_img_u8(img, OUTPUT_DIR, name)

    # plt.clf()
    # plt.imshow(img,cmap='viridis')
    # plt.savefig(os.path.join(OUTPUT_DIR, name+'_dff.png'))
