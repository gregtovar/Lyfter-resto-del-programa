#
# Ejercicio 7.0: Version 2 - fix bugs
# Cree una función que acepte una lista de números y retorne una lista con
# los números primos de la misma.
#

#
# Function Declaration
#
# First we need to know if the number is prime:
#
def is_it_prime(num_param):
    if num_param < 2:                   #is N is less than 2 is not prime
        return False;                   # not prime
    for i in range(2, num_param):        #if bigger than 2, then we need to iterate and try to figure it out if prime
        if num_param % i == 0:
            return False;
    return True;                        # Otherwse is prime
#
#
#
def return_list_with_primes(list_param):                    # This function returns a list of prime nunbers only
    local_list = [];                                        # declare a local list
    len_list = len(list_param);                             # how long in th list
    for number_index in range(1,len_list):                  # iterate the list looking for primes
        if is_it_prime(list_param[number_index]):           #call the is_prime function
            local_list.append(list_param[number_index]);    # if Yes, add the prime number to the local list
    return local_list;                                      #return the created list
#
#  Variables
#  
global_list_of_numbers = [1, 4, 6, 7, 13, 9, 67, 113];      # declare list of INITIAL numbers
global_list_of_prime_numbers = [];                          # declare list of PRIME nunbers - emty for now

#
#  Main Program
#  
print();
#
# Call the function
#
global_list_of_prime_numbers= return_list_with_primes(global_list_of_numbers);
print();
print("------ OUTPUT--------"); 
print(global_list_of_numbers, "→ ",global_list_of_prime_numbers);
print();
print("------ END OF OUTPUT--------");                     
print();
#
#  End of Main Program
#  