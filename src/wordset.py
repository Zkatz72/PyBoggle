import random

class ElementNotFoundException(Exception):
    pass
class EmptyWordsetException(Exception):
    pass

def _is_prime(num):
    if num > 1:
        for i in range(2, num//2 + 1):
            if num%i == 0:
                return False

        else:
            return True
    return False

def _next_prime(current):
    num = current + 1
    while True:
        if _is_prime(num):
            return num
        num+=1
        

def polynomial_hash_function(s, base, mod):
    total = 0
    for i in range(len(s)):
        total *= base
        total += ord(s[i]) - ord('a') + 1
        total %= mod
        
    return total % mod

class Wordset: #uses a cuckoo hashmap
    _BASE_H1 = 37
    _BASE_H2 = 41
    
    def __init__(self, initial_capacity, eviction_threshold = 5):
        self._eviction_threshold = eviction_threshold
        self._capacity = initial_capacity
        self._table1 = [''] * self._capacity
        self._table2 = [''] * self._capacity
        self._word_count = 0


    def contains(self, s):
        hash1 = polynomial_hash_function(s, self._BASE_H1, self._capacity)
        hash2 = polynomial_hash_function(s, self._BASE_H2, self._capacity)
        return self._table1[hash1] == s or self._table2[hash2] == s

    def __contains__(self, s):
        return self.contains(s)
        
    def get_word_count(self):
        return self._word_count

    def get_capacity(self):
        return self._capacity

    def insert(self, s):

        if self.contains(s):
            return

        evictions = 0
        inserted_safely = False
        current_hash = polynomial_hash_function(s, self._BASE_H1, self._capacity)

        current_base = self._BASE_H1
        string_to_be_added = s

        while evictions < self._eviction_threshold and not inserted_safely:

            if current_base == self._BASE_H1 and self._table1[current_hash] != '':
                evictions += 1
                saved = self._table1[current_hash]
                self._table1[current_hash] = string_to_be_added
                current_hash = polynomial_hash_function(s, self._BASE_H2, self._capacity)
                string_to_be_added = saved
                current_base = self._BASE_H2

            elif current_base == self._BASE_H2 and self._table2[current_hash] != '':
                evictions += 1
                saved = self._table2[current_hash]
                self._table2[current_hash] = string_to_be_added
                current_hash = polynomial_hash_function(s, self._BASE_H1, self._capacity)
                string_to_be_added = saved
                current_base = self._BASE_H1

            else:

                if current_base == self._BASE_H1:
                    self._table1[current_hash] = string_to_be_added
                else:
                    self._table2[current_hash] = string_to_be_added

                inserted_safely = True

        if inserted_safely:
            self._word_count += 1
        else:
            self._resize()
            self.insert(string_to_be_added)

    def _resize(self):
        old_capacity = self._capacity
        self._capacity = _next_prime(2*self._capacity)
        old_table1 = self._table1
        old_table2 = self._table2
        self._table1 = [''] * self._capacity
        self._table2 = [''] * self._capacity
        self._word_count = 0
            
        for i in range(old_capacity):
            if old_table1[i] != '':
                self.insert(old_table1[i])
            if old_table2[i] != '':
                self.insert(old_table2[i])

    def remove(self, s):
        
        if not self.is_empty():
            hash1 = polynomial_hash_function(s, self._BASE_H1, self._capacity)
            hash2 = polynomial_hash_function(s, self._BASE_H2, self._capacity)
            if self._table1[hash1] == s:
                self._table1[hash1] = ''
            elif self._table2[hash2] == s:
                self._table2[hash2] = ''
            else:
                raise ElementNotFoundException(f'This word[\'{s}\'] is not in the wordset')
        else:
            raise EmptyWordsetException('Cannot remove from an empty wordset')
