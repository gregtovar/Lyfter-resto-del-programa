#
#  Discount calculator 
#
# Variables
price = 0.00;
discount_rate =0.00;
final_price = 0.00

# input price
price = float(input("Enter the product price in USD: "))
 
#logic
if price < 100:
    discount_rate = 0.02;4
else:
    discount_rate = 0.10;
 
discount = price * discount_rate;
final_price = price - discount;
 
#output
print(f"\nOriginal price:  ${price:.2f}");
print(f"Discount ({int(discount_rate * 100)}%):   -${discount:.2f}");
print(f"Final price:     ${final_price:.2f}");
print(f"\n");
 
 #
 # End of program 
 #