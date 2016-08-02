import os
import os.path
import hashlib
import json
import pprint as p

class Diagram(object):
    def __init__(self, in_file, out_path, image_type, process_line_by_line, fontname = None, verbose = False):
        self.in_file = in_file
        self.out_path = out_path
        self.image_type = image_type
        self.process_line_by_line = process_line_by_line
        self.fontname = fontname
        self.verbose = verbose

    def lexical_analysis(self, src):
        raise NotImplementedError('lexical_analysis method must be overridden and implemented by a descendant class.') 

    def syntactic_analysis(self, src):
        raise NotImplementedError('lexical_analysis method must be overridden and implemented by a descendant class.') 

    def generate_dot(self, ast):
        raise NotImplementedError('lexical_analysis method must be overridden and implemented by a descendant class.') 

    def generate_image(self, dot):
        dot_file = hashlib.md5(bytes(json.dumps(dot), 'utf-8')).hexdigest() + '.dot'
        out_file = os.path.basename(os.path.splitext(self.in_file)[0]) + '.' + self.image_type
        f_out = open(dot_file, 'w', encoding='utf-8')
        f_out.write(dot)
        f_out.flush()
        f_out.close()

        verbose_opt = ' -v' if self.verbose else ''
        command = 'dot -T' + self.image_type + ' -o ' + self.out_path + '/' + out_file + verbose_opt + ' ' + dot_file
        os.system(command)
        if not self.verbose:
            os.remove(dot_file)

    def compile(self):
        f_in = open(self.in_file, 'r', encoding = 'utf-8')
        if self.process_line_by_line:
            parsed_lines = []
            for line in f_in.readlines():
                replaced_line = str(line.replace('\n',''))
                if len(replaced_line) != 0:
                    parsed_line = self.lexical_analysis(replaced_line)
                    parsed_lines.append(parsed_line)
        else:
            lines = f_in.read()
            parsed_lines = self.lexical_analysis(lines)
        ast = self.syntactic_analysis(parsed_lines)
        dot = self.generate_dot(ast)
        self.generate_image(dot)
