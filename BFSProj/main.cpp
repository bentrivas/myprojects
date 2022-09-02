#include <iostream>
#include <fstream>
#include <math.h>
#include <queue>
using namespace std;
struct qPos{//linked list
  int x;
  int y;
  qPos *prev;
};
int counterR = 0;//counts rows, will count ever character that isnt line break or space in the program
int counterC = 1;//amounts of rows is the amount of spaces + 1 because line breaks are counted, but last row in list does not have linebreak
queue<qPos> paff;
qPos start;//used later
qPos finish;//used later
int main() {
  ifstream is1("maze");//reads in file maze, counts width and height
  char c1;
  while(is1.get(c1)){
    cout<<" "<<c1;
    if(c1==45||c1==120||c1==115||c1==102){//only counts f s x and -
      counterR++;
    }
    else{
      counterC++;//counts line breaks
    }
  }
  char x[counterC][counterR/counterC];
  ifstream is2("maze");//read in file maze, makes 2d array to display maze and eventually path
  char c2;
  int arrC = 0;
  while(is2.get(c2)){
    if(c2==45||c2==120||c2==115||c2==102){
      x[arrC/(counterR/counterC)][arrC%(counterR/counterC)] = c2;
      arrC++;
    }
  }
  int width = counterR/counterC;
  int height = counterC;
  cout<<endl;
  bool visited[counterC][counterR/counterC];
  for(int i=0; i<counterC; i++)
  {
    for(int j=0; j<counterR/counterC; j++)
    {
    //cout<<" "<<x[i][j]<<" ";
    visited[i][j]=false;
    if(x[i][j]==115){
      start.x=i;
      start.y=j;
      start.prev = NULL;
      visited[i][j] = true;
    }
    if(x[i][j]==102){
      finish.x=i;
      finish.y=j;
      finish.prev = NULL;
    }
    if(x[i][j]==120){
      visited[i][j] = true;
    }
    }
    //cout<<"\n";
  }
  //cout<<endl;
  /*for(int i=0; i<counterC; i++)
  {
    for(int j=0; j<counterR/counterC; j++)
    {
      cout<<visited[i][j];
    }
    cout<<endl;
  }*/
  cout<<endl<<"Start at ("<<start.x<<", "<<start.y<<")";
  cout<<endl<<"Finish at ("<<finish.x<<", "<<finish.y<<")";
  /**********************************************************/
  qPos *current;
  paff.push(start);
  while(!paff.empty()){
    current = &paff.front();
    paff.pop();
    if(current->x == finish.x && current->y == finish.y){
      cout<<endl<<"Found Path"<<endl;
      current=current->prev;
      while(current->prev!=NULL){
        x[current->x][current->y] = '0';
        current=current->prev;
      }
      for(int i=0; i<counterC; i++)
      {
        for(int j=0; j<counterR/counterC; j++)
        {
          cout<<x[i][j]<<" ";
        }
        cout<<endl;
      }
      break;
    }
    else{
      if((current->y+1<width)&&(!visited[current->x][current->y+1])){//right
      visited[current->x][current->y+1]=true;
      qPos temp;
      temp.x = current->x;
      temp.y = current->y+1;
      temp.prev=current;
      paff.push(temp);
      }
      if((current->y-1>=0)&&(!visited[current->x][current->y-1])){ //left
      visited[current->x][current->y-1]=true;
      qPos temp;
      temp.x = current->x;
      temp.y = current->y-1;
      temp.prev=current;
      paff.push(temp);
      }
      if((current->x-1>=0)&&(!visited[current->x-1][current->y])){ //up
      visited[current->x-1][current->y]=true;
      qPos temp;
      temp.x = current->x-1;
      temp.y = current->y;
      temp.prev=current;
      paff.push(temp);
      }
      if((current->x+1<height)&&(!visited[current->x+1][current->y])){//down
      visited[current->x+1][current->y]=true;
      qPos temp;
      temp.x = current->x+1;
      temp.y = current->y;
      temp.prev=current;
      paff.push(temp);
      }
    }
  }
}