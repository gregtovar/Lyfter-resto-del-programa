# Trying to add different data Types
#
# Variables definition
int_variable = 1;
float_var = 3.44;
boolean_var1 = False;
boolean_var2 = True;
string1 = "This is string number 1";
string2 = "This is string number 2";
list1 = [1,2,3,4,5,6,7,8,9];
list2 = [10,11,12];
#
# Operations
#
print(string1+string2);
print(string1 + int_variable);  #does not work - gives error
print(int_variable + string1); #does not work - gives error
print(list1+list2);
print(string1+list1);   #does not work
print(float_var+int_variable); 
print(boolean_var1 + boolean_var2); #Returns 1

#end

