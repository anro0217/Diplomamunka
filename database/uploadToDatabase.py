import json
from database import DatabaseManager


def upload_tasks_to_database(db_file, json_file, update=False):
    # Adatbázis inicializálása
    db = DatabaseManager(db_file)

    # JSON fájl beolvasása
    with open(json_file, 'r', encoding='utf-8') as file:
        tasks = json.load(file)

    # Feladatok feltöltése az adatbázisba
    for task in tasks:
        title = task.get("title")
        description = task.get("description")
        task_type = task.get("type")
        code_template = task.get("code_template")
        code_result = task.get("code_result")
        drag_drop_items = task.get("drag_drop_items")
        matching_pairs = task.get("matching_pairs")
        quiz_question = task.get("quiz_question")
        quiz_options = task.get("quiz_options")
        quiz_answer = task.get("quiz_answer")
        debugging_code = task.get("debugging_code")
        correct_code = task.get("correct_code")
        material = task.get("material")

        if update:
            existing_task = db.get_task_by_title(title)

            if existing_task:
                task_id = existing_task[0]
                success = db.update_task(task_id, title, description, task_type, code_template, code_result,
                                         drag_drop_items, matching_pairs, quiz_question, quiz_options, quiz_answer,
                                         debugging_code, correct_code, material)

                if not success:
                    print(f"Failed to update task: {title}")
            else:
                print(f"Task with title '{title}' not found, skipping update.")
        else:
            success = db.add_task(title, description, task_type, code_template, code_result, drag_drop_items,
                                  matching_pairs, quiz_question, quiz_options, quiz_answer, debugging_code,
                                  correct_code, material)

            if not success:
                print(f"Failed to add task: {title}")


if __name__ == "__main__":
    database_file = 'application.db'
    json_file = 'tasks_data.json'
    upload_tasks_to_database(database_file, json_file, True)  # 3rd param (update): update existing or create new
