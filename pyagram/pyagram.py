#!/usr/bin/env python3

import sys
from argparse import ArgumentParser
import os
import pyparsing as pp
import hashlib

def lexical_analysis(src):
    string = pp.Regex('[a-zA-Z0-9_/ ａ-ｚＡ-Ｚぁ-ゔゞァ-・ヽヾ゛゜ー一-龯]+')

    blank = pp.LineStart() + pp.LineEnd()

    start = '['
    end = ']' + pp.LineEnd()

    graph_tag = pp.LineStart() + '@'
    graph = graph_tag + start + string + end

    view_tag = pp.LineStart() + '#'
    view = view_tag + start + string + end

    process_tag = pp.LineStart() + '$'
    process = process_tag + start + string + end

    view_transition_operator = pp.LineStart() + '-->'
    view_transition = view_transition_operator + string

    process_transition_operator = pp.LineStart() + '==>'
    process_transition = process_transition_operator + string

    state_machine = pp.OneOrMore(graph | view | process | view_transition | process_transition | string | blank)

    return state_machine.parseString(src)

def syntactic_analysis(src):
    prev = False
    next_view_count = 0
    count = 0
    d = {'graph': {'title': ''}, 'views': {}, 'processes': {}}
    for elem in src:
        if elem[0] == '@' and elem[1] == '[' and elem[3] == ']':
            d['graph'][elem[2]] = ''
            prev = elem

        elif elem[0] == '#' and elem[1] == '[' and elem[3] == ']':
            d['views'][elem[2]] = {}
            d['views'][elem[2]]['path'] = ''
            d['views'][elem[2]]['next_view'] = {}
            d['views'][elem[2]]['next_processes'] = {}
            d['views'][elem[2]]['next_processes']['action'] = {}
            d['views'][elem[2]]['next_processes']['process'] = {}
            prev = elem
            next_view_count = 0
            count = 0

        elif elem[0] == '$' and elem[1] == '[' and elem[3] == ']':
            d['processes'][elem[2]] = {}
            d['processes'][elem[2]]['next_processes'] = {}
            d['processes'][elem[2]]['next_processes']['action'] = {}
            d['processes'][elem[2]]['next_processes']['process'] = {}
            prev = elem
            count = 0

        elif prev and prev[0] == '@':
            d['graph'][prev[2]] = elem[0].strip()

        elif prev and prev[0] == '#' and elem[0] != '-->' and elem[0].startswith('/'):
            d['views'][prev[2]]['path'] = elem[0]

        elif prev and prev[0] == '#' and elem[0] == '-->':
            d['views'][prev[2]]['next_view'][next_view_count] = elem[1].strip()
            next_view_count = next_view_count + 1

        elif prev and prev[0] == '#' and elem[0] != '==>':
            d['views'][prev[2]]['next_processes']['action'][count] = elem[0].strip()

        elif prev and prev[0] == '#' and elem[0] == '==>':
            d['views'][prev[2]]['next_processes']['process'][count] = elem[1].strip()
            count = count + 1

        elif prev and prev[0] == '$' and elem[0] != '==>':
            d['processes'][prev[2]]['next_processes']['action'][count] = elem[0].strip()

        elif prev and prev[0] == '$' and elem[0] == '==>':
            d['processes'][prev[2]]['next_processes']['process'][count] = elem[1].strip()
            count = count + 1

    return d

def generate(in_file, image_type, src):
    dot_file = hashlib.md5().hexdigest()
    out_file = in_file.replace('.txt', '.' + image_type)
    f_out = open(dot_file, 'w')
    f_out.write('digraph sample {')
    f_out.write('graph [label="' + src['graph']['title'] + '",labelloc=t,fontsize=18];')
    for key, value in src['views'].items():
        f_out.write('"' + key + '"' + '[peripheries=2,label="' + key + ' ' + value['path'] + '"];')
    for key, value in src['views'].items():
        if 0 in value['next_view']:
            f_out.write('"' + key + '"' + '->' + '"' + value['next_view'][0] + '"' + '[style=dashed];')
    for key, value in src['processes'].items():
        f_out.write('"' + key + '"' + '[style=filled];')
    for key, value in src['views'].items():
        for key2, value2 in value.items():
            if key2 != 'path' and key2 != 'next_view':
                for key3, value3 in value2['process'].items():
                    if key3 in value2['action']:
                        f_out.write('"' + key + '"' + '->' + '"' + value3 + '"' + '[label="' + value2['action'][key3] + '"];')
                    else:
                        f_out.write('"' + key + '"' + '->' + '"' + value3 + '";')
    for key, value in src['processes'].items():
        for key2, value2 in value.items():
            for key3, value3 in value2['process'].items():
                if key3 in value2['action']:
                    f_out.write('"' + key + '"' + '->' + '"' + value3 + '"' + '[label="' + value2['action'][key3] + '"];')
                else:
                    f_out.write('"' + key + '"' + '->' + '"' + value3 + '";')
    f_out.write('}')
    f_out.flush()

    command1 = 'dot -T' + image_type + ' -o ' + out_file + ' ' + dot_file
    os.system(command1)

    command2 = 'rm -f ' + dot_file
    os.system(command2)

def compile(in_file, image_type):
    f_in = open(in_file, 'r')
    lines = []
    for line in f_in.readlines():
        replaced_line = str(line.replace('\n',''))
        if len(replaced_line) != 0:
            result1 = lexical_analysis(replaced_line)
            lines.append(result1)
    result2 = syntactic_analysis(lines)
    generate(in_file, image_type, result2)

def main():
    parser = ArgumentParser(description='Pyagram: Diagram generator')
    parser.add_argument('-f', '--input', help='Input filename')
    parser.add_argument('-t', '--imagetype', help='Output image type')
    _args = parser.parse_args()
    if not _args.imagetype in ['gif', 'png', 'svg']:
        raise ValueError('Output image type must be gif, png or svg.')
    compile(_args.input, _args.imagetype)

if __name__ == '__main__':
    main()
