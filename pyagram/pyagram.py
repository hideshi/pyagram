#!/usr/bin/env python3

from argparse import ArgumentParser
import os.path
import pprint

def main():
    parser = ArgumentParser(description='Pyagram: Diagram generator')
    parser.add_argument('-d', '--diagram', help='Diagram type')
    parser.add_argument('-i', '--input', help='Input filename')
    parser.add_argument('-o', '--outpath', help='Output file path', default='.')
    parser.add_argument('-t', '--imagetype', help='Output image type')
    parser.add_argument('-f', '--font', help='Fontname for labels')
    _args = parser.parse_args()
    if not _args.imagetype in ['gif', 'png', 'svg']:
        raise ValueError('Output image type must be gif, png or svg.')
    if not _args.diagram in ['fsmd', 'erd']:
        raise ValueError('Diagram type must be fsmd (Finite State Machine Diagram) or erd(Entity Relation Diagram).')
    if not os.path.exists(_args.outpath):
        raise ValueError('Output file path must exist.')
    if _args.diagram == 'fsmd':
        from finite_state_machine_diagram import FiniteStateMachineDiagram as Diagram
        process_line_by_line = True
    elif _args.diagram == 'erd':
        from pyagram import EntityRelationalDiagram as Diagram
        process_line_by_line = False
    diagram = Diagram(_args.input, _args.outpath, _args.imagetype, _args.font, process_line_by_line)
    diagram.compile()

if __name__ == '__main__':
    main()
