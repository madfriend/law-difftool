#include <iostream>
#include <fstream>
#include <cstring>
#include <string>

using namespace std;

string change(string s, string a, string b){
   size_t found2=-1;
   size_t found = 0;
   size_t found3=0;   

   while (s.find (".", found3)!=string::npos){
    found=s.find(a, found2+1);
    found2=s.find(b, found+1);
    found3=s.find(".", found+1);
 
     while (found3<found2){
      s.replace(found3, 1, "~");
      cout <<s <<endl;
      found3 = s.find(".",found3+1);
    }
   }
return s;
}

int main (int argc, char* argv[]){
 for(int i=1; i < argc; i++){
  fstream f;
  f.open (argv[i]);
  string s;

  if (!f.is_open())
   cout << "error" << endl;
  		
  while (!f.eof()){
   getline(f,s);
   change(change(s,"«","»"),"(",")");
  }

  cout << s << endl;
 }
}


