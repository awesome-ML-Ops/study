import sys
import os
import re
import xml.etree.ElementTree
import conf
import io

INPUT = conf.source_xml
OUTPUT = conf.source_tsv

TAG = 'python'

try: #python2
    reload(sys)
    sys.setdefaultencoding('utf-8')
except: pass

def print_usage(msg):
    if msg:
        sys.stderr.write('{}\n'.format(msg))
    sys.stderr.write('Usage:\n')
    sys.stderr.write('\tpython posts_to_tsv.py\n')


def process_posts(fd_in, fd_out, target_tag):
    num = 1
    for line in fd_in:
        try:
            attr = xml.etree.ElementTree.fromstring(line).attrib

            id = attr.get('Id', '')
            label = 1 if target_tag in  attr.get('Tags', '') else 0
            title = attr.get('Title', '').replace('\t', ' ').replace('\n', ' ').replace('\r', ' ')
            body = attr.get('Body', '').replace('\t', ' ').replace('\n', ' ').replace('\r', ' ')
            text = title + ' ' + body

            fd_out.write(u'{}\t{}\t{}\n'.format(id, label, text))

            num += 1
        except Exception as ex:
            sys.stderr.write('Skipping the line {}: {}\n'.format(num, ex))


if __name__ == '__main__':
    target_tag = u'<' + TAG + '>'

    if not os.path.exists(INPUT):
        print_usage('Input file {} does not exist'.format(INPUT))
        sys.exit(1)

    with io.open(INPUT, encoding='utf8') as fd_in:
        with io.open(OUTPUT, 'w', encoding='utf8') as fd_out:
            process_posts(fd_in, fd_out, target_tag)

