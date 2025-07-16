def input_matrix(n, name):
    print(f"Enter the elements of matrix {name} (row by row):")
    matrix = []
    for i in range(n):
        row = list(map(int, input(f"Row {i + 1}: ").split()))
        if len(row) != n:
            print(f"Error: Each row must have exactly {n} elements.")
            return None
        matrix.append(row)
    return matrix

def main():
    n = int(input("Enter the order of the matrices (n x n): "))
    print("Matrix X:")
    matrix_x = input_matrix(n, "X")
    if matrix_x is None:
        return
    print("Matrix Y:")
    matrix_y = input_matrix(n, "Y")
    if matrix_y is None:
        return

    print("\nMatrix X:")
    for row in matrix_x:
        print(row)
    print("\nMatrix Y:")
    for row in matrix_y:
        print(row)

if __name__ == "__main__":
    main()