# SUPER SIMPLE EXAMPLE

print("="*50)
print("YOUR WAY - Using Global Variable")
print("="*50)

# Global variable
my_list = ["A", "B", "C"]

def check_first_item():
    # This function looks at the GLOBAL my_list
    print(f"First item is: {my_list[0]}")
    return my_list[0] == "A"

# Test 1
my_list = ["A", "B", "C"]
print(f"my_list = {my_list}")
result = check_first_item()
print(f"Is first item 'A'? {result}\n")  # True ✓

# Test 2
my_list = ["X", "Y", "Z"]  # Changed the global!
print(f"my_list = {my_list}")
result = check_first_item()  # Calling same function
print(f"Is first item 'A'? {result}\n")  # False ✗ - Different result!

print("⚠️  PROBLEM: Same function, different results!")
print("⚠️  Because my_list changed between calls!")


print("\n" + "="*50)
print("CORRECT WAY - Using Parameter")
print("="*50)

def check_first_item_correct(the_list):
    # This function uses the parameter you give it
    print(f"First item is: {the_list[0]}")
    return the_list[0] == "A"

# Test 1
list1 = ["A", "B", "C"]
print(f"Testing list1 = {list1}")
result = check_first_item_correct(list1)
print(f"Is first item 'A'? {result}\n")  # True ✓

# Test 2
list2 = ["X", "Y", "Z"]
print(f"Testing list2 = {list2}")
result = check_first_item_correct(list2)
print(f"Is first item 'A'? {result}\n")  # False ✓ - Expected!

# Test 1 AGAIN - still works!
print(f"Testing list1 again = {list1}")
result = check_first_item_correct(list1)
print(f"Is first item 'A'? {result}\n")  # True ✓ - Consistent!

print("✓ Each test uses its own list!")
print("✓ Results are predictable!")


print("\n" + "="*50)
print("YOUR ACTUAL SITUATION")
print("="*50)

# This is what you're doing:
Role_Info = []  # Global

def empath_ability():
    # Uses global Role_Info
    print(f"  Checking: {Role_Info}")

print("\nLoop iteration 1:")
Role_Info = ["Imp", "Spy", "Chef"]
print(f"Role_Info = {Role_Info}")
empath_ability()  # Sees ["Imp", "Spy", "Chef"]

print("\nLoop iteration 2:")
Role_Info = ["Empath", "Imp", "Spy"]  # Changed!
print(f"Role_Info = {Role_Info}")
empath_ability()  # Sees ["Empath", "Imp", "Spy"] - Different!

print("\n⚠️  The function sees different things each time!")


print("\n" + "="*50)
print("WHAT YOU SHOULD DO")
print("="*50)

def empath_ability_correct(role_info):
    # Uses parameter
    print(f"  Checking: {role_info}")

print("\nLoop iteration 1:")
role_info_v1 = ["Imp", "Spy", "Chef"]
print(f"Testing: {role_info_v1}")
empath_ability_correct(role_info_v1)

print("\nLoop iteration 2:")
role_info_v2 = ["Empath", "Imp", "Spy"]
print(f"Testing: {role_info_v2}")
empath_ability_correct(role_info_v2)

print("\n✓ Each iteration passes its own version!")
print("✓ No confusion!")