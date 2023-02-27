from PIL import Image
import numpy as np

import os

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='path to the image directory')
    parser.add_argument('-r', '--interp_res', type=int, default=4, help='number of frames between each reference frames')
    args = parser.parse_args()

    dir = args.dir
    out_dir = os.path.join(dir, 'out')
    os.makedirs(out_dir, exist_ok=True)

    imgs = []

    for fname in os.listdir(dir):
        if len(fname.split('.')) != 2:
            continue

        id, ext = fname.split('.')

        if len(id) != 2 or ext != 'png':
            continue

        imgs.append({
            'id': int(id),
            'path': os.path.join(dir, fname)
        })
    
    imgs.sort(key=lambda x: x['id'])

    interp_res = args.interp_res

    for i in range(len(imgs)):
        imgs[i]['id'] = i*(interp_res+1) + imgs[0]['id']

    n = imgs[0]['id']
    path = imgs[0]['path']
    im1 = np.array(Image.open(path))/255.
    im1 = im1[:,:,:3]

    for e in imgs[1:]:
        path = e['path']
        im2 = np.array(Image.open(path))/255.
        im2 = im2[:,:,:3]

        for id in range(interp_res+1):
            d = id/(interp_res+1)
            im = (1.-d)*im1 + d*im2
            im = Image.fromarray(np.round(im*255.).clip(0.,255.).astype(np.uint8))
            im.save(os.path.join(out_dir, f'{n+id:02d}.png'))
        
        n = e['id']
        im1 = im2

    im = im1
    id = 0
    im = Image.fromarray(np.round(im*255.).clip(0.,255.).astype(np.uint8))
    im.save(os.path.join(out_dir, f'{n+id:02d}.png'))

    framerate = 30
    os.system(f'ffmpeg -framerate {framerate} -i {out_dir}/%02d.png {out_dir}/video.mp4')
