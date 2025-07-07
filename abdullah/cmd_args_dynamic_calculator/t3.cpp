#include <iostream>
#include <string>
using namespace std;

// Define enum
enum Operator {
    Add,
    Sub,
    Mul,
    Div,
    Invalid
};

// Function to map char to enum
Operator getOperator(char op) {
    if (op == '+') return Add;
    if (op == '-') return Sub;
    if (op == '*') return Mul;
    if (op == '/') return Div;
    return Invalid;
}

// Perform operation
void calculate(int left, int right, Operator op) {
    switch(op) {
        case Add:
            cout << "Addition of numbers is: " << (left + right) << endl;
            break;
        case Sub:
            cout << "Subtraction of numbers is: " << (left - right) << endl;
            break;
        case Mul:
            cout << "Multiplication of numbers is: " << (left * right) << endl;
            break;
        case Div:
            if (right != 0)
                cout << "Division of numbers is: " << (left / right) << endl;
            else
                cout << "Error: Division by zero!" << endl;
            break;
        default:
            cout << "Invalid operation!" << endl;
    }
}

int main(int argc, char* argv[]) {
    if (argc != 2) return 1;

    string input = argv[1];
    int i;
    char op_char;

    // Find operator
    for (i = 0; i < input.length(); i++) {
        if (input[i] == '+' || input[i] == '-' || input[i] == '*' || input[i] == '/') {
            op_char = input[i];
            break;
        }
    }

    // If operator not found
    if (i == input.length()) return 1;

    // Split input
    string left_str = input.substr(0, i);
    string right_str = input.substr(i + 1);

    int left = stoi(left_str);
    int right = stoi(right_str);

    // Map char to enum
    Operator op = getOperator(op_char);

    // Calculate
    calculate(left, right, op);

    return 0;
}
