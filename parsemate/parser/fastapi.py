import ast
from typing import Any
from pprint import pp

class Visitor(ast.NodeTransformer):

    route_metadata: list[dict[str, dict]] = []

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> ast.AsyncFunctionDef:
        if node.decorator_list:
            for decorator in node.decorator_list:
                self.extract_metadata(decorator, node)
        return node

    def extract_metadata(self, decorator: ast.expr, node: ast.AsyncFunctionDef):
        data = {
            "decorator_attribute": decorator.func.attr,
            "decorator_args": [arg.value for arg in decorator.args],
            "decorator_keywords": [],
            "method_name": node.name,
            "method_args": [{"arg": n.arg, "annotation": getattr(n.annotation, "id", None), "default_value": n.arg} for n in node.args.args],
        }
        for keyword in decorator.keywords:
            if getattr(keyword.value, "id", None) is not None:
                data["decorator_keywords"].append({"arg": keyword.arg, "annotation": keyword.value.id})
            elif getattr(keyword.value, "value", None) is not None:
                data["decorator_keywords"].append({"arg": keyword.arg, "annotation": f"{keyword.value.value.id}[{keyword.value.slice.id}]"})
        self.route_metadata.append(data)


class FastAPIParser:

    def parse(self, file_path: str) -> ast.Module:
        with open(file_path) as f:
            tree = ast.parse(f.read())
        return tree

    def extract(self, tree: ast.Module) -> list[dict[str, Any]]:
       visitor = Visitor()
       visitor.visit(tree)
       return visitor.route_metadata
