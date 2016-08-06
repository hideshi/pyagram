#!/usr/bin/env python3

from argparse import ArgumentParser
import os.path
import pprint as p

def main():
    parser = ArgumentParser(description='Pyagram: Diagram generator')
    parser.add_argument('-d', '--diagram', help='Diagram type')
    parser.add_argument('-i', '--input', help='Input filename')
    parser.add_argument('-o', '--outpath', help='Output file path', default='.')
    parser.add_argument('-t', '--imagetype', help='Output image type')
    parser.add_argument('-f', '--font', help='Fontname for labels')
    parser.add_argument('-v', '--verbose', help='Print various information mode', action='store_true', default=False)
    _args = parser.parse_args()
    if not _args.imagetype in ['gif', 'png', 'svg']:
        raise ValueError('Output image type must be gif, png or svg.')
    if not _args.diagram in ['std', 'erd']:
        raise ValueError('Diagram type must be std(State Transition Diagram) or erd(Entity Relationship Diagram).')
    if not os.path.exists(_args.outpath):
        raise ValueError('Output file path must exist.')
    if _args.diagram == 'std':
        from pyagram.state_transition_diagram import StateTransitionDiagram as Diagram
        process_line_by_line = True
    elif _args.diagram == 'erd':
        from pyagram.entity_relationship_diagram import EntityRelationshipDiagram as Diagram
        process_line_by_line = False
    diagram = Diagram(_args.input, _args.outpath, _args.imagetype, process_line_by_line, _args.font, _args.verbose)
    diagram.compile()

if __name__ == '__main__':
    main()
