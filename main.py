class MemoryManager:
    def __init__(self, total_memory):
        self.total_memory = total_memory
        self.allocated_blocks = []  # List of (start, size) tuples
        self.free_blocks = [(0, total_memory)]  # List of (start, size) tuples

    def allocate(self, size):
        # Simple first-fit allocation
        for i, (start, block_size) in enumerate(self.free_blocks):
            if block_size >= size:
                self.allocated_blocks.append((start, size))
                self.free_blocks[i] = (start + size, block_size - size)
                if self.free_blocks[i][1] == 0:
                    del self.free_blocks[i]
                return start
        return -1  # Allocation failed

    def deallocate(self, address):
        # Find and remove the allocated block
        for i, (start, size) in enumerate(self.allocated_blocks):
            if start == address:
                self.allocated_blocks.pop(i)
                self.free_blocks.append((start, size))
                self.free_blocks.sort()  # Simple merge could be added
                return True
        return False

    def display_memory(self):
        print("Allocated blocks:", self.allocated_blocks)
        print("Free blocks:", self.free_blocks)

if __name__ == "__main__":
    mm = MemoryManager(100)  # 100 units of memory
    print("Initial memory:")
    mm.display_memory()
    
    addr1 = mm.allocate(20)
    print(f"Allocated 20 at {addr1}")
    mm.display_memory()
    
    addr2 = mm.allocate(30)
    print(f"Allocated 30 at {addr2}")
    mm.display_memory()
    
    mm.deallocate(addr1)
    print(f"Deallocated {addr1}")
    mm.display_memory()