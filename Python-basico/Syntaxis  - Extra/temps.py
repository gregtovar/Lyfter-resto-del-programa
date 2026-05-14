#
# Temperatures App
#

#
# Vars
#
celsius = 0.00;
fahrenheit = 0.00;
kelvin = 0.00;

celsius = float(input("Enter temperature in Celsius: "));
 
fahrenheit = (celsius * 9/5) + 32;
kelvin = celsius + 273.15;
 
print(f"\nCelsius:    {celsius}°C");
print(f"Fahrenheit: {fahrenheit}°F");
print(f"Kelvin:     {kelvin}K");
print(f" ");
#
# End of program
#
