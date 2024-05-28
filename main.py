from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QMessageBox
from PyQt6.QtGui import QColor

class SearchNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class SearchTree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        if self.root is None:
            self.root = SearchNode(data)
        else:
            self._insert_recursive(self.root, data)

    def _insert_recursive(self, node, data):
        if data < node.data:
            if node.left is None:
                node.left = SearchNode(data)
            else:
                self._insert_recursive(node.left, data)
        else:
            if node.right is None:
                node.right = SearchNode(data)
            else:
                self._insert_recursive(node.right, data)

    def search(self, data):
        return self._search_recursive(self.root, data)

    def _search_recursive(self, node, data):
        if node is None:
            return False
        if node.data == data:
            return True
        if data < node.data:
            return self._search_recursive(node.left, data)
        else:
            return self._search_recursive(node.right, data)

    def delete(self, data):
        self.root = self._delete_recursive(self.root, data)

    def _delete_recursive(self, node, data):
        if node is None:
            return node

        if data < node.data:
            node.left = self._delete_recursive(node.left, data)
        elif data > node.data:
            node.right = self._delete_recursive(node.right, data)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            node.data = self._min_value_node(node.right)
            node.right = self._delete_recursive(node.right, node.data)

        return node

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current.data

    def inorder_list(self):
        result = []
        self._inorder_list_recursive(self.root, result)
        return result

    def _inorder_list_recursive(self, node, result):
        if node:
            self._inorder_list_recursive(node.left, result)
            result.append(node.data)
            self._inorder_list_recursive(node.right, result)

class SearchTreeGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Binary Tree")
        self.setGeometry(100, 100, 800, 600)

        self.tree = SearchTree()

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)

        self.insert_input = QLineEdit()
        self.search_input = QLineEdit()
        self.delete_input = QLineEdit()

        self.insert_button = QPushButton("Insert")
        self.search_button = QPushButton("Search")
        self.delete_button = QPushButton("Delete")
        self.list_ascend_button = QPushButton("List Ascending")
        self.export_ascend_button = QPushButton("Export to txt")

        self.TreeUI()

    def TreeUI(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout()

        insert_layout = QHBoxLayout()
        insert_layout.addWidget(QLabel("Insert value:"))
        insert_layout.addWidget(self.insert_input)
        insert_layout.addWidget(self.insert_button)

        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search value:"))
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)

        delete_layout = QHBoxLayout()
        delete_layout.addWidget(QLabel("Delete value:"))
        delete_layout.addWidget(self.delete_input)
        delete_layout.addWidget(self.delete_button)

        list_layout = QHBoxLayout()
        list_layout.addWidget(QLabel("List values:"))
        list_layout.addWidget(self.list_ascend_button)

        export_layout = QHBoxLayout()
        export_layout.addWidget(QLabel("Export to txt:"))
        export_layout.addWidget(self.export_ascend_button)

        main_layout.addWidget(self.view)
        main_layout.addLayout(insert_layout)
        main_layout.addLayout(search_layout)
        main_layout.addLayout(delete_layout)
        main_layout.addLayout(list_layout)
        main_layout.addLayout(export_layout)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.insert_button.clicked.connect(self.insert_node)
        self.search_button.clicked.connect(self.search_node)
        self.delete_button.clicked.connect(self.delete_node)
        self.list_ascend_button.clicked.connect(self.list_ascend)
        self.export_ascend_button.clicked.connect(self.export_ascend_to_txt)

    def redraw_tree(self):
        self.scene.clear()
        self.draw_tree_recursive(self.tree.root, 400, 50, 300)

    def draw_tree_recursive(self, node, x, y, offset):
        if node:
            green_color = QColor('#228B22')

            circle = self.scene.addEllipse(x, y, 30, 30)
            circle.setBrush(green_color)

            text_item = self.scene.addText(str(node.data))
            text_item.setPos(x + 5, y + 5)

            if node.left:
                line = self.scene.addLine(x + 15, y + 30, x - offset + 15, y + 100)
                self.draw_tree_recursive(node.left, x - offset, y + 100, offset / 2)

            if node.right:
                line = self.scene.addLine(x + 15, y + 30, x + offset + 15, y + 100)
                self.draw_tree_recursive(node.right, x + offset, y + 100, offset / 2)

    def insert_node(self):
        value = self.insert_input.text()
        self.tree.insert(value)
        self.redraw_tree()
        self.insert_input.clear()

    def search_node(self):
        value = self.search_input.text()
        if self.tree.search(value):
            QMessageBox.information(self, "Search successfully", f"The value {value} is on the tree.")
        else:
            QMessageBox.warning(self, "Search failed", f"The value {value} is not on the tree.")
        self.search_input.clear()

    def delete_node(self):
        value = self.delete_input.text()
        self.tree.delete(value)
        self.redraw_tree()
        self.delete_input.clear()

    def list_ascend(self):
        ordered_list = self.tree.inorder_list()
        QMessageBox.information(self, "Ordered List", f"The elements in ascending order are: {ordered_list}")

    def export_ascend_to_txt(self):
        ordered_list = self.tree.inorder_list()
        try:
            with open("ordered_data.txt", "w") as file:
                for item in ordered_list:
                    file.write(str(item) + "\n")
            QMessageBox.information(self, "Export successful", "Data exported to ordered_data.txt successfully.")
        except Exception as e:
            QMessageBox.warning(self, "Export failed", f"An error occurred while exporting the data: {str(e)}")

if __name__ == "__main__":
    app = QApplication([])
    window = SearchTreeGUI()
    window.show()
    app.exec()
