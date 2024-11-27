import heapq
from collections import defaultdict

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def calculate_frequencies(text):
    frequencies = defaultdict(int)
    for char in text:
        frequencies[char] += 1
    return frequencies

def build_huffman_tree(frequencies):
    priority_queue = [HuffmanNode(char, freq) for char, freq in frequencies.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        node1 = heapq.heappop(priority_queue)
        node2 = heapq.heappop(priority_queue)
        merged = HuffmanNode(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        heapq.heappush(priority_queue, merged)

    return priority_queue[0]

def generate_huffman_codes(root):
    codes = {}

    def traverse(node, code):
        if node is None:
            return
        if node.char is not None:
            codes[node.char] = code
        traverse(node.left, code + "0")  # Go left: append "0"
        traverse(node.right, code + "1")  # Go right: append "1"

    traverse(root, "")
    return codes

def encode_text(text, codes):
    encoded_text = "".join(codes[char] for char in text)
    return encoded_text

def decode_text(encoded_text, root):
    decoded_text = []
    current_node = root
    for bit in encoded_text:
        current_node = current_node.left if bit == "0" else current_node.right
        if current_node.char is not None:
            decoded_text.append(current_node.char)
            current_node = root  # Reset to root for the next character
    return "".join(decoded_text)

def save_to_file(filename, content):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)

def read_from_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()

def huffman_compression(input_file, output_file):
    text = read_from_file(input_file)
    frequencies = calculate_frequencies(text)
    root = build_huffman_tree(frequencies)
    codes = generate_huffman_codes(root)
    encoded_text = encode_text(text, codes)

    # Save the Huffman codes and the encoded text (binary string) in the output file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("Huffman codes for each character:\n")
        for char, code in codes.items():
            file.write(f"{char}: {code}\n")
        
        file.write("\nEncoded Text (Binary):\n")
        file.write(encoded_text)
    
    return root, encoded_text, codes

def huffman_decompression(output_file, root, encoded_text, codes):
    # Decode the encoded text back to original characters
    decoded_text = decode_text(encoded_text, root)

    # Save the decompressed data (original text) in the same output file
    with open(output_file, "a", encoding="utf-8") as file:
        file.write("\nDecoded Text (Decompressed):\n")
        file.write(decoded_text)

# File paths
input_file = "D:/Data compression/second assignment/input.txt"  
output_file = "D:/Data compression/second assignment/output.txt"  

# Compress the data
root, encoded_text, codes = huffman_compression(input_file, output_file)

# Decompress the encoded data and append it to the same output file
huffman_decompression(output_file, root, encoded_text, codes)
