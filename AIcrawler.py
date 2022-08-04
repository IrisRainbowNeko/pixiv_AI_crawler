import os.path

from torchvision import transforms, models
import torch
from timm.models import create_model
from torch import nn
from PIL import Image
from pathlib import Path
from tqdm import tqdm
from shutil import copyfile
from datasets import build_transform
import argparse
import utils

import models.convnext
import models.convnext_isotropic

from pixiv_crawler import config
from pixiv_crawler.config import DOWNLOAD_CONFIG
from pixiv_crawler.crawlers.ranking_crawler import RankingCrawler
from pixiv_crawler.crawlers.keyword_crawler import KeywordCrawler

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
cls_names=['其他', '高质量涩图', '百合']

def str2bool(v):
    """
    Converts string to bool type; enables command line
    arguments in the format of '--arg1 true --arg2 false'
    """
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def get_args_parser():
    parser = argparse.ArgumentParser('ConvNeXt training and evaluation script for image classification', add_help=False)

    # Model parameters
    parser.add_argument('--model', default='convnext_tiny', type=str, metavar='MODEL',
                        help='Name of model to train')
    parser.add_argument('--drop_path', type=float, default=0, metavar='PCT',
                        help='Drop path rate (default: 0.0)')
    parser.add_argument('--input_size', default=384, type=int,
                        help='image input size')

    # Evaluation parameters
    parser.add_argument('--crop_pct', type=float, default=None)
    parser.add_argument('--pos_thr', type=list, default=[2.0, 0.823, 0.5])

    # Dataset parameters
    parser.add_argument('--nb_classes', default=1000, type=int,
                        help='number of the classification types')
    parser.add_argument('--imagenet_default_mean_and_std', type=str2bool, default=True)

    parser.add_argument('--ckpt', default='ckpt/checkpoint-best_t4.pth', help='resume from checkpoint')

    # Crawlers
    parser.add_argument('--capacity', default=1024*8, type=int, help='crawler capacity')
    parser.add_argument('--keyword', default=None, type=str, help='for keyword crawler')
    parser.add_argument('--n_images', default=500, type=int, help='for keyword crawler')

    return parser

@torch.no_grad()
def run_crawler(args):

    transform = build_transform(False, args)

    net = create_model(
        args.model,
        pretrained=False,
        num_classes=args.nb_classes,
        drop_path_rate=args.drop_path,
        )
    #net.load_state_dict(torch.load(args.ckpt)['model'])
    utils.load_state_dict(net, torch.load(args.ckpt), prefix='')
    net = net.to(device)
    net.eval()

    to_pil=transforms.ToPILImage()

    def im_classifier(img):
        pimg = to_pil(img)
        pimg.save('test.jpg')
        0/0
        img = transform(pimg).to(device).unsqueeze(0)

        pred = net(img)
        cls = pred.view(-1).argmax().item()

        conf = torch.softmax(pred, dim=-1)[0, cls]
        if conf < args.pos_thr[cls]:
            return None
        else:
            return cls_names[cls]

    if args.keyword is None:
        config.MODE_CONFIG['N_ARTWORK']=args.n_images
        crawler=RankingCrawler(capacity=args.capacity, im_classifier=im_classifier)
    else:
        crawler=KeywordCrawler(keyword=args.keyword, n_images=args.n_images, capacity=args.capacity, im_classifier=im_classifier)

    crawler.run()

if __name__ == '__main__':
    parser = argparse.ArgumentParser('ConvNeXt pixiv AI crawler', parents=[get_args_parser()])
    args = parser.parse_args()

    for name in cls_names:
        os.makedirs(os.path.join(DOWNLOAD_CONFIG["STORE_PATH"], name), exist_ok=True)

    run_crawler(args)
