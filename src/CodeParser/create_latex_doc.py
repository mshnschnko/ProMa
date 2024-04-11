from syntax.build_ast import TreeNode
from dsl_token import Token
from dsl_info import Terminal, keys, Nonterminal

class LatexCreator:
    def __init__(self, dest_path: str, preamble_path: str = 'preamble.txt') -> None:
        self.preamble_path = preamble_path
        self.dest_path = dest_path
        self.nodes = []
        self.tabs = 0

    def create_begin(self):
        with open(self.preamble_path, 'r', encoding='utf8') as preamble_file:
            preamble = preamble_file.read()

        with open(self.dest_path, 'w', encoding='utf8') as latex_file:
            latex_file.write(preamble)
            latex_file.write('\n\\begin{document}\n\\noindent\n')

        self.lines: list[str] = []

    def create_end(self):
        with open(self.dest_path, 'a+', encoding='utf8') as latex_file:
            latex_file.writelines(self.lines)
            latex_file.write('\n\\end{document}')

    def process_node(self, node: TreeNode, latex_file) -> None:
        if TreeNode.Type.NONTERMINAL == node.type:
            match node.nonterminalType:
                case Nonterminal.ASSIGNMENT:
                    latex_file.write(f'\n${node.childs[2].childs[0].token.str} := {node.childs[4].childs[0].token.str}$')
                    self.nodes = self.nodes[1:]
                    self.nodes = node.childs + self.nodes
                    return
                case Nonterminal.NAME:
                    latex_file.write(f'${node.childs[0].childs[0].token.str}$ : ')
                    return
                case Nonterminal.DEFINITION:
                    # latex_file.write(f'\n${node[0].childs[2].childs[0].childs[0].token.str}$ : ')
                    for child in node.childs[1:]:
                        self.process_node(child, latex_file)
                    return
                case Nonterminal.TYPE:
                    self.process_node(node.childs[0])
                    return
                case Nonterminal.TYPE_ARRAY:
                    # latex_file.write('\n\\textbf{array} $' + node.childs[2].childs[0].token.str + '$ \\textbf{of} ')
                    for i, child in enumerate(node.childs):
                        # if child.type == TreeNode.Type.NONTERMINAL:
                        self.process_node(child, latex_file)
                        if i == 2:
                            latex_file.write(' \\textbf{of} ')
                    return
                case Nonterminal.TYPE_STRUCT:
                    # latex_file.write('\n\\textbf{struct} $\{')

                    for i, child in enumerate(node.childs):
                        # if child.type == TreeNode.Type.NONTERMINAL:
                        self.process_node(child, latex_file)
                        if i == 0:
                            latex_file.write(' \{ ')
                    latex_file.write('\}')
                    return
                case Nonterminal.STATEMENT:
                    self.process_node(node.childs[0])
                    return
                case _:
                    self.nodes = self.nodes[1:]
                    self.nodes = node.childs + self.nodes
        else:
            token = node.token
            if Token.Type.TERMINAL == token.type:
                if token.terminalType == Terminal.other:
                    latex_file.write(f'${token.str}$')
            elif Token.Type.KEY == token.type:
                if token.terminalType == Terminal.word:
                    latex_file.write('\\textbf{' + token.str + '}')
                if token.terminalType == Terminal.char_sequence:
                    pass


    def parse_ast(self, ast: TreeNode) -> None:
        with open(self.dest_path, 'a+') as latex_file:
            i = 1
            self.nodes = [ast]
            while len(self.nodes):
                node = self.nodes[0]
                self.process_node(self.nodes[0], latex_file)
                print(len(self.nodes))
                # nodes = nodes[1:]
                # nodes = [(child, i) for child in node[0].childs] + nodes
                # node = nodes[0]
                # if TreeNode.Type.NONTERMINAL == node[0].type:
                #     if node[1] != 0:
                #         pass
                #     match node[0].nonterminalType:
                #         case Nonterminal.ASSIGNMENT:
                #             latex_file.write(f'\n${node[0].childs[2].childs[0].token.str} := {node[0].childs[4].childs[0].token.str}$')
                #             nodes = nodes[1:]
                #             continue
                #         case Nonterminal.NAME:
                #             latex_file.write(f'${node[0].childs[0].childs[0].token.str}$ : ')
                #         case Nonterminal.DEFINITION:
                #             # latex_file.write(f'\n${node[0].childs[2].childs[0].childs[0].token.str}$ : ')
                #             nodes = nodes[1:]
                #             nodes = [(child, i) for child in node[0].childs[2:]] + nodes
                #             continue
                #         case Nonterminal.TYPE_ARRAY:
                #             latex_file.write('\n\\textbf{array} $' + node[0].childs[2].childs[0].token.str + '$ \\textbf{of} ')
                #             nodes = nodes[1:]
                #             nodes = [(child, i) for child in node[0].childs[4:]] + nodes
                #             continue
                #         case Nonterminal.TYPE_STRUCT:
                #             latex_file.write('\n\\textbf{struct} $\{')
                #             nodes = nodes[1:]
                #             nodes = [(child, i) for child in node[0].childs if child.type == TreeNode.Type.NONTERMINAL] + nodes
                #             continue
                #     nodes = nodes[1:]
                #     nodes = [(child, i) for child in node[0].childs] + nodes
                # else:
                #     token = node[0].token
                #     if Token.Type.TERMINAL == token.type:
                #         if token.terminalType == Terminal.other:
                #             latex_file.write(f'${token.str}$')
                #     elif Token.Type.KEY == token.type:
                #         if token.terminalType == Terminal.word:
                #             if token.str == 'assign':
                #                 pass
                #             latex_file.write('\\textbf{' + token.str + '}')
                #         if token.terminalType == Terminal.char_sequence:
                #             latex_file.write('')
                #     nodes = nodes[1:]
                # i += 1


    def dfs(self, ast: TreeNode) -> None:
        if ast:
            if ast.type == TreeNode.Type.NONTERMINAL:
                if ast.nonterminalType == Nonterminal.INPUT:
                    self.lines.append('\\\\\n')
                    self.lines.append('\\textbf{Вход:} ')
                    for child in ast.childs[1:]:
                        self.dfs(child)
                    self.lines.append('\\\\\n')
                    return
                if ast.nonterminalType == Nonterminal.ALG_OUTPUT:
                    self.lines.append('\\textbf{Выход:} ')
                    for child in ast.childs:
                        self.dfs(child)
                    self.lines.append('\\\\\n')
                    self.tabs += 1
                    return
                if ast.nonterminalType == Nonterminal.BRANCHING:
                    for child in ast.childs[:3]:
                        self.dfs(child)
                    self.tabs += 1
                    self.lines.append('\\textbf{then} \\\\\n')
                    br_count = 0
                    i = 3
                    # child = ast.childs[i]
                    while br_count < 2 and i < len(ast.childs):
                        child = ast.childs[i]
                        if child.type == TreeNode.Type.TOKEN and child.token.type == Token.Type.KEY \
                                and child.token.terminalType == Terminal.char_sequence and child.token.str == '(':
                            br_count += 1
                        self.dfs(child)
                        i += 1
                    if ast.type == TreeNode.Type.TOKEN and ast.childs[i].token.type == Token.Type.KEY \
                        and ast.childs[i].token.terminalType == Terminal.word and ast.childs[i].token.str == ')':
                        pass
                    else:
                        self.lines.append((self.tabs - 1) * '\\tab ' + '\\textbf{else} \\\\\n')
                    for child in ast.childs[i:]:
                        self.dfs(child)
                    return
                if ast.nonterminalType == Nonterminal.FOR or ast.nonterminalType == Nonterminal.WHILE:
                    for child in ast.childs[:3]:
                        self.dfs(child)
                    self.tabs += 1
                    self.lines.append('\\textbf{do} \\\\\n')
                    for child in ast.childs[3:]:
                        self.dfs(child)
                    return
                # if ast.nonterminalType == Nonterminal.WHILE:

                if ast.nonterminalType == Nonterminal.NAME:
                    self.dfs(ast.childs[0].childs[0])
                    self.lines.append(' $:$ ')
                    return
                if ast.nonterminalType == Nonterminal.PARAM_LIST:
                    self.lines.append(' (')
                    for child in [chi for chi in ast.childs[:-1] if chi.type == TreeNode.Type.NONTERMINAL]:
                        self.dfs(child)
                        self.lines.append(', ')
                    self.dfs(ast.childs[-1])
                    self.lines.append(') ')
                    return
                if ast.nonterminalType == Nonterminal.ASSIGNMENT:
                    self.dfs(ast.childs[2].childs[0])
                    self.lines.append(' $:=$ ')
                    self.dfs(ast.childs[4].childs[0])
                    self.lines.append('\\\\\n')
                    return
                if ast.nonterminalType == Nonterminal.DEFINITION:
                    for child in ast.childs[1:]:
                        self.dfs(child)
                    self.lines.append('\\\\\n')
                    return
                if ast.nonterminalType == Nonterminal.TYPE_ARRAY:
                    self.dfs(ast.childs[0])
                    self.dfs(ast.childs[2])
                    self.lines.append(' \\textbf{of} ')
                    self.dfs(ast.childs[4].childs[0])
                    return
                if ast.nonterminalType == Nonterminal.TYPE_STRUCT:
                    self.dfs(ast.childs[0])
                    self.lines.append(' \{')
                    for child in ast.childs[1:]:
                        self.dfs(child)
                    self.lines.append('\} ')
                    return
                if ast.nonterminalType == Nonterminal.COMMENT:
                    self.lines[-1] = self.lines[-1].replace('\n', ' ')
                    self.lines.append('{\color{gray}// ' + ast.childs[2].childs[0].token.str + '}\\\\\n')
                    return
            elif ast.type == TreeNode.Type.TOKEN:
                if ast.token.type == Token.Type.KEY and ast.token.terminalType == Terminal.word:
                    if ast.token.str in ['integer', 'string', 'char', 'array', 'struct']:
                        self.lines.append('\\textbf{' + ast.token.str + '} ')
                    elif ast.token.str == 'algorithm':
                        self.lines.append('Алгоритм ')
                    elif 'end ' in ast.token.str:
                        self.tabs -= 1
                        s = '\\tab ' if len(self.lines) > 0 and '\n' in self.lines[-1] else ''
                        self.lines.append(self.tabs * s + '\\textbf{' + ast.token.str + '}\\\\\n')
                    else:
                        s = '\\tab ' if len(self.lines) > 0 and '\n' in self.lines[-1] else ''
                        self.lines.append(self.tabs * s + '\\textbf{' + ast.token.str + '} ')
                elif ast.token.type == Token.Type.TERMINAL and ast.token.terminalType == Terminal.word:
                    s = '\\tab ' if len(self.lines) > 0 and '\n' in self.lines[-1] else ''
                    self.lines.append(self.tabs * s + f'{ast.token.str}')
                elif ast.token.type == Token.Type.TERMINAL and ast.token.terminalType == Terminal.other:
                    self.lines.append(f' ${ast.token.str}$ ')
            for child in ast.childs:
                self.dfs(child)