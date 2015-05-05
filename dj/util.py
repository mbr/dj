import click
import requests


def progress_download_url(url, out, label=None):
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    return progress_download(resp, out, label)


def progress_download(resp, out, label=None):
    with click.progressbar(length=int(resp.headers.get('content-length', 0)),
                           label=label,
                           bar_template='%(label)s [:%(bar)s:] %(info)s',
                           fill_char=unichr(0x2669),
                           empty_char='.') as bar:
        for chunk in resp.iter_content(4096):
            out.write(chunk)
            bar.update(len(chunk))
