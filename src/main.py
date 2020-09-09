import os
import sys
import csv
import time
import pathlib
import argparse
import logging
from tqdm import tqdm

from pytube import YouTube


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
                if os.path.exists(os.path.join(video_dir, f"{row['video_id']}.mp4")):
                    continue

                # download
                try:
                    yt = YouTube(url)
                    yt.streams.filter(progressive=True, file_extension='mp4').first().download(
                        output_path=video_dir,
                        filename=row['video_id'],
                        skip_existing=True
                    )
                except Exception as e:
                    logger.debug(f'{url}: {e}')
