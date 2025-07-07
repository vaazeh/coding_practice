#include<iostream>
using namespace std;


int main(int argc, char* argv[])
{
    if(argc >=2)
   { cout<<argc;
    }
     int i=0;
    while(i<argc){
        cout<<argv[i]<<endl;
        i++;

    }
}