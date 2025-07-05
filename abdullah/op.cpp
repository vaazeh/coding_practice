#include <iostream>
using namespace std;

enum class opreatorType {
    IntegerAdd,
    IntegerSub,
    Integermul,
    Integerdiv,
};


void performopreators(opreatorType type, int left_op, int right_op) {
    switch (type) {
        case opreatorType::IntegerAdd:
            cout << "Integer Addition: " << left_op + right_op << endl;
            break;
        case opreatorType::IntegerSub:
            cout << "Integer Subtraction: " << left_op - right_op << endl;
            break;
             case opreatorType::Integermul:
            cout << "Integer Multiplication: " << left_op * right_op << endl;
            break;
        case opreatorType::Integerdiv:
       if(right_op!=0){
            cout << "Integer Division: " << left_op / right_op << endl;
       }
       else
       cout<<"this is not possible";
            break;
            default:
            cout<<"invalid value";
    }
}

int main() {
    int left_op, right_op;
    cout << "Enter two integers: ";
    cin >> left_op >> right_op;
    opreatorType type = opreatorType::IntegerAdd; 
    performopreators(type, left_op, right_op);

    return 0;
}
