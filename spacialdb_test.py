from spacialdb import switchify, Node, SpacialTree, SpacialDB

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



db = SpacialDB()
db.insert(100.0, 100.0, "test")
print(db.get_all(100.0,100.0))
db.insert(359.999, 0, "a")
db.insert(0.001, 0, "b")
print(db.get_all(0.0,0))