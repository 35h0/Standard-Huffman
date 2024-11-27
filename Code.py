import heapq
import os
from collections import Counter, defaultdict

# Node class for Huffman Tree
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # Define comparison for priority queue
    def __lt__(self, other):
        return self.freq < other.freq

# Build the Huffman Tree
def build_huffman_tree(text):
    frequency = Counter(text)
    priority_queue = [Node(char, freq) for char, freq in frequency.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)

    return priority_queue[0] if priority_queue else None

# Generate Huffman codes
def generate_codes(node, prefix="", code_map=None):
    if code_map is None:
        code_map = {}

    if node:
        if node.char is not None:
            code_map[node.char] = prefix
        generate_codes(node.left, prefix + "0", code_map)
        generate_codes(node.right, prefix + "1", code_map)
    
    return code_map

# Encode text using Huffman codes
def huffman_encode(text, code_map):
    return ''.join(code_map[char] for char in text)

# Decode Huffman encoded data
def huffman_decode(encoded_data, root):
    decoded_text = []
    node = root
    for bit in encoded_data:
        node = node.left if bit == '0' else node.right
        if node.char is not None:
            decoded_text.append(node.char)
            node = root

    return ''.join(decoded_text)

# Pad encoded text to make its length a multiple of 8
def pad_encoded_text(encoded_text):
    extra_padding = 8 - len(encoded_text) % 8
    for _ in range(extra_padding):
        encoded_text += "0"

    padded_info = "{0:08b}".format(extra_padding)
    return padded_info + encoded_text

# Remove padding from encoded text
def remove_padding(padded_encoded_text):
    padded_info = padded_encoded_text[:8]
    extra_padding = int(padded_info, 2)
    return padded_encoded_text[8:-extra_padding]

# Convert encoded text to bytes
def get_byte_array(padded_encoded_text):
    if len(padded_encoded_text) % 8 != 0:
        raise ValueError("Encoded text is not properly padded")

    byte_array = bytearray()
    for i in range(0, len(padded_encoded_text), 8):
        byte = padded_encoded_text[i:i+8]
        byte_array.append(int(byte, 2))

    return byte_array

# Save compressed file
def save_compressed_file(output_path, padded_encoded_text):
    byte_array = get_byte_array(padded_encoded_text)
    with open(output_path, 'wb') as file:
        file.write(byte_array)

# Compress file
def compress(input_path, output_path):
    with open(input_path, 'r') as file:
        text = file.read().rstrip()

    root = build_huffman_tree(text)
    code_map = generate_codes(root)
    encoded_text = huffman_encode(text, code_map)
    padded_encoded_text = pad_encoded_text(encoded_text)

    save_compressed_file(output_path, padded_encoded_text)
    print(f"File compressed and saved to {output_path}")

    return root, code_map

# Decompress file
def decompress(input_path, output_path, root):
    with open(input_path, 'rb') as file:
        bit_string = ""
        byte = file.read(1)
        while byte:
            byte = ord(byte)
            bits = bin(byte)[2:].rjust(8, '0')
            bit_string += bits
            byte = file.read(1)

    encoded_text = remove_padding(bit_string)
    decoded_text = huffman_decode(encoded_text, root)

    with open(output_path, 'w') as file:
        file.write(decoded_text)
    print(f"File decompressed and saved to {output_path}")

# Main
if __name__ == "__main__":
    input_file = "input.txt"
    compressed_file = "compressed.huff"
    decompressed_file = "decompressed.txt"

    root, code_map = compress(input_file, compressed_file)
    decompress(compressed_file, decompressed_file, root)
