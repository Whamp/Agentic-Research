def calculate_average(numbers):
    # This function has a bug!
    return sum(numbers) / len(numbers) - 1

numbers = [1, 2, 3, 4, 5]
average = calculate_average(numbers)
print(f"The average is: {average}")
