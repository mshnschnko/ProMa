from argparse import ArgumentParser
from build_ast import parse_code
from create_latex_doc import LatexCreator

if __name__ == '__main__':
    parser = ArgumentParser(prog="create_ast", description="Create AST")
    parser.add_argument("-c", "--code", dest="codeFile", help="File with code", metavar="FILE", default='D:\spbstu_projects\ProMa\src\CodeParser\example.txt', required=False)
    parser.add_argument("-j", "--json", dest="jsonFile", help="Json file with settings", metavar="FILE", default='D:\spbstu_projects\ProMa\src\CodeParser\grammar\proma.json', required=False)
    parser.add_argument("-d", "--dest", dest="destFile", help="Result latex file", metavar="FILE", default='D:\spbstu_projects\ProMa\src\CodeParser\example.tex', required=False)
    parser.add_argument("-p", "--preamble", dest="preambleFile", help="Preamble", metavar="FILE", default='D:\spbstu_projects\ProMa\src\CodeParser\preamble.txt', required=False)
    args = parser.parse_args()

    ast = parse_code(args.jsonFile, args.codeFile)

    lc = LatexCreator(args.destFile, args.preambleFile)
    lc.create_begin()
    # lc.parse_ast(ast)
    lc.dfs(ast)
    lc.create_end()
