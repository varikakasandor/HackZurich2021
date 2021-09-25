import os
import click

HTML = 'html'
PDF2TXT = 'pdf2txt.py'
TXT = 'txt'

@click.command()
@click.option('--input', help='Input (digital pdf)')
@click.option('--output', default='.', help='Output directory to extract the txt to')
def click_convert_pdf(input, output):
    convert_pdf(input, output)


def convert_pdf(input, output, mode=TXT):
    filename = (os.path.split(input)[-1]).replace('pdf', mode)
    layout = '--layoutmode exact '
    if mode == TXT:
        layout = ''
        mode = 'text'
    s = f'{PDF2TXT} --output_type {mode} {layout}"{input}" > "{os.path.join(output, filename)}"'
    os.system(s)
    return filename


if __name__ == '__main__':
    click_convert_pdf()

