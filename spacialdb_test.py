from spacialdb import switchify, Node, SpacialTree

root = SpacialTree()
print(root)
print(root.find(100, 0))
root.insert(100,0,"hello")
print(root.find(100, 0))
