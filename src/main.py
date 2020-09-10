import os
import sys
import csv
import time
import pathlib
import argparse
import logging
from tqdm import tqdm

import youtube_dl


# setting for argparse
parser = argparse.ArgumentParser(description='Analysis an image showing company structure')
parser.add_argument('--dataset_dir', type=str, default='/data', help='the directory path where the countix csv files and outputs are')
parser.add_argument('--logging', action='store_true', default=False, help='if true, output the all image/pdf files during the process')

args = parser.parse_args()
log_dir = '/logs/{}'.format(time.strftime("%Y%m%d-%H%M%S"))

# setting for logging
if args.logging:
    log_fpath = os.path.join(log_dir, 'logger.log')
    os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(
        filename=log_fpath,
        level=logging.DEBUG
    )
logger = logging.getLogger(__name__)

_console_handler = logging.StreamHandler(sys.stdout)
_console_handler.setLevel(logging.DEBUG)
logger.addHandler(_console_handler)


def download_video_from_url(
    url_to_video: str,
    path_to_video: str,
    skip_existing_videos: bool = True
) -> str:
    # This function is copied from https://colab.research.google.com/github/google-research/google-research/blob/master/repnet/repnet_colab.ipynb

    if os.path.exists(path_to_video):
        if skip_existing_videos:
            return 'skipped'
        else:
            os.remove(path_to_video)
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'outtmpl': str(path_to_video),
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url_to_video])
        return 'success'


if __name__ == "__main__":
    data_dir = pathlib.Path(args.dataset_dir).resolve()
    video_dir = os.path.join(data_dir, 'downloaded_videos')
    csv_file_names = [
        'countix_train.csv',
        'countix_val.csv',
        'countix_test.csv'
    ]

    logger.info(f'command line arguments: {args}')

    for csv_file_name in csv_file_names:
        logger.info(f'load {csv_file_name}')

        with open(os.path.join(data_dir, csv_file_name)) as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                url = 'http://youtube.com/watch?v={}'.format(row['video_id'])
                logger.debug(url)

                # check if the video was already downloaded
                video_fpath = os.path.join(video_dir, f"{row['video_id']}.mp4")
                if os.path.exists(video_fpath):
                    continue

                # download
                r = download_video_from_url(
                    url_to_video=url,
                    path_to_video=video_fpath
                )

