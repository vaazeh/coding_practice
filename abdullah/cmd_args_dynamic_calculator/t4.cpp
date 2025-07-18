#include <iostream>
#include <string>
using namespace std;

enum Operator {
    Add,
    Sub,
    Mul,
    Div,
    Invalid
};

Operator getOperator(char op) {
    if (op == '+') return Add;
    if (op == '-') return Sub;
    if (op == '*') return Mul;
    if (op == '/') return Div;
    return Invalid;
}


int apply(int left, int right, Operator op) {
    switch(op) {
        case Add: return left + right;
        case Sub: return left - right;
        case Mul: return left * right;
        case Div:
            if (right != 0)
                return left / right;
            else {
                cout << "Error: Division by zero!" << endl;
                exit(1);
            }
        default:
            cout << "Invalid operation!" << endl;
            exit(1);
    }
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        cout << "Usage: ./t4 \"3+2*4-1\"\n";
        return 1;
    }

    string input = argv[1];
    string number = "";
    int result = 0;
    Operator currentOp = Add; 

    for (int i = 0; i < input.length(); i++) {
        char ch = input[i];

        if (isdigit(ch)) {
            number += ch;
        } else {
            int num = stoi(number);  
            result = apply(result, num, currentOp);  
            number = "";  
            currentOp = getOperator(ch);  
        }
    }

   
    if (!number.empty()) {
        int num = stoi(number);
        result = apply(result, num, currentOp);
    }

    cout << "Result: " << result << endl;
    return 0;
}
