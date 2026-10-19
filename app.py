"""A local help-desk practice application. Uses Python's standard library only."""
import argparse
import sqlite3
from pathlib import Path

STATUSES = ('Open', 'In Progress', 'Resolved')
PRIORITIES = ('Low', 'Medium', 'High')

class TicketStore:
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.db.row_factory = sqlite3.Row
        self.db.execute('''CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT NOT NULL, issue TEXT NOT NULL,
            priority TEXT NOT NULL CHECK(priority IN ('Low','Medium','High')),
            status TEXT NOT NULL DEFAULT 'Open'
                CHECK(status IN ('Open','In Progress','Resolved')),
            created TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)''')
        self.db.commit()

    def create(self, customer, issue, priority):
        if not customer.strip() or not issue.strip():
            raise ValueError('Customer and issue cannot be blank.')
        if priority not in PRIORITIES:
            raise ValueError('Invalid priority.')
        with self.db:
            cursor = self.db.execute(
                'INSERT INTO tickets(customer,issue,priority) VALUES (?,?,?)',
                (customer.strip(), issue.strip(), priority))
        return cursor.lastrowid

    def search(self, query='', status=None):
        # Bound parameters keep user text separate from SQL commands.
        sql = 'SELECT * FROM tickets WHERE (instr(lower(customer),lower(?))>0 OR instr(lower(issue),lower(?))>0 OR CAST(id AS TEXT)=?)'
        args = [query, query, query]
        if status:
            if status not in STATUSES:
                raise ValueError('Invalid status.')
            sql += ' AND status=?'
            args.append(status)
        return self.db.execute(sql + ' ORDER BY id DESC', args).fetchall()

    def update_status(self, ticket_id, status):
        if status not in STATUSES:
            raise ValueError('Invalid status.')
        with self.db:
            cursor = self.db.execute('UPDATE tickets SET status=? WHERE id=?', (status, ticket_id))
        return cursor.rowcount > 0

    def summary(self):
        counts = dict(self.db.execute('SELECT status,COUNT(*) FROM tickets GROUP BY status'))
        return {s: counts.get(s, 0) for s in STATUSES}

    def close(self):
        self.db.close()


def choose(label, options):
    while True:
        print(label + ': ' + ', '.join(f'{i+1}={s}' for i, s in enumerate(options)))
        answer = input('Choose: ').strip()
        if answer.isdigit() and 1 <= int(answer) <= len(options):
            return options[int(answer)-1]
        print('Please choose a listed number.')


def display(rows):
    if not rows:
        print('No matching tickets.')
    for row in rows:
        print(f"\n#{row['id']} | {row['status']} | {row['priority']} | {row['customer']}")
        print(f"Issue: {row['issue']}\nCreated: {row['created']} UTC")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', default=str(Path(__file__).with_name('tickets.db')))
    parser.add_argument('--demo', action='store_true', help='Load fictional examples into an empty database')
    args = parser.parse_args()
    store = None
    try:
        store = TicketStore(args.db)
        if args.demo and not store.search():
            store.create('Alex Demo', 'Laptop cannot connect to Wi-Fi', 'High')
            number = store.create('Sam Example', 'Install a PDF reader', 'Low')
            store.update_status(number, 'Resolved')
            store.create('Taylor Sample', 'Phone data transfer assistance', 'Medium')
        while True:
            print('\nIT SUPPORT TICKET TRACKER\n1. Create ticket\n2. List tickets\n3. Search tickets\n4. Change status\n5. Filter by status\n6. Summary\n0. Exit')
            option = input('Choose: ').strip()
            try:
                if option == '0':
                    break
                elif option == '1':
                    customer = input('Customer: ')
                    issue = input('Issue: ')
                    priority = choose('Priority', PRIORITIES)
                    print(f'Ticket #{store.create(customer, issue, priority)} created.')
                elif option == '2':
                    display(store.search())
                elif option == '3':
                    display(store.search(input('Search name, issue, or exact ID: ')))
                elif option == '4':
                    number = int(input('Ticket ID: '))
                    status = choose('Status', STATUSES)
                    print('Status saved.' if store.update_status(number, status) else 'Ticket not found.')
                elif option == '5':
                    display(store.search(status=choose('Status', STATUSES)))
                elif option == '6':
                    for status, count in store.summary().items():
                        print(f'{status}: {count}')
                else:
                    print('Choose a listed menu number.')
            except ValueError as error:
                print('Invalid input:', error)
    except (EOFError, KeyboardInterrupt):
        print('\nGoodbye.')
    except sqlite3.Error as error:
        print('Database error:', error)
        raise SystemExit(1)
    finally:
        if store:
            store.close()

if __name__ == '__main__':
    main()
