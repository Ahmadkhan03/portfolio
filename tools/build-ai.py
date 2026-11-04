"""Build the AI section's web media from the raw AI/ folder (the AI/ folder itself is not committed).

Images -> media/ai-<id>-<i>.webp (1600px) and media/ai-<id>-<i>-s.webp (640px)
Videos -> ai-reels/<id>.mp4 (max 1280px, web-ready) and media/ai-v-<id>.webp (poster frame)
Writes ai-media.js with the image counts and aspect ratios the page needs.

To add work: pick files in CAMPAIGNS / VIDEOS below, then run from the portfolio root:
    python tools/build-ai.py
"""
import os, json, subprocess
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AI = os.path.join(ROOT, 'AI')
IMG = ('.jpg', '.jpeg', '.png', '.webp', '.jfif')
B2, B20 = 'Creaives Batch 2 October', 'Creaives Batch 20 October'
JUL, FH, LOGOS = 'Creatives New Batch - July 24/Selected Creatives', 'Forever Her', 'Creatives New Batch - July 24/Animated Logos'


def pick(folder, idx):
    """Files in a folder, by their position in name order."""
    fs = sorted(f for f in os.listdir(os.path.join(AI, folder)) if f.lower().endswith(IMG))
    return [f'{folder}/{fs[i]}' for i in idx]


def bac(*names):
    return [f'BACWATER-Static-Ads (For Approval)/{n}' for n in names]


CAMPAIGNS = {
    'fh': pick(f'{FH}/Batch - 1/According to brand guidelines/1.1', [0, 1, 2, 3, 5, 6])
          + pick(f'{FH}/Batch - 1/According to swipe file/1.1', [2, 4, 5, 6, 8, 10, 11, 16])
          + pick('ForeverHer - 26 October/Static', [1, 5])
          + pick(f'{FH}/Toned/PACKAGES/Vial Done', [2]) + pick(f'{FH}/Toned/PACKAGES/Packaging Box (3 Pack)', [1, 2]),
    'apc': pick(f'{B2}/Australian Peptide/Creatives - Spring Themed', [0, 1, 2, 3, 4, 8])
           + pick(f'{B2}/Australian Peptide/Original - Creatives', [1, 2, 8, 11, 12, 6])
           + pick(f'{B20}/APC', [0, 2, 4, 5]),
    'atomix': pick(f'{B2}/Atomix/Autumn/4x5', [0, 1, 2, 3, 4, 5, 6, 9])
              + pick(f'{B2}/Atomix/Original/4x5', [6, 7]) + pick(f'{B20}/Atomix', [3, 5]),
    'brutal': pick(f'{B2}/Brutal/Autumn - Updated/4x5', [0, 1, 2, 3, 4, 5, 8, 9])
              + pick('Creatives New Batch - July 24/Brutal Rx/1.1/Final/1.1', [0, 5, 6]) + pick(f'{B20}/Brutal', [0, 2]),
    'five': [f for b in ['Alyve', 'Atomix', 'CP', 'Elite Labs', 'Quantiv'] for f in pick(f'{JUL}/{b}/1.1', [0, 1, 4, 5])],
    'bac': bac('Angle 1/1A/1A — Variant A.jpg', 'Angle 1/1B/1B — Variant B.jpg', 'Angle 1/1C/1C — Variant A.jpg',
               'Angle 2/2A/2A — Variant A.jpg', 'Angle 2/2B/2B — Variant B.jpg', 'Angle 2/2C/2C — Variant A.jpg',
               'Angle 3/3A/3A — Variant A.jpg', 'Angle 3/3A/3A — Variant B.jpg', 'Angle 3/3B/3B — Variant A - V1.jpg',
               'Angle 3/3B/3B — Variant B - V2.jpg', 'Angle 3/3C/3C — Variant A - V1.jpg', 'Angle 3/3C/3C — Variant B - V2.jpg'),
    'veri': pick(f'{B2}/VeriLeaf', list(range(8))),
    'pop': pick('POP Marketing - 29 October/1x1_1080x1080', list(range(10))),
    'tp': pick('Trade Pilot/TradePilot AI - Youtube Banners and Thumbnails', [1, 4, 0, 3])
          + pick('Trade Pilot/Trade Pilot Bot Images', [0, 1, 2, 3]),
    'sofia': pick('AI Infulencer - Sofia/Sofia in Miami/DP', list(range(20))),
    'products': pick('Selected BioLabs - Product Listing', [0, 2, 5, 7, 10, 12, 14, 16])
                + pick('Pep Vitals', [3, 5])
                + pick(f'{FH}/Toned/PACKAGES/Vial Done', [0, 1]),
    'nutrist': pick('Nutrist/NUTRIST', [0, 2, 3, 5]) + pick('Origano/Origano', [0, 1, 2, 3, 4, 5]),
}

