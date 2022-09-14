from __future__ import annotations
import random


class Node:
    def __init__(self, item: int, left: Node = None, right: Node = None):
        self.item: int = item
        self.left: Node = left
        self.right: Node = right
        self.height = 1

    def getHeight(self) -> int:
        """ 获取当前节点的高度 """
        return self.height

    def setHeight(self):
        """ 设置当前节点高度 """
        self.height = max(self.getLeftHight(), self.getRightHight()) + 1

    def getLeftHight(self) -> int:
        """ 获取左子树的高度 """
        return self.left.height if self.left else 0

    def getRightHight(self) -> int:
        """ 获取右子树的高度 """
        return self.right.height if self.right else 0

    def getBalance(self) -> int:
        """ 获取平衡因子（左子树高度 - 右子树高度）"""
        return self.getLeftHight() - self.getRightHight()

    def add(self, node):
        """ 添加节点 """
        if not node:
            return

        if node.item < self.item:
            # 小于当前值，进入左子树
            if not self.left:
                self.left = node
            else:
                self.left.add(node)
        else:
            # 大于等于当前值，进入右子树
            if not self.right:
                self.right = node
            else:
                self.right.add(node)

        self.setHeight()

        # 检查是否平衡
        if self.left and self.getBalance() > 1:
            # 左子树比右子树的高度大于 1，进行右旋转
            if self.left.right and self.left.getBalance() < 0:
                # 左子节点的右子树高度大于左子节点的左子树高度，则先对左节点进行左旋转
                self.left.leftRotate()
            self.rightRotate()
        elif self.right and self.getBalance() < -1:
            # 右子树比左子树的高度大于 1，进行左旋转
            if self.right.left and self.right.getBalance() > 0:
                # 右子节点的左子树高度大于右子节点的右子树高度，则先对右节点进行右旋转
                self.right.rightRotate()
            self.leftRotate()

    def rightRotate(self):
        """ 左子树比右子树的高度大于 1，进行右旋转 """
        # 1. 创建新节点, 新节点的值等于当前节点的值
        newright = Node(self.item)
        # 2. 把当前节点的右子树设置为新节点的右子树
        newright.right = self.right
        # 3. 把当前节点的左节点的右子树设置为新节点的左子树
        newright.left = self.left.right
        # 4. 将当前节点的值换成左子节点的值
        self.item = self.left.item
        # 5. 将当前节点的左子节点的左树设置为当前节点的左树
        leftnode = self.left
        self.left = self.left.left
        # 6. 删除原左子节点
        del leftnode
        # 7. 将新节点设置为当前节点的右子节点
        self.right = newright
        newright.setHeight()
        self.setHeight()


    def leftRotate(self):
        """ 右子树比左子树的高度大于 1，进行左旋转 """
        # 1. 创建新节点, 新节点的值等于当前节点的值
        newleft = Node(self.item)
        # 2. 把当前节点的左子树设置为新节点的左子树
        newleft.left = self.left
        # 3. 把当前节点的右节点的左子树设置为新节点的右子树
        newleft.right = self.right.left
        # 4. 将当前节点的值换成右子节点的值
        self.item = self.right.item
        # 5. 将当前节点的右子节点的右树设置为当前节点的右树
        rightnode = self.right
        self.right = self.right.right
        # 6. 删除原右子节点
        del rightnode
        # 7. 将新节点设置为当前节点的左子节点
        self.left = newleft
        newleft.setHeight()
        self.setHeight()

    def search(self, item: int) -> Node | None:
        """ 查找节点 """
        if self.item == item:
            return self
        elif item < self.item:
            if not self.left:
                return None
            else:
                return self.left.search(item)
        else:
            if not self.right:
                return None
            else:
                return self.right.search(item)

    def searchParent(self, item: int) -> Node | None:
        """ 查找父节点 """
        if item < self.item:
            if not self.left:
                return None
            elif item == self.left.item:
                return self
            else:
                return self.left.searchParent(item)
        else:
            if not self.right:
                return None
            elif item == self.right.item:
                return self
            else:
                return self.right.searchParent(item)

    def searchWithParent(self, item: int) -> (Node | None, Node | None):
        """ 查找节点并返回该节点与父节点 """
        if item < self.item:
            if not self.left:
                return None, None
            elif item == self.left.item:
                return self.left, self
            else:
                return self.left.searchWithParent(item)
        else:
            if not self.right:
                return None, None
            elif item == self.right.item:
                return self.right, self
            else:
                return self.right.searchWithParent(item)

    def getmin(self) -> Node:
        """ 获取最小值节点 """
        if self.left:
            return self.left.getmin()
        else:
            return self

    def getmax(self) -> Node:
        """ 获取最大值节点 """
        if self.right:
            return self.right.getmax()
        else:
            return self

    def getminWithParent(self) -> (Node | None, Node | None):
        """ 获取最小值节点 """
        if not self.left:
            return self, None
        elif not self.left.left:
            return self.left, self
        else:
            return self.left.getminWithParent()

    def delete(self, item: int, parent: Node | None):
        """ 删除节点， 按值删除 """
        if item < self.item:
            if not self.left:
                # 未命中
                return
            self.left.delete(item, self)
        elif item > self.item:
            if not self.right:
                # 未命中
                return
            self.right.delete(item, self)
        else:
            # 命中
            if not (self.left and self.right):
                if parent:
                    if parent.left is self:
                        parent.left = (self.left if self.left else self.right)
                    else:
                        parent.right = (self.left if self.left else self.right)
                    return
                else:
                    # 当前节点是根节点
                    if self.left:
                        self.item = self.left.item
                        self.left = None
                    elif self.right:
                        self.item = self.right.item
                        self.right = None
            else:
                if self.getBalance() > 0:
                    # 左子树高于右子树高度
                    maxnode = self.left.getmax()  # 获取左子树最大值
                    self.item = maxnode.item
                    self.left.delete(maxnode.item, self)
                else:
                    # 右子树高于或等于左子树高度
                    minnode = self.right.getmin()  # 获取右子树最小值
                    self.item = minnode.item
                    self.right.delete(minnode.item, self)

        self.setHeight()

        # 检查是否平衡
        if self.left and self.getBalance() > 1:
            # 左子树比右子树的高度大于 1，进行右旋转
            if self.left.right and self.left.getBalance() < 0:
                # 左子节点的右子树高度大于左子节点的左子树高度，则先对左节点进行左旋转
                self.left.leftRotate()
            self.rightRotate()
        elif self.right and self.getBalance() < -1:
            # 右子树比左子树的高度大于 1，进行左旋转
            if self.right.left and self.right.getBalance() > 0:
                # 右子节点的左子树高度大于右子节点的右子树高度，则先对右节点进行右旋转
                self.right.rightRotate()
            self.leftRotate()


    def preorder(self, node):
        """ 前序遍历二叉树 """
        if not node:
            return

        print(node, end=", ")
        self.preorder(node.left)
        self.preorder(node.right)

    def inorder(self, node):
        """ 中序遍历二叉树 """
        if not node:
            return

        self.inorder(node.left)
        print(node, end=", ")
        self.inorder(node.right)

    def __str__(self):
        return f"{self.item}"


