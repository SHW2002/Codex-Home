"""Split transparent UI sheets without rescaling or losing frame registration.

Requires Pillow. Run with --help; never makes image-generation API calls.
"""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw


def bounds_union(boxes):
    return (min(b[0] for b in boxes), min(b[1] for b in boxes),
            max(b[2] for b in boxes), max(b[3] for b in boxes))


def collect_frames(source, columns, rows, names):
    width, height = source.size
    slot_size = ((width + columns - 1) // columns, (height + rows - 1) // rows)
    frames = []
    for index, name in enumerate(names):
        if name == '-':
            continue
        col, row = index % columns, index // columns
        rect = (col * width // columns, row * height // rows,
                (col + 1) * width // columns, (row + 1) * height // rows)
        cell = source.crop(rect)
        if cell.getchannel('A').getextrema()[0] != 0:
            raise ValueError(f'{name}: cell has no fully transparent pixels; inspect its background')
        frame = Image.new('RGBA', slot_size)
        frame.paste(cell, (0, 0))  # No mask: preserve alpha instead of multiplying it twice.
        bbox = frame.getchannel('A').getbbox()
        if bbox is None:
            raise ValueError(f'{name}: named cell is completely transparent')
        frames.append((name, frame, rect, bbox))
    return frames, slot_size


def make_preview(exports, size):
    columns = min(5, len(exports))
    tile_width, tile_height = size + 24, size * 2 + 60
    rows = (len(exports) + columns - 1) // columns
    preview = Image.new('RGB', (columns * tile_width, rows * tile_height), '#989898')
    draw = ImageDraw.Draw(preview)
    for index, (_, frame) in enumerate(exports):
        x, y = index % columns * tile_width, index // columns * tile_height
        thumb = frame.copy()
        thumb.thumbnail((size, size), Image.Resampling.LANCZOS)
        for variant, color in enumerate(('#eee8da', '#252831')):
            top = y + 20 + variant * (size + 20)
            plate = Image.new('RGBA', (size, size), color)
            plate.alpha_composite(thumb, ((size - thumb.width) // 2, (size - thumb.height) // 2))
            preview.paste(plate.convert('RGB'), (x + 12, top))
        draw.text((x + 12, y + 4), str(index + 1), fill='black')
    return preview


def export_sheet(args):
    with Image.open(args.input) as image:
        source = image.convert('RGBA')
    if args.columns > source.width or args.rows > source.height:
        raise ValueError('Grid cells must each contain at least one pixel')
    frames, slot_size = collect_frames(source, args.columns, args.rows, args.names)
    shared = bounds_union([frame[3] for frame in frames])
    paths = [args.out_dir / f'{frame[0]}.png' for frame in frames]
    paths += [args.out_dir / 'slice-report.json', args.out_dir / 'contact-sheet.png']
    if not args.overwrite:
        existing = [str(path) for path in paths if path.exists()]
        if existing:
            raise FileExistsError('Outputs already exist: ' + ', '.join(existing))
    if args.input.resolve() in [path.resolve() for path in paths]:
        raise ValueError('Output must not overwrite the source sheet')
    exports, reports = [], []
    for name, frame, rect, bbox in frames:
        crop = ((0, 0, *slot_size) if args.mode == 'cell'
                else shared if args.mode == 'shared' else bbox)
        selected = frame.crop(crop)
        result = Image.new('RGBA', (selected.width + 2 * args.padding,
                                   selected.height + 2 * args.padding))
        result.paste(selected, (args.padding, args.padding))
        alpha = result.getchannel('A')
        histogram = alpha.histogram()
        reports.append(dict(name=name, source_rect=rect, content_bbox=bbox, crop=crop,
                            size=result.size, alpha_extrema=alpha.getextrema(),
                            transparent_pixels=histogram[0], opaque_pixels=histogram[255],
                            partial_alpha_pixels=sum(histogram[1:255]),
                            content_touches_cell_edge=(bbox[0] == 0 or bbox[1] == 0
                                                       or bbox[2] >= rect[2] - rect[0]
                                                       or bbox[3] >= rect[3] - rect[1])))
        exports.append((name, result))
    report = dict(source=str(args.input.resolve()), source_size=source.size,
                  grid=[args.columns, args.rows], mode=args.mode, padding=args.padding,
                  preview_size=args.preview_size, sprites=reports)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for name, result in exports:
        result.save(args.out_dir / f'{name}.png')
    make_preview(exports, args.preview_size).save(args.out_dir / 'contact-sheet.png')
    (args.out_dir / 'slice-report.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Exported {len(exports)} sprites: {args.out_dir.resolve()}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--out-dir', required=True, type=Path)
    parser.add_argument('--columns', required=True, type=int)
    parser.add_argument('--rows', required=True, type=int)
    parser.add_argument('--names', required=True, nargs='+', help='Row-major stems; - skips a cell')
    parser.add_argument('--mode', choices=('cell', 'shared', 'trim'), default='cell')
    parser.add_argument('--padding', type=int, default=0)
    parser.add_argument('--preview-size', type=int, default=64)
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    if args.columns < 1 or args.rows < 1 or args.padding < 0 or args.preview_size < 1:
        parser.error('Grid and preview size must be positive; padding must be nonnegative')
    if len(args.names) > args.columns * args.rows:
        parser.error('More names than cells')
    names = [name for name in args.names if name != '-']
    if not names or len({name.casefold() for name in names}) != len(names):
        parser.error('At least one unique sprite name is required')
    reserved = {'CON', 'PRN', 'AUX', 'NUL'} | {f'{p}{i}' for p in ('COM', 'LPT') for i in range(1, 10)}
    for name in names:
        if (name.casefold() in ('.', '..', 'contact-sheet') or name.endswith(('.', ' '))
                or name.split('.')[0].upper() in reserved
                or any(c in name for c in '<>:"/\\|?*') or any(ord(c) < 32 for c in name)):
            parser.error(f'Use a safe filename stem: {name!r}')
    try:
        export_sheet(args)
    except (ValueError, OSError) as error:
        parser.exit(1, f'Error: {error}\n')


if __name__ == '__main__':
    main()
