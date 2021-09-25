import os
import click

PDF2TXT = 'pdf2txt.py'

@click.command()
@click.option('--input', help='Input (digital pdf)')
@click.option('--output', default='.', help='Output directory to extract the txt to')
def convert_pdf(input, output):
    filename = (os.path.split(input)[-1]).replace('pdf', 'txt')
    s = f'{PDF2TXT} "{input}" > "{os.path.join(output, filename)}"'
    print(s)
    os.system(s)

if __name__ == '__main__':
    convert_pdf()

