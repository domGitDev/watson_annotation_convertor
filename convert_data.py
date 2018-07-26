
""" Module to convert IBM Watson NLP text annotation to simple json with bellow format
  {
    "category1": [],
    'category2': [],
    ....
  }
 """
import os
import json
import glob
import argparse
import functools


parser = argparse.ArgumentParser(description="Convert watson annotation to simple json!")
parser.add_argument('dir', type=str, help='input directory to annotated json files.')
parser.add_argument('filename', type=str, help='output filename to convert json.')

def validate_annotation(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 'text' not in args[0] or 'sentences' not in args[0] or 'mentions' not in args[0]:
            raise TypeError(
                'missing keys=[text, sentences, mentions] in anotation data.')	
        return func(*args, **kwargs)
    return wrapper


def load_watson_ks_annotaion(filename):
    data = {}
    if not os.path.exists(filename):
        print('File not exist %s' % filename)
        return data
    with open(filename, 'r') as f:
        data = json.loads(f.read())
    return data


@validate_annotation
def convert_data(data):
    out_data = {}
    sentences_str = data['text']
    for item in data['mentions']:
        try:
            begin = int(item['begin'])
            end = int(item['end'])
            category = item['type']
            if category not in out_data:
                out_data[category] = []
            out_data[category].append(sentences_str[begin:end])

        except KeyError as e:
            print(str(e))
            pass
        except IndexError as e:
            print(str(e))
            pass
    return out_data



def run_convertor(filenames, out_filename):
    if filenames:
        out_data = {}
        for filename in filenames:
            data = load_watson_ks_annotaion(filename)
            output = convert_data(data)
            out_data.update(output)

        with open(out_filename, 'w') as f:
            f.write(json.dumps(out_data, indent=4))
        print('Output: %s' % out_filename)


if __name__ == '__main__':
    args = parser.parse_args()
    if not os.path.exists(args.dir):
        raise ValueError('input directory does not exist: %s' % args.dir)

    out_dir = os.path.dirname(args.filename)
    if out_dir and not os.path.exists(out_dir):
        raise ValueError('output directory does not exist: %s' % out_dir)

    filenames = glob.glob(os.path.join(args.dir, '*.json'))
    if filenames:
        print('json files found: %d.' % len(filenames))
        run_convertor(filenames, args.filename)
    else:
        print('json files found: 0.')