class AVLTree:
    def __init__(self, l: list = None):
        self.root: Node | None = None
        for i in l:
            self.add(Node(i))

    def getHight(self) -> int:
        if not self.root:
            return 0
        else:
            return self.root.getHeight()

    def add(self, node: Node):
        """ 增加节点 """
        if not self.root:
            self.root = node
        else:
            self.root.add(node)

    def search(self, item: int) -> Node | None:
        """ 查找节点 """
        if not self.root:
            return None
        else:
            return self.root.search(item)

    def searchParent(self, item: int) -> Node | None:
        """ 查找父节点 """
        if not self.root:
            return None
        else:
            return self.root.searchParent(item)

    def searchWithParent(self, item: int) -> (Node | None, Node | None):
        """ 查找节点并返回该节点与父节点 """
        if not self.root:
            return None, None
        if self.root.item == item:
            return self.root, None
        else:
            return self.root.searchWithParent(item)

    def delete(self, item: int):
        """ 删除节点(按值删除) """
        # cur, par = self.searchWithParent(item)
        # self.deleteNode(cur, par)
        if self.root:
            self.root.delete(item, None)

    def deleteNode(self, cur, par):
        """ 删除节点(按节点删除) """
        if cur:
            # 当前节点存在
            if not (cur.left and cur.right):
                # 当前节点没有子节点(当前节点是叶子节点)或只有一个子节点
                if par:
                    # 当前节点有父节点
                    if cur == par.left:
                        par.left = (cur.left if cur.left else cur.right)
                    else:
                        par.right = (cur.left if cur.left else cur.right)
                else:
                    # 当前节点没有父节点(当前节点是根节点)
                    self.root = (cur.left if cur.left else cur.right)
                del cur
            else:
                # 当前节点有两个子节点
                # 找到当前节点的后驱节点，即右子树的最小值节点，删除后驱节点，并用该节点的值替换当前节点的值
                post, postpar = cur.right.getminWithParent()
                cur.item = post.item
                self.deleteNode(post, postpar if postpar else cur)

    def preshow(self):
        """ 前序遍历 """
        if self.root:
            self.root.preorder(self.root)

    def inshow(self):
        """ 中序遍历

        BST 的中序遍历恰好是从小到大
        """
        if self.root:
            self.root.inorder(self.root)


def main():
    # l = [random.randint(1, 100) for _ in range(10)]
    l = [10, 1, 41, 56, 98, 70, 84, 27, 56, 4]
    # l = [8, 5, 9, 4, 6, 7]
    # l = [3, 1, 5]
    # l = [8, 9, 6, 7, 5, 4]
    print(l)
    bst = AVLTree(l)
    print("前序遍历")
    bst.preshow()
    print("\n中序遍历")
    bst.inshow()

    # 添加节点
    # bst.add(Node(80))
    # print("\n前序遍历")
    # bst.preshow()
    # print("\n中序遍历")
    # bst.inshow()
    #
    # print("\n查找")
    # n = bst.search(50)
    # print(n)
    #
    # print("查找父节点")
    # n = bst.searchParent(10)
    # print(n)

    print("删除子节点")
    bst.delete(10)
    print("\n前序遍历")
    bst.preshow()
    print("\n中序遍历")
    bst.inshow()
    #
    # bst.delete(5)
    # print("\n前序遍历")
    # bst.preshow()
    # print("\n中序遍历")
    # bst.inshow()
    print("\n平衡二叉树的高度")
    h = bst.getHight()
    print(h)


if __name__ == '__main__':
    main()
