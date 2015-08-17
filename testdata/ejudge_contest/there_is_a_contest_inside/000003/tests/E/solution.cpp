#include<iostream>

using namespace std;

int N;

int Rooms[105];

int K;

int M_R[105];
int M_T[105];
int M_C[105];

int main()
{
	int i, j;
	cin>>N;
	for(i=1;i<=N;++i)
		cin>>Rooms[i];
	cin>>K;
	for(i=1;i<=K;++i)
		cin>>M_R[i]>>M_T[i]>>M_C[i];

	int CurrTime=0;

	for(i=1;i<=N;++i)
	{
		int ThisRoomTime=0;
		while(Rooms[i]>0)
		{
			CurrTime+=Rooms[i];
			ThisRoomTime+=Rooms[i];
			Rooms[i]=0;
			for(j=1;j<=K;++j)
				if(M_T[j]<=CurrTime)
				{
					Rooms[M_R[j]]+=M_C[j];
					M_T[j]=1000000000;
					M_R[j]=0;
					M_C[j]=0;
				}
		}
		cout<<ThisRoomTime<<" ";
	}
	cout<<endl;
	return 0;
}
