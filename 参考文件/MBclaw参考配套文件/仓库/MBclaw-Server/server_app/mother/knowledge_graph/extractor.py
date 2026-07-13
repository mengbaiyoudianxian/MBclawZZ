from __future__ import annotations

import ast
from typing import List
from knowledge_graph.entity import KGNode


class CodeExtractor:

    def extract_from_code(self, code: str) -> List[KGNode]:

        nodes = []

        try:
            tree = ast.parse(code)
        except Exception:
            return []

        for n in ast.walk(tree):

            if isinstance(n, ast.FunctionDef):

                nodes.append(KGNode(
                    id=f"func_{n.name}",
                    type="module",
                    name=n.name,
                    content=ast.get_source_segment(code, n) or "",
                    meta={"kind": "function"}
                ))

            if isinstance(n, ast.ClassDef):

                nodes.append(KGNode(
                    id=f"class_{n.name}",
                    type="module",
                    name=n.name,
                    content="",
                    meta={"kind": "class"}
                ))

        return nodes