VIDEOS = {
    'fh-math': 'ForeverHer - 26 October/ForeverHer_VideoA_TheMath_1080x1920.mp4',
    'fh-forme': 'ForeverHer - 26 October/ForeverHer_VideoB_IsThisForMe_1080x1920.mp4',
    'fh-nothigh': 'ForeverHer - 26 October/ForeverHer_VideoC_NotHighEnough_1080x1920.mp4',
    'fh-dose': 'ForeverHer - 26 October/ForeverHer_VideoD_DoseGoesUp_1080x1920.mp4',
    'provais-1': 'Provais Product Videos/Refined Product Sample 1 (2).mp4',
    'provais-2': 'Provais Product Videos/Product Sapmple 6.mp4',
    'provais-3': 'Provais Product Videos/Provais_oral_strips_ad_202607232208.mp4',
    'veri-app': f'{B2}/VeriLeaf/FL6 Video.mp4',
    'veri-sketch': f'{B2}/VeriLeaf/FL3 Video.mp4',
    'tp-short-1': 'Trade Pilot/TradePilot Youtube Videos/Shorts/tradepilot-short-01-what-is-copy-trading.mp4',
    'tp-short-3': 'Trade Pilot/TradePilot Youtube Videos/Shorts/tradepilot-short-03-how-to-read-a-trader-profile.mp4',
    'tp-guide': 'Trade Pilot/TradePilot Youtube Videos/Guide/tradepilot-guide-01-what-is-tradepilot.mp4',
    'logo-alyve': f'{LOGOS}/Alyve - 1.mp4',
    'logo-atomix': f'{LOGOS}/Atmoix - 1.mp4',
    'logo-elite': f'{LOGOS}/Elite Labs - 1.mp4',
    'logo-quantiv': f'{LOGOS}/Quantiv Labs - 1.mp4',
    'motion-alyve': f'{LOGOS}/Others/Motion_graphics_for_Meta_ads_202607250257.mp4',
}


def save(im, path, size, q):
    im = im.copy()
    im.thumbnail((size, size), Image.LANCZOS)
    im.save(path, 'WEBP', quality=q, method=6)


def probe(path, entries):
    return subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', entries,
                                    '-of', 'csv=p=0', path], text=True).strip()


def main():
    media, reels = os.path.join(ROOT, 'media'), os.path.join(ROOT, 'ai-reels')
    os.makedirs(reels, exist_ok=True)
    out = {'img': {}, 'vid': {}}
    for cid, files in CAMPAIGNS.items():
        ars = []
        for i, f in enumerate(files, 1):
            im = Image.open(os.path.join(AI, f)).convert('RGB')
            ars.append(round(im.width / im.height, 3))
            save(im, f'{media}/ai-{cid}-{i}.webp', 1600, 82)
            save(im, f'{media}/ai-{cid}-{i}-s.webp', 640, 74)
        out['img'][cid] = {'n': len(files), 'ars': ars}
        print(cid, len(files))
    for vid, f in VIDEOS.items():
        src, dst = os.path.join(AI, f), f'{reels}/{vid}.mp4'
        w, h = map(int, probe(src, 'stream=width,height').split(',')[:2])
        scale = 'scale=trunc(iw/2)*2:trunc(ih/2)*2' if max(w, h) <= 1280 else ('scale=-2:1280' if h >= w else 'scale=1280:-2')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-vf', scale, '-c:v', 'libx264', '-crf', '27',
                        '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '96k', '-movflags', '+faststart',
                        dst], check=True)
        dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                                             '-of', 'csv=p=0', dst], text=True))
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(min(1.5, dur / 3)), '-i', dst, '-frames:v', '1',
                        '-vf', 'scale=-2:720', '-c:v', 'libwebp', '-quality', '78', f'{media}/ai-v-{vid}.webp'], check=True)
        out['vid'][vid] = {'ar': round(w / h, 3), 'dur': round(dur)}
        print(vid, os.path.getsize(dst) // 1024, 'KB')
    with open(os.path.join(ROOT, 'ai-media.js'), 'w', encoding='utf8') as fh:
        fh.write('// generated by tools/build-ai.py: image counts, aspect ratios and video sizes for the AI section\n')
        fh.write('const AI_MEDIA = ' + json.dumps(out, separators=(',', ':')) + ';\n')


if __name__ == '__main__':
    main()
