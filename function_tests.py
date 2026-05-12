import Database.database_manage as dbm
import vendor_trie as vt

test_trie = vt.VendorTrie()

#test_trie.insert("Justin", "Groceries", 1)
#test_trie.insert("Ghost Mix", "Groceries", 2)
test_trie.insert("Chelsea", "Groceries", 3)
#test_trie.insert("Toemas", "Groceries", 4)
test_trie.insert("Chex Mix", "Groceries", 5)
#test_trie.insert("Nova", "Groceries", 6)

#print(test_trie.search("Ghost Mix"))
print(test_trie.search("Chelsea"))
print(test_trie.search("Chex Mix"))
#print(test_trie.search("TOemas"))
#print(test_trie.search("HUNGRY"))