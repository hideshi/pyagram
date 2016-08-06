import pyparsing as pp
import pprint as p
from pyagram.diagram import Diagram

class StateTransitionDiagram(Diagram):
    def lexical_analysis(self, src):
        string = pp.Regex('[a-zA-Z0-9_{}"=+\-*/\.:;&%@$#<>? ａ-ｚＡ-Ｚぁ-ゔゞァ-・ヽヾ゛゜ー一-龯]+')
    
        blank = pp.LineStart() + pp.LineEnd()
    
        start = '['
        end = ']' + pp.LineEnd()
    
        graph_tag = pp.LineStart() + '@'
        graph = graph_tag + start + string + end
    
        view_tag = pp.LineStart() + '#'
        view = view_tag + start + string + end
    
        server_process_tag = pp.LineStart() + '$'
        server_process = server_process_tag + start + string + end
    
        client_process_tag = pp.LineStart() + '%'
        client_process = client_process_tag + start + string + end
    
        view_transition_identifier = pp.LineStart() + '-->'
        view_transition = view_transition_identifier + string
    
        process_transition_identifier = pp.LineStart() + '==>'
        process_transition = process_transition_identifier + string
    
        state_machine = pp.OneOrMore(graph | view | server_process | client_process | view_transition | process_transition | string | blank)
    
        return state_machine.parseString(src)

    def syntactic_analysis(self, src):
        prev = False
        next_views_count = 0
        count = 0
        d = {'graph': {'title': ''}, 'views': {}, 'server_processes': {}, 'client_processes': {}}
        for elem in src:
            if elem[0] == '@' and elem[1] == '[' and elem[3] == ']':
                d['graph'][elem[2]] = ''
                prev = elem
    
            elif elem[0] == '#' and elem[1] == '[' and elem[3] == ']':
                d['views'][elem[2]] = {}
                d['views'][elem[2]]['path'] = ''
                d['views'][elem[2]]['next_views'] = {}
                d['views'][elem[2]]['next_server_processes'] = {}
                d['views'][elem[2]]['next_server_processes']['action'] = {}
                d['views'][elem[2]]['next_server_processes']['process'] = {}
                d['views'][elem[2]]['next_client_processes'] = {}
                d['views'][elem[2]]['next_client_processes']['action'] = {}
                d['views'][elem[2]]['next_client_processes']['process'] = {}
                prev = elem
                next_views_count = 0
                count = 0
    
            elif elem[0] == '$' and elem[1] == '[' and elem[3] == ']':
                d['server_processes'][elem[2]] = {}
                d['server_processes'][elem[2]]['next_server_processes'] = {}
                d['server_processes'][elem[2]]['next_server_processes']['action'] = {}
                d['server_processes'][elem[2]]['next_server_processes']['process'] = {}
                prev = elem
                count = 0
    
            elif elem[0] == '%' and elem[1] == '[' and elem[3] == ']':
                d['client_processes'][elem[2]] = {}
                d['client_processes'][elem[2]]['next_client_processes'] = {}
                d['client_processes'][elem[2]]['next_client_processes']['action'] = {}
                d['client_processes'][elem[2]]['next_client_processes']['process'] = {}
                prev = elem
                count = 0
    
            elif prev and prev[0] == '@':
                d['graph'][prev[2]] = elem[0].strip()
    
            elif prev and prev[0] == '#' and elem[0] != '-->' and elem[0].startswith('/'):
                d['views'][prev[2]]['path'] = elem[0]
    
            elif prev and prev[0] == '#' and elem[0] == '-->':
                d['views'][prev[2]]['next_views'][next_views_count] = elem[1].strip()
                next_views_count = next_views_count + 1
    
            elif prev and prev[0] == '#' and elem[0] != '==>':
                d['views'][prev[2]]['next_server_processes']['action'][count] = elem[0].strip()
    
            elif prev and prev[0] == '#' and elem[0] == '==>':
                d['views'][prev[2]]['next_server_processes']['process'][count] = elem[1].strip()
                count = count + 1
    
            elif prev and prev[0] == '$' and elem[0] != '==>':
                d['server_processes'][prev[2]]['next_server_processes']['action'][count] = elem[0].strip()
    
            elif prev and prev[0] == '$' and elem[0] == '==>':
                d['server_processes'][prev[2]]['next_server_processes']['process'][count] = elem[1].strip()
                count = count + 1
    
            elif prev and prev[0] == '%' and elem[0] != '==>':
                d['client_processes'][prev[2]]['next_client_processes']['action'][count] = elem[0].strip()
    
            elif prev and prev[0] == '%' and elem[0] == '==>':
                d['client_processes'][prev[2]]['next_client_processes']['process'][count] = elem[1].strip()
                count = count + 1
    
        return d

    def generate_dot(self, src):
        dot = 'digraph sample {\n'
        fontsetting = 'fontname="' + self.fontname + '"' if self.fontname else ''
        dot = dot + '\tgraph [label="' + src['graph']['title'] + '", labelloc=t, fontsize=18, ' + fontsetting + '];\n'
        dot = dot + '\tnode ['+fontsetting+'];\n'
        dot = dot + '\tedge ['+fontsetting+'];\n'
        for key, value in src['views'].items():
            dot = dot + '\t"' + key + '" ' + '[peripheries=2, label="' + key + ' ' + value['path'] + '"];\n'
        for key, value in src['views'].items():
            for key2, value2 in value['next_views'].items():
                dot = dot + '\t"' + key + '" ' + ' -> ' + '"' + value2 + '"' + '[style=dashed];\n'
        for key, value in src['server_processes'].items():
            dot = dot + '\t"' + key + '" ' + '[style=filled];\n'
        for key, value in src['views'].items():
            for key2, value2 in value.items():
                if key2 != 'path' and key2 != 'next_views':
                    for key3, value3 in value2['process'].items():
                        if key3 in value2['action']:
                            dot = dot + '\t"' + key + '"' + ' -> ' + '"' + value3 + '"' + '[label="' + value2['action'][key3] + '"];\n'
                        else:
                            dot = dot + '\t"' + key + '"' + ' -> ' + '"' + value3 + '";\n'
        for key, value in src['server_processes'].items():
            for key2, value2 in value.items():
                for key3, value3 in value2['process'].items():
                    if key3 in value2['action']:
                        dot = dot + '\t"' + key + '"' + ' -> ' + '"' + value3 + '"' + '[label="' + value2['action'][key3] + '"];\n'
                    else:
                        dot = dot + '\t"' + key + '"' + ' -> ' + '"' + value3 + '";\n'
        for key, value in src['client_processes'].items():
            for key2, value2 in value.items():
                for key3, value3 in value2['process'].items():
                    if key3 in value2['action']:
                        dot = dot + '"' + key + '"' + ' -> ' + '"' + value3 + '"' + '[label="' + value2['action'][key3] + '"];\n'
                    else:
                        dot = dot + '"' + key + '"' + ' -> ' + '"' + value3 + '";'
        dot = dot + '}'
        return dot
