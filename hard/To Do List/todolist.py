from sql_util import SqlSession
from datetime import datetime, timedelta

SQL = SqlSession()
PROMPT = "1) Today's tasks\n" \
         "2) Week's tasks\n" \
         "3) All tasks\n" \
         "4) Missed tasks\n" \
         "5) Add task\n" \
         "6) Delete task\n" \
         "0) Exit\n"


def main():
    while True:
        print_prompt()


def print_prompt():
    print(PROMPT)
    choice = input()
    fun_choices = {'1': todays_tasks, '2': weeks_tasks, '3': all_tasks, '4': missed_tasks, '5': add_task,
                   '6': delete_task, '0': shutdown}
    fun_choices.get(choice, incorrect_input)()


def todays_tasks():
    today = datetime.today()
    rows = SQL.get_todays_tasks()
    print(f"Today {today.day} {today.strftime('%b')}:")
    if len(rows) == 0:
        print("Nothing to do!")
    else:
        for index, task in enumerate(rows, start=1):
            print(f"{index} {task.task}")
    print("")


def weeks_tasks():
    task = {}
    rows = SQL.get_weeks_tasks()
    today = datetime.today()
    for row in rows:
        task.setdefault(row.deadline, []).append(row.task)
    for i in range(7):
        day = today + timedelta(days=i)
        print("")
        print(day.strftime(f"%A {day.day} %b:"))
        tasks = task.get(day.date())
        if not tasks:
            print("Nothing to do!")
        else:
            for c in range(0, len(task[day.date()])):
                print(f"{c+1} {task[day.date()][c]}")
    print("")


def all_tasks():
    rows = SQL.get_tasks()
    print("All tasks:")
    if len(rows) == 0:
        print("Nothing to do!")
    else:
        for index, task in enumerate(rows, start=1):
            print(f"{index} {task.task}. {task.deadline.strftime('%#d %b')}")
    print("")


def add_task():
    print("Enter task")
    task = input()
    print("Enter deadline")
    deadline = input()
    SQL.add_task(task=task, deadline=datetime.strptime(deadline, '%Y-%m-%d'))
    print("The task has been added!")
    print("")


# TODO: combine with all_tasks
def missed_tasks():
    print("Missed tasks:")
    rows = SQL.get_missed_tasks()
    if len(rows) == 0:
        print("Nothing to do!")
    else:
        for index, task in enumerate(rows, start=1):
            print(f"{index} {task.task}. {task.deadline.strftime('%#d %b')}")
    print("")


def delete_task():
    print("Choose the number of the task you want to delete:")
    task = {}
    rows = SQL.get_tasks()

    for index, row in enumerate(rows, start=1):
        print(f"{index} {row.task}. {row.deadline.strftime('%#d %b')}")
        task.setdefault(index, row.id)
    print("")
    task_id_to_delete = task[int(input())]
    SQL.delete_task(task_id_to_delete)
    print("The task has been deleted!")


def shutdown():
    print("\nBye!")
    exit(0)


def incorrect_input():
    print("Incorrect input, try again\n")
    print_prompt()


if __name__ == '__main__':
    main()
