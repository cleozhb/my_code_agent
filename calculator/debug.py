from pkg.calculator import Calculator

calculator = Calculator()

# Test basic logarithms
print("Testing basic logarithms:")
print(f"log 100 = {calculator.evaluate('log 100')}")  # Should be 2.0
print(f"ln 2.71828 = {calculator.evaluate('ln 2.71828')}")  # Should be ~1.0
print(f"log2 8 = {calculator.evaluate('log2 8')}")  # Should be 3.0

print("\nTesting expressions with logarithms:")
print(f"log 100 + 3 = {calculator.evaluate('log 100 + 3')}")  # Should be 5.0
print(f"3 + log 100 = {calculator.evaluate('3 + log 100')}")  # Should be 5.0

print("\nTesting multiple logarithms:")
print(f"log 100 + ln 2.71828 = {calculator.evaluate('log 100 + ln 2.71828')}")  # Should be ~3.0