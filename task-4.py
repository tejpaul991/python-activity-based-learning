
def validate_dimension(value):
    """Validate that the dimension is a positive integer."""
    try:
        number = int(value)
        if number <= 0:
            raise ValueError("Dimension must be greater than zero.")
        return number
    except ValueError:
        raise ValueError(
            "Invalid input! Enter a positive whole number."
        )


def hollow_diamond(n):
    """Print a hollow diamond of height 2*n - 1."""
    print("\nHollow Diamond Pattern:\n")

    for i in range(1, 2 * n):
        # Distance from the widest middle row
        row = i if i <= n else 2 * n - i
        spaces = n - row

        if row == 1:
            print(" " * spaces + "*")
        else:
            inner_spaces = 2 * row - 3
            print(
                " " * spaces
                + "*"
                + " " * inner_spaces
                + "*"
            )


def numeric_pyramid(n):
    """Print a symmetric numerical pyramid."""
    print("\nSymmetric Numerical Pattern:\n")

    for i in range(1, n + 1):
        # Leading spaces for alignment
        print(" " * (n - i), end="")

        # Ascending sequence
        for j in range(1, i + 1):
            print(j, end="")

        # Descending sequence
        for j in range(i - 1, 0, -1):
            print(j, end="")

        print()


def main():
    print("===== ADVANCED NUMERIC PATTERN GENERATOR =====")
    print("1. Hollow Diamond")
    print("2. Symmetric Numerical Pyramid")

    choice = input("Choose a pattern (1 or 2): ").strip()

    if choice not in ("1", "2"):
        print("Invalid choice! Please select 1 or 2.")
        return

    try:
        n = validate_dimension(
            input("Enter the pattern dimension: ").strip()
        )

        if n > 100:
            print("Dimension too large! Please enter a value up to 100.")
            return

        if choice == "1":
            hollow_diamond(n)
        else:
            numeric_pyramid(n)

    except ValueError as error:
        print("Error:", error)


if __name__ == "__main__":
    main()
