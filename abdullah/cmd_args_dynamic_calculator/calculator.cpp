#include <cstdio>
#include <iostream>
#include<cmath>
using namespace std;
void simple()
{
	float a,b;
	char op;
	cout << "Enter expression (e.g., 3 + 4): ";
    cin >> a >> op >> b;
    switch (op)
    {
    	case '+' :cout<<"Result:"<<a+b<<endl;
    	break;
    	case '-':cout<<"Result:"<<a-b<<endl;
    	break;
    	case '*':cout<<"Result:"<<a*b<<endl;
    	break;
    	case '/':
    		if(a!=0)
    		cout<<"Result:"<<a/b<<endl;
    		else
    		cout<<"Error: Division by zero!";
    		break;
    		default:
    			cout<<"invalid value";
    		
    	
	}
}
void scientific()
{
	int choice;
	float x;
	cout << "Scientific Mode: "<<endl<<" 1.Square Root"<<endl<<"2. Power"<<endl<<"3. Logarithm"<<endl<<"Choose an option: ";
    cin >> choice;
    switch (choice) {
        case 1: 
            cout << "Enter number: ";
            cin >> x;
            cout << "Square Root: " << sqrt(x) << endl;
            break;
        case 2: {
            double y;
            cout << "Enter base and exponent: ";
            cin >> x >> y;
            cout << "Result: " << pow(x, y) << endl;
            break;
        }
        case 3:
            cout << "Enter number: ";
            cin >> x;
            cout << "Logarithm: " << log(x) << endl;
            break;
        default: cout << "Invalid choice!" << endl;
    }
}
void logical()
{
	int a,b;
	 cout << "Enter two binary numbers: ";
    cin >> a >> b;
    cout << "AND: " << (a & b) << " OR: " << (a | b) << " XOR: " << (a ^ b) << endl;
}
int main()
{

int mode;
while(true){

cout << endl<<"Select Mode: \n1. Simple\n2. Scientific\n3. Logical\nChoose: ";
    cin >> mode;
    if(mode==0){
    	cout<<"Exit to this program";
    	break;
	}
    
    switch (mode) {
        case 1: simple(); break;
        case 2: scientific(); break;
        case 3: logical(); break;
        default: cout << "Invalid mode!" << endl;
    }
}
}
