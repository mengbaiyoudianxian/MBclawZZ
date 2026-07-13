from __future__ import annotations

import ast
from typing import List
from knowledge_graph_v2.entity import KGEntity


class CodeStructureExtractor:

    def extract(self, code: str) -> List[KGEntity]:

        nodes = []

        try:
            tree = ast.parse(code)
        except Exception:
            return []

        for n in ast.walk(tree):

            if isinstance(n, ast.FunctionDef):

                nodes.append(KGEntity(
                    id=f"func_{n.name}",
                    type="tool",
                    name=n.name,
                    content=ast.get_source_segment(code, n) or "",
                    meta={"ast": "function"}
                ))

            if isinstance(n, ast.ClassDef):

                nodes.append(KGEntity(
                    id=f"class_{n.name}",
                    type="module",
                    name=n.name,
                    content="",
                    meta={"ast": "class"}
                ))

        return nodes
