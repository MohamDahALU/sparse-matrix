#!/usr/bin/python3

import sys


def load_sparse_matrix(file_path):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()

        if len(lines) < 2:
            raise ValueError("Missing rows/cols header.")

        rows = int(lines[0].split('=')[1].strip())
        cols = int(lines[1].split('=')[1].strip())

        matrix = {}
        for line in lines[2:]:
            line = line.strip()
            if not line:
                continue
            try:
                row, col, val = eval(line)
                matrix[(row, col)] = val
            except:
                raise ValueError(f"Invalid line: {line}")
        
        return matrix, (rows, cols)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise RuntimeError(f"Error reading {file_path}: {e}")


def save_sparse_matrix(matrix, shape, file_path):
    rows, cols = shape
    try:
        with open(file_path, 'w') as f:
            f.write(f"rows={rows}\n")
            f.write(f"cols={cols}\n")
            for (r, c), v in sorted(matrix.items()):
                if v != 0:
                    f.write(f"({r}, {c}, {v})\n")
    except Exception as e:
        raise RuntimeError(f"Error writing to {file_path}: {e}")


def multiply_sparse_matrices(A, A_shape, B, B_shape):
    """
    Multiplies two sparse matrices efficiently.
    """
    a_rows, a_cols = A_shape
    b_rows, b_cols = B_shape

    # Check if matrices can be multiplied
    if a_cols != b_rows:
        raise ValueError("Incompatible shapes for multiplication.")

    # Group B entries by row index for efficient lookup during multiplication
    # This avoids having to scan all entries of B for each entry of A
    B_by_row = {}
    for (r, c), val in B.items():
        if r not in B_by_row:
            B_by_row[r] = []
        B_by_row[r].append((c, val))

    # Compute the product matrix
    result = {}
    for (a_r, a_c), a_val in A.items():
        # Only process if there are corresponding entries in B
        if a_c in B_by_row:
            # For each corresponding B entry, calculate the product contribution
            for b_c, b_val in B_by_row[a_c]:
                key = (a_r, b_c)
                # Accumulate products into the result matrix
                result[key] = result.get(key, 0) + a_val * b_val

    return result, (a_rows, b_cols)


def add_or_subtract_sparse_matrices(A, A_shape, B, B_shape, op):
    """
    Performs addition or subtraction on two sparse matrices.
    """
    if A_shape != B_shape:
        raise ValueError("Matrix dimensions must match for addition or subtraction.")

    result = {}
    # Get the union of all keys from both matrices
    keys = set(A.keys()) | set(B.keys())

    for key in keys:
        val_a = A.get(key, 0)  # Default to 0 if key not in A
        val_b = B.get(key, 0)  # Default to 0 if key not in B

        if op == 'add':
            result[key] = val_a + val_b
        elif op == 'subtract':
            result[key] = val_a - val_b

        # Remove zero entries to maintain sparsity
        if result[key] == 0:
            del result[key]

    return result, A_shape


def main():
    """
    Main function that parses command line arguments and executes matrix operations.
    """
    # Use command sys.argv rather than input() for ease of testing 
    if len(sys.argv) != 5:
        print("Usage: sparse_matrix_calc <file1> <file2> <operation> <result_file>")
        print("operation: add | subtract | multiply")
        sys.exit(1)

    # Parse command line arguments
    file_a, file_b, operation, output_file = sys.argv[1:]

    try:
        # Load input matrices
        A, A_shape = load_sparse_matrix(file_a)
        B, B_shape = load_sparse_matrix(file_b)

        # Perform the requested operation
        if operation == "multiply":
            result, shape = multiply_sparse_matrices(A, A_shape, B, B_shape)
        elif operation == "add":
            result, shape = add_or_subtract_sparse_matrices(A, A_shape, B, B_shape, op="add")
        elif operation == "subtract":
            result, shape = add_or_subtract_sparse_matrices(A, A_shape, B, B_shape, op="subtract")
        else:
            raise ValueError("Invalid operation. Use add, subtract, or multiply.")

        save_sparse_matrix(result, shape, output_file)
        print(f"Result written to: {output_file}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
