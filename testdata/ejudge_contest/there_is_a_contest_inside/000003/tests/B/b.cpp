#include <stdio.h>

int main()
{
	int i, j, n, a[2];
	a[0] = a[1] = 0;
	scanf("%d", &n);
	for (i=0; i<n; i++)	{
		scanf("%d", &j);
		a[j%2]++;
	}
	j = a[0]<a[1]?a[0]:a[1];
	printf("%d", j);
	return 0;
}