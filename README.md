# IT Support Ticket Tracker

A beginner-friendly Python command-line application for recording and tracking help-desk issues. This is a local portfolio practice project, not a production support system.

## Features

- Create tickets with a customer name, issue, and Low/Medium/High priority.
- Automatically generate ticket IDs and creation timestamps (UTC).
- List tickets or search by name, issue, and exact ID.
- Update a ticket to Open, In Progress, or Resolved.
- Filter tickets by status and view status counts.
- Save records in SQLite so they remain after the program closes.
- Validate input and use parameterized SQL queries.

## Requirements and run instructions

Python 3.10 or newer. No packages to install.

Open a Terminal in this project folder:

```bash
python3 app.py --demo
```

On Windows, use `py app.py --demo` if `python3` is unavailable.
The demo option adds three fictional tickets only when the database is empty. It never resets existing tickets.

In PyCharm: open this folder, select a Python 3 interpreter, right-click `app.py`, then choose Run. The menu works without demo data; choose 1 to add your own ticket.

The default database is `tickets.db` next to `app.py`. To use another database:

```bash
python3 app.py --db practice.db --demo
```

## Quick demonstration

1. Run with `--demo`.
2. Choose 2 to list the sample tickets.
3. Choose 4, enter ticket ID 1, and choose 2 for In Progress.
4. Choose 5, then 2, to see that ticket.
5. Choose 6 for the summary.
6. Exit with 0 and reopen; the change is still saved.

See [DEMO.txt](DEMO.txt) for a recorded run.

## Project structure

- `app.py`: SQLite storage class, input helpers, and interactive menu.
- `test_app.py`: automated tests using temporary databases.
- `DEMO.txt`: example program output with fictional data.
- `.gitignore`: keeps personal databases and Python cache files out of Git.

## Tests

```bash
python3 -m unittest -v
```

Tests cover persistence across reopening, status filtering and counts, missing IDs, validation, and literal searches including SQL-like text.

## Design and limitations

`TicketStore` handles SQL operations; the menu handles user interaction. Database transactions commit changes immediately. There is no login, shared server, attachment support, or ticket audit history. Names and issues are stored locally as plain text in SQLite. Use fictional data in a public demonstration.

## Concepts to understand

Functions, classes, exception handling, SQL CRUD operations, bound parameters, and automated testing. Start by tracing `create()` from the menu to the INSERT query.

## Possible improvements

Add resolution notes, due dates, CSV export, or a Tkinter interface after understanding this version.

## Development note

This starter version was generated with AI assistance. Anyone using it as a portfolio project should review, run, explain, and personalize the code, and describe their own contributions accurately.
