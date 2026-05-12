import Database.database_manage as dbm

"""The trie will be populated on startup based on existing relationships (vendor / type) within the database
if the vendor doesn't yet exist, the user will supply the type, which will then be added to the DB.

Within the database, we can use an alias for the all the different vendor names as they appear on the statements
when the user sees a new vendor name, we can ask if this is a new vendor or belongs to an existing vendor and is just 
a different variant and should be an alias - the user can search for the vendor within the trie and if it's not there, we can 
add new"""

class TrieNodeVendor:
    def __init__(self):
        # 1 array slot for each character of the alphabet plus 1 for space character
        self.char_array = [None] * 27
        self.type = None
        self.vendor_id = None
        self.is_word = False

class VendorTrie():
    def __init__(self):
        # initiate root node
        self.root = TrieNodeVendor()

    def insert(self, key, type, vendor_id):
        #ensure all characters are in lowercase so indices are in range
        key = key.lower()
        cursor = self.root

        for character in key:
            # Index between 0 and 25 based on ASCII codes for lowercase letters
            index = ord(character) - ord("a")
            if (index < 0 or index > 25) and ord(character) != 32:
                return "Vendor name must only contain letters a - z"
            if ord(character) == 32:
                index = 26
            if cursor.char_array[index] is None:
                next_char = TrieNodeVendor()
                cursor.char_array[index] = next_char
                cursor = next_char
            else:
                cursor = cursor.char_array[index]

        cursor.type = type
        cursor.vendor_id = vendor_id
        cursor.is_word = True


             

    def search(self, key):
        #ensure all characters are in lowercase so indices are in range
        key = key.lower()
        cursor = self.root

        for character in key:
            # Index between 0 and 25 based on ASCII codes for lowercase letters
            index = ord(character) - ord("a")
            # need to handle this better for the multple elements returned
            if (index < 0 or index > 25) and ord(character) != 32:
                return "Vendor name must only contain letters a - z"
            # need to add an additional slot for space character
            if ord(character) == 32:
                index = 26
            if cursor.char_array[index] is None:
                return False, cursor.vendor_id, cursor.type
            cursor = cursor.char_array[index]
        return cursor.is_word, cursor.vendor_id, cursor.type



    def populate_trie_from_db(self):
        # Need to reset root
        all_vendors = dbm.get_vendors()
        for vendor in all_vendors:
            self.insert(vendor[1], vendor[2], vendor[0])