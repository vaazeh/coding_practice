#include <iostream>
#include <string>
using namespace std;

int evaluate(string expr, int& i);

int parseNumber(string expr, int& i) {
    int num = 0;
    while (i < expr.length() && expr[i] >= '0' && expr[i] <= '9') {
        num = num * 10 + (expr[i] - '0');
        i++;
    }
    return num;
}

int parseFactor(string expr, int& i) {
    if (expr[i] == '(') {
        i++; // skip '('
        int val = evaluate(expr, i);
        if (i < expr.length() && expr[i] == ')') i++; // skip ')'
        return val;
    } else {
        return parseNumber(expr, i);
    }
}

int parseTerm(string expr, int& i) {
    int val = parseFactor(expr, i);
    while (i < expr.length()) {
        if (expr[i] == '*') {
            i++;
            val *= parseFactor(expr, i);
        } else if (expr[i] == '/') {
            i++;
            int right = parseFactor(expr, i);
            if (right == 0) {
                cout << "Error: Division by zero!" << endl;
                exit(1);
            }
            val /= right;
        } else {
            break;
        }
    }
    return val;
}

int evaluate(string expr, int& i) {
    int val = parseTerm(expr, i);
    while (i < expr.length()) {
        if (expr[i] == '+') {
            i++;
            val += parseTerm(expr, i);
        } else if (expr[i] == '-') {
            i++;
            val -= parseTerm(expr, i);
        } else {
            break;
        }
    }
    return val;
}

string insertMultiplication(string expr) {
    string result = "";
    for (int j = 0; j < expr.length(); j++) {
        result += expr[j];
        if (j < expr.length() - 1) {
            char curr = expr[j];
            char next = expr[j + 1];
            bool needStar = ((curr >= '0' && curr <= '9') || curr == ')') && next == '(';
            if (needStar) {
                result += '*';
            }
        }
    }
    return result;
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        cout << "Usage: ./t5.exe \"expression\"\n";
        return 1;
    }

    string expr = argv[1];
    expr = insertMultiplication(expr);

    int pos = 0;
    int result = evaluate(expr, pos);

    cout << "Result: " << result << endl;
    return 0;
}
