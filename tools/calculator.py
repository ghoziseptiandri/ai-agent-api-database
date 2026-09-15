def calculate(a: float, b: float, operation: str) -> float:

    #print("🔧 Calculator tool called:")
    #print(f"{operation}")
    #print()

    if operation == "add":
        return a + b

    if operation == "subtract":
        return a - b

    if operation == "multiply":
        return a * b

    if operation == "divide":
        if b == 0:
            raise ValueError("Denominator cannot be zero.")
        return a / b

    raise ValueError(f"Unknown operation: {operation}")