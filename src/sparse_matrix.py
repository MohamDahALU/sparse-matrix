#!/usr/bin/python3

class SparseMatrix:
    """
    Represents a sparse matrix. Uses a dictionary to represent the matrix
    """

    def __init__(self, filename):
        """
        Reads a sparse matrix from a file.
        """
        try:
            with open(filename, "r") as file:
                try:
                    # Extract row and column dimensions from first two lines
                    rows, cols = [
                        int(file.readline().strip().split("=")[1]) for _ in range(2)
                    ]
                    self.rows = rows
                    self.cols = cols
                    matrix = {}
                    # Read each element line by line
                    for line in file:
                        if line.strip():
                            r, c, v = [int(x) for x in line.strip()[1:-1].split(",")]
                            # Skip if value is 0
                            if v != 0:
                                matrix[f"{r},{c}"] = v
                    self.matrix = matrix
                    # matrix is a dictionary with key format "row,col" and value as matrix value
                except ValueError:
                    raise ValueError("Input file has wrong format")
        except FileNotFoundError:
            raise FileNotFoundError(f"The file '{filename}' could not be found")


def perform_matrix_operation(matrix1, matrix2, operation):
    """
    Performs addition, subtraction, or multiplication of two matrices.
    """
    if matrix1.cols != matrix2.cols or matrix1.rows != matrix2.rows:
        raise ValueError("Matrices must have compatible dimensions.")

    result = {"rows": matrix1.rows, "cols": matrix1.cols, "matrix": {}}
    # Copy first matrix elements to result
    for k, v in matrix1.matrix.items():
        result["matrix"][k] = v
    # Apply operation with second matrix
    if operation == "add":
        for k, v in matrix2.matrix.items():
            newV = result["matrix"].get(k, 0) + v
            if (newV != 0):
                result["matrix"][k] = newV
            else:
                del result["matrix"][k]
    elif operation == "subtract":
        for k, v in matrix2.matrix.items():
            newV = result["matrix"].get(k, 0) - v
            if (newV != 0):
                result["matrix"][k] = newV 
            else:
                del result["matrix"][k]
    elif operation == "multiply":
        for k, v in matrix2.matrix.items():
            existing = result["matrix"].get(k, 1)
            result["matrix"][k] = existing * v
    
    # Remove zero elements to maintain sparsity
    result["matrix"] = {k: v for k, v in result["matrix"].items() if v != 0}
    return result


def save_matrix_to_file(matrix, output_file):
    """
    Saves the matrix in a file.
    """
    try:
        with open(output_file, "w") as file:
            file.write(f"rows={matrix['rows']}\n")
            file.write(f"cols={matrix['cols']}\n")

            # Write each non-zero element in the required format
            for k, v in matrix["matrix"].items():
                r, c = k.split(",")
                file.write(f"({r}, {c}, {v})\n")
    except IOError as e:
        raise IOError(f"Error writing to file '{output_file}': {e}")


def main():
    """
    Main function for handling user input and matrices operations.
    """
    try:
        # Get user input
        file1 = input("Input the path of the first file: ")
        file2 = input("Input the path of the second file: ")
        operation = (
            input("What operation do you want to perform [add, subtract, multiply]: ")
            or "add"
        )
        output_file = (
            input("What's the name of the output file: ") or f"matrix_{operation}.txt"
        )

        # Load matrices from files
        matrix1 = SparseMatrix(file1)
        matrix2 = SparseMatrix(file2)

        # Perform operation and save result
        if operation in ["add", "subtract", "multiply"]:
            result = perform_matrix_operation(matrix1, matrix2, operation)
            save_matrix_to_file(result, output_file)
        else:
            raise ValueError("Invalid operation")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
