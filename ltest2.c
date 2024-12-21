#include <stdio.h>

int main() {
    int sum = 0;

    // Use a for loop to sum the first 5 natural numbers
    for (int i = 1; i <= 5; i++) {
        sum += i;  // Add the current number to sum
    }

    // Print the result
    printf("The sum of the first 5 natural numbers is: %d\n", sum);

    return 0;
}
