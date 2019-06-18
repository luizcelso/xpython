import click
import requests
import re
from validator_collection import validators, checkers
import os.path

__author__ = "Luiz Celso Pergentino"


@click.group()
def main():
    """
    Python CLI XVideos Downloader. Academic Purposes Only. How to Use: x.py url http... or x.py file file.txt
    """
    pass


@main.command()
@click.argument('u')
def url(u):
    """Download a video of a given URL."""

    if checkers.is_url(u):
        if download(u):
            click.echo('Success!')
        else:
            click.echo('Download error. No fap :(')
    else:
        click.echo('URL error.')


@main.command()
@click.argument('text_file')
def file(text_file):
    """Download videos of a given text file."""

    if os.path.exists(text_file):
        file = open(text_file, 'r')
        for x in file:
            if checkers.is_url(x):
                click.echo('Downloading video from URL: %s' % x)
                if download(x):
                    click.echo('Success!')
                else:
                    click.echo('Download error. No fap :(')
    else:
        click.echo('File does not exist.')


def download(u):
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    }

    response = requests.get(u, headers=headers)
    response_title = re.search(r"(?<=setVideoTitle\(')(.*?)(?=\s*\'\);)", response.text)
    video_title = response_title.group(0) if len(response_title.group(0)) > 0 else 'No Title'
    click.echo('Downloading Video: %s' % video_title)
    video_high_res = re.search(r"(?<=setVideoUrlHigh\(')(.*?)(?=\s*\'\);)", response.text)
    video_low_res = re.search(r"(?<=setVideoUrlLow\(')(.*?)(?=\s*\'\);)", response.text)
    video_file_url = video_high_res.group(0) if len(video_high_res.group(0)) > 0 else video_low_res.group(0)
    download_file = requests.get(video_file_url, allow_redirects=True)
    video_file = video_title.replace(' ', '_')+'.mp4'
    click.echo('Downloading file as: %s' % video_file)
    open(video_file, 'wb').write(download_file.content)
    return True if validators.file_exists(video_file) else False


if __name__ == "__main__":
    main()


