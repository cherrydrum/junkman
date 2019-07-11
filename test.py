import main as m

conn = m.Connection('config.txt')
print(conn.req('users.get', {'user_ids': '371469551'}))
