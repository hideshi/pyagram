import sys
import re
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
    d = {'graph': {}, 'views': {}, 'processes': {}}
    for elem in src:
        if elem[0] == '@' and elem[1] == '[' and elem[3] == ']':
            d['graph'][elem[2]] = ''
            prev = elem

        elif elem[0] == '#' and elem[1] == '[' and elem[3] == ']':
            d['views'][elem[2]] = {}
            prev = elem

        elif elem[0] == '$' and elem[1] == '[' and elem[3] == ']':
            d['processes'][elem[2]] = {}
            prev = elem

        elif prev and prev[0] == '@':
            d['graph'][prev[2]] = elem[0]

        elif prev and prev[0] == '#':
            d['views'][prev[2]] = elem[0]

        elif prev and prev[0] == '$':
            d['processes'][prev[2]] = elem[0]

        #elif prev and prev[0] == '-->':
        #    d['views'][prev[2]].append(elem[1])

        #elif prev and prev[0] == '==>':
        #    d['views'][prev[2]].append(elem[1])

    return d

def compile(filename):
    f = open(filename, 'r')
    src = []
    for line in f.readlines():
        print(line)
        res1 = lexical_analysis(line)
        if (len(res1) == 1 and len(res1[0]) != 1) or len(res1) > 1:
            src.append(res1)
            print(res1)
        print('--------------------------')
    res2 = syntactic_analysis(src)
    print(res2)

if __name__ == '__main__':
    compile(sys.argv[1])
