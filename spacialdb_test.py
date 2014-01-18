from spacialdb import switchify, Node, SpacialTree

root = SpacialTree()
print(root)
print(root.find(100, 0))
root.insert(100,0,"hello")
root.insert(100,0,"hello2")
root.insert(200,1,"hello")
print(root.find(100, 0))
print(root.find(100, 1))
print(root.find(101, 0))
print(root.find(200, 1))
root.remove(100,0,"hello")
print(root.find(100, 0))