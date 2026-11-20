import ast
from pathlib import Path
R=Path(__file__).resolve().parent
class Trace(ast.NodeTransformer):
    def visit_Assign(self,node):
        if any(isinstance(t,ast.Name) and t.id in ['base','lid'] for t in node.targets):
            n=node.targets[0].id
            p=ast.parse(f"print('TRACE {n} line {node.lineno}',round({n}.Volume),len({n}.Solids),{n}.isValid(),flush=True)").body[0]
            return [node,p]
        return node
t=Trace().visit(ast.parse((R/'build_revision06.py').read_text()))
(R/'trace_run.py').write_text(ast.unparse(ast.fix_missing_locations(t)))
