#include <mysql.h>
#include <stdio.h>

int main(void)
{
                printf(“My_SQL client version: %s\n”, mysql_get_client_info());

return 0;
}
