from helping_functions import create_meal, create_user, select_users_by_mealpoints
import sqlite3
conn = sqlite3.connect('database.db')
c = conn.cursor()
# Insert a row of data
user1='Julien R.',1,1000,10.3,2,1, 1
user2='Corentin B.',2,1001,10.3,2,1, 1
create_user(conn,user1)
create_user(conn,user2)

# Save (commit) the changes
conn.commit()
rows=select_users_by_mealpoints(conn,1)
for row in rows:
    print(row)
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()