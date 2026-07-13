class CodeExtractor:

    def extract(self, runtime_graph, memory, audit_log):

        return {
            "modules": runtime_graph.nodes if runtime_graph else {},
            "flows": audit_log if audit_log else [],
            "knowledge": memory if memory else {}
        }
