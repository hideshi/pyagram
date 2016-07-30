#!/usr/bin/env python3

from argparse import ArgumentParser
import os.path
import pprint as p

def main():
    parser = ArgumentParser(description='Pyagram: Diagram generator')
    parser.add_argument('-i', '--input', help='Input filename')
    parser.add_argument('-o', '--outpath', help='Output file path', default='.')
    parser.add_argument('-t', '--imagetype', help='Output image type')
    parser.add_argument('-f', '--font', help='Fontname for labels')
    _args = parser.parse_args()
    if not _args.imagetype in ['gif', 'png', 'svg']:
        raise ValueError('Output image type must be gif, png or svg.')
    if not os.path.exists(_args.outpath):
        raise ValueError('Output file path must exist.')
    from state_transition_diagram import StateTransitionDiagram as Diagram
    process_line_by_line = True
    diagram = Diagram(_args.input, _args.outpath, _args.imagetype, process_line_by_line, _args.font)
    diagram.compile()

if __name__ == '__main__':
    main()
