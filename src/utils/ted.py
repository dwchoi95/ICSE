import ast
from zss import simple_distance, Node

class TED:
    @classmethod
    def __ast_to_tree(cls, node):
        """
        Recursively converts an AST node into a tree format suitable for zss library.
        """
        if not isinstance(node, ast.AST):
            return Node(str(node))
        
        tree = Node(type(node).__name__)
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    tree.addkid(cls.__ast_to_tree(item))
            elif isinstance(value, ast.AST):
                tree.addkid(cls.__ast_to_tree(value))
            else:
                tree.addkid(Node(str(value)))
        
        return tree

    @classmethod
    def __compute_ast_size(cls, tree):
        """
        Computes the size of the AST tree.
        """
        if tree is None:
            return 0
        size = 1  # count the current node
        for child in tree.children:
            size += cls.__compute_ast_size(child)
        return size
    
    @classmethod
    def relative_patch_size(cls, buggy, patch):
        buggy_tree = cls.__ast_to_tree(ast.parse(buggy))
        patch_tree = cls.__ast_to_tree(ast.parse(patch))
        ted = simple_distance(buggy_tree, patch_tree)
        buggy_size = cls.__compute_ast_size(buggy_tree)
        return round(ted / buggy_size, 2)
    
    @classmethod
    def compute_ted(cls, code1, code2):
        """
        Computes the tree edit distance between two pieces of Python code.
        """
        tree1 = cls.__ast_to_tree(ast.parse(code1))
        tree2 = cls.__ast_to_tree(ast.parse(code2))
        return simple_distance(tree1, tree2)

    @classmethod
    def compute_sim(cls, code1, code2):
        """
        Computes the similarity between two pieces of Python code based on tree edit distance.
        """
        tree1 = cls.__ast_to_tree(ast.parse(code1))
        tree2 = cls.__ast_to_tree(ast.parse(code2))
        distance = simple_distance(tree1, tree2)
        max_distance = cls.__compute_ast_size(tree1) + cls.__compute_ast_size(tree2)
        similarity = 1 - distance / max_distance
        return similarity
    
    


# Example usage
class TEDTest:
    @staticmethod
    def run(code1, code2):
        distance = TED.compute_ted(code1, code2)
        print(f"Distance: {distance}")
        similarity = TED.compute_sim(code1, code2)
        print(f"Similarity: {similarity}")
        rps = TED.relative_patch_size(code1, code2)
        print(f"RPS: {rps}")
