import sys
import re
import pprint
import pyparsing as pp

def lexical_analysis(src):
    string = pp.Word(pp.alphanums + '_' + '/' + ' ')

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
    d = {'graph': {}, 'views': {}, 'processes': {}}
    for elem in src:
        #print(elem)
        #print(prev)
        if elem[0] == '@' and elem[1] == '[' and elem[3] == ']':
            d['graph'][elem[2]] = ''
            prev = elem

        elif elem[0] == '#' and elem[1] == '[' and elem[3] == ']':
            d['views'][elem[2]] = {}
            d['views'][elem[2]]['path'] = {}
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
            d['graph'][prev[2]] = elem[0]

        elif prev and prev[0] == '#' and elem[0] != '-->' and elem[0].startswith('/'):
            d['views'][prev[2]]['path'] = elem[0]

        elif prev and prev[0] == '#' and elem[0] == '-->':
            d['views'][prev[2]]['next_view'][next_view_count] = elem[1]
            next_view_count = next_view_count + 1

        elif prev and prev[0] == '#' and elem[0] != '==>':
            d['views'][prev[2]]['next_processes']['action'][count] = elem[0]

        elif prev and prev[0] == '#' and elem[0] == '==>':
            d['views'][prev[2]]['next_processes']['process'][count] = elem[1]
            count = count + 1

        elif prev and prev[0] == '$' and elem[0] != '==>':
            d['processes'][prev[2]]['next_processes']['action'][count] = elem[0]

        elif prev and prev[0] == '$' and elem[0] == '==>':
            d['processes'][prev[2]]['next_processes']['process'][count] = elem[1]
            count = count + 1

    return d

def compile(filename):
    f = open(filename, 'r')
    src = []
    for line in f.readlines():
        l = line.replace('\n','')
        if len(l) != 0:
            res1 = lexical_analysis(l)
            src.append(res1)
    #print(src)
    res2 = syntactic_analysis(src)
    pprint.pprint(res2)

if __name__ == '__main__':
    compile(sys.argv[1])
