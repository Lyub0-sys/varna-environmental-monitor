from __future__ import annotations

# json е част от стандартната библиотека.
# Използваме го, за да пазим отметките от чеклиста в отделен JSON файл.
import json

# sys е част от стандартната библиотека.
# Използваме го, за да прочетем командите, подадени през Terminal/PowerShell.
import sys

# Path е част от стандартната библиотека pathlib.
# Намира надеждно папката, в която се намира този .py файл.
from pathlib import Path

# dedent е част от стандартната библиотека textwrap.
# Помага ни да отпечатваме многострочен текст без излишни отстъпи.
from textwrap import dedent


# Папката на проекта Varna Environmental Monitor.
# Не пишем твърд Windows път, защото Path намира папката автоматично.
BASE_DIR = Path(__file__).resolve().parent

# В този JSON файл ще се пази кои задачи са приключени.
STATUS_FILE = BASE_DIR / "project_status.json"


PROJECT_TITLE = "Varna Environmental Monitor"

PROJECT_GOAL = """
Да изградим Flask уебприложение за наблюдение на околната среда във Варна.

Първа версия:
- качество на въздуха;
- данни от OpenAQ;
- записване в SQLite;
- обработка и SQL заявки;
- визуализация в браузъра;
- публикуване онлайн.

По-късно:
- метеорологични данни;
- радиационен фон;
- двуезичен интерфейс BG/EN;
- периодично обновяване на данните.
"""

ARCHITECTURE = """
ИЗТОЧНИК НА ДАННИ
        ↓
ИЗТЕГЛЯНЕ / ПРОЧИТАНЕ
        ↓
ПОЧИСТВАНЕ И ПРОВЕРКА
        ↓
SQLite БАЗА ДАННИ
        ↓
queries.py + data_utils.py
        ↓
Flask app.py
        ↓
HTML / Jinja templates
        ↓
CSS + диаграми
        ↓
PythonAnywhere / друга облачна услуга
"""

LESSONS_FROM_HEAD_FIRST = [
    "Разделяй проекта на малки модули, вместо всичко да бъде в app.py.",
    "Използвай BASE_DIR и Path, а не твърдо написани абсолютни пътища.",
    "Дръж SQL заявките в queries.py.",
    "Дръж достъпа до базата в data_utils.py.",
    "Използвай параметризирани SQL заявки, а не сглобяване на SQL с f-string.",
    "Прави резервно копие на базата преди миграция или голяма промяна.",
    "Проверявай за дублирани, липсващи и несвързани записи.",
    "Тествай локално целия поток: избор → заявка → резултат → диаграма.",
    "При облачно разгръщане проверявай Error log и Server log.",
    "Не пази пароли и API ключове директно в публичен код.",
    "След промяна в PythonAnywhere винаги прави Reload на приложението.",
    "Пази локалната и облачната конфигурация отделени, но с общ интерфейс.",
]


# done=True означава, че задачата вече е изпълнена.
# done=False означава, че задачата още предстои.
DEFAULT_TASKS = [
    {
        "id": "1.1",
        "section": "1. Основа на проекта",
        "task": "Създадена е папката varna_environment_monitor.",
        "done": True,
        "next": "Работим само в тази папка и не смесваме файловете с webapp.",
    },
    {
        "id": "1.2",
        "section": "1. Основа на проекта",
        "task": "Определена е целта: екологичен монитор за Варна.",
        "done": True,
        "next": "Първо завършваме минимална версия само с качеството на въздуха.",
    },
    {
        "id": "1.3",
        "section": "1. Основа на проекта",
        "task": "Добавен е този файл project_roadmap.py.",
        "done": True,
        "next": "Пускай го при започване на работа, за да видиш следващата задача.",
    },
    {
        "id": "2.1",
        "section": "2. Данни от OpenAQ",
        "task": "Избран е източникът OpenAQ и локация 8843 за Варна.",
        "done": True,
        "next": "Запази източника и обяснение за него в README.md.",
    },
    {
        "id": "2.2",
        "section": "2. Данни от OpenAQ",
        "task": "CSV файлът е прочетен с Python.",
        "done": True,
        "next": "Отдели четенето на данните в собствена функция.",
    },
    {
        "id": "2.3",
        "section": "2. Данни от OpenAQ",
        "task": "Извлечени са записите за параметъра CO.",
        "done": True,
        "next": "Направи функция, която приема име на параметър, а не работи само с CO.",
    },
    {
        "id": "2.4",
        "section": "2. Данни от OpenAQ",
        "task": "Събран е set от параметри и е върнат sorted списък.",
        "done": True,
        "next": "Провери кои параметри действително имат достатъчно измервания.",
    },
    {
        "id": "2.5",
        "section": "2. Данни от OpenAQ",
        "task": "Определи точните колони, които ще използваме.",
        "done": False,
        "next": "Избери минимум: location, parameter, value, unit, datetime, latitude, longitude.",
    },
    {
        "id": "2.6",
        "section": "2. Данни от OpenAQ",
        "task": "Добави проверки за липсващи стойности и невалидни типове.",
        "done": False,
        "next": "Провери None, празни низове, невалидни числа и невалидни дати.",
    },
    {
        "id": "2.7",
        "section": "2. Данни от OpenAQ",
        "task": "Добави проверка и премахване на дублирани измервания.",
        "done": False,
        "next": "Определи уникален ключ: station + parameter + datetime.",
    },
    {
        "id": "3.1",
        "section": "3. SQLite база данни",
        "task": "Създай SQLite файл за проекта.",
        "done": False,
        "next": "Предложено име: varna_environment.db.",
    },
    {
        "id": "3.2",
        "section": "3. SQLite база данни",
        "task": "Създай schema.sql.",
        "done": False,
        "next": "Започни с таблици stations, measurements и imports.",
    },
    {
        "id": "3.3",
        "section": "3. SQLite база данни",
        "task": "Създай Python код за записване на почистените измервания.",
        "done": False,
        "next": "Използвай INSERT с параметри и обработка на дублирани записи.",
    },
    {
        "id": "3.4",
        "section": "3. SQLite база данни",
        "task": "Провери броя на записите и връзките между таблиците.",
        "done": False,
        "next": "Направи COUNT заявки и проверка за orphan rows.",
    },
    {
        "id": "3.5",
        "section": "3. SQLite база данни",
        "task": "Направи резервно копие и процедура за възстановяване.",
        "done": False,
        "next": "Пази копие преди промяна на schema.sql.",
    },
    {
        "id": "4.1",
        "section": "4. Python модули",
        "task": "Създай data_utils.py.",
        "done": False,
        "next": "Тук ще бъдат функциите за връзка с базата и връщане на данни.",
    },
    {
        "id": "4.2",
        "section": "4. Python модули",
        "task": "Създай queries.py.",
        "done": False,
        "next": "Премести всички SQL SELECT заявки в този файл.",
    },
    {
        "id": "4.3",
        "section": "4. Python модули",
        "task": "Създай data_loader.py.",
        "done": False,
        "next": "Този модул ще чете CSV/API, ще валидира и ще записва в базата.",
    },
    {
        "id": "4.4",
        "section": "4. Python модули",
        "task": "Създай convert_utils.py само ако има реална нужда.",
        "done": False,
        "next": "Тук могат да бъдат преобразувания на дати, единици и числови стойности.",
    },
    {
        "id": "5.1",
        "section": "5. Flask приложение",
        "task": "Създай app.py и Flask приложението.",
        "done": False,
        "next": "Първо направи само начален маршрут /.",
    },
    {
        "id": "5.2",
        "section": "5. Flask приложение",
        "task": "Добави маршрут за избор на параметър.",
        "done": False,
        "next": "Например /parameters с CO, NO2, PM10 и други налични параметри.",
    },
    {
        "id": "5.3",
        "section": "5. Flask приложение",
        "task": "Добави маршрут за показване на измервания.",
        "done": False,
        "next": "Филтрирай по параметър и период.",
    },
    {
        "id": "5.4",
        "section": "5. Flask приложение",
        "task": "Добави маршрут за диаграма.",
        "done": False,
        "next": "Първо покажи една проста времева серия.",
    },
    {
        "id": "6.1",
        "section": "6. HTML и CSS",
        "task": "Създай templates/base.html.",
        "done": False,
        "next": "Общата HTML структура трябва да бъде само на едно място.",
    },
    {
        "id": "6.2",
        "section": "6. HTML и CSS",
        "task": "Създай templates/index.html.",
        "done": False,
        "next": "Покажи целта на проекта и последното налично измерване.",
    },
    {
        "id": "6.3",
        "section": "6. HTML и CSS",
        "task": "Създай шаблон за избор и филтриране.",
        "done": False,
        "next": "Използвай Jinja и HTML form, както в Swimclub.",
    },
    {
        "id": "6.4",
        "section": "6. HTML и CSS",
        "task": "Създай static/style.css.",
        "done": False,
        "next": "Първо направи чист и четим интерфейс, без JavaScript.",
    },
    {
        "id": "6.5",
        "section": "6. HTML и CSS",
        "task": "Добави диаграма и легенда с мерни единици.",
        "done": False,
        "next": "Винаги показвай parameter, value, unit и datetime.",
    },
    {
        "id": "7.1",
        "section": "7. Полезни функции",
        "task": "Покажи последното измерване за всеки параметър.",
        "done": False,
        "next": "Направи SQL заявка с MAX(datetime).",
    },
    {
        "id": "7.2",
        "section": "7. Полезни функции",
        "task": "Покажи история за избран период.",
        "done": False,
        "next": "Започни с последните 24 часа или 7 дни.",
    },
    {
        "id": "7.3",
        "section": "7. Полезни функции",
        "task": "Добави сравнение между параметри.",
        "done": False,
        "next": "Това е след минималната работеща версия.",
    },
    {
        "id": "7.4",
        "section": "7. Полезни функции",
        "task": "Добави български и английски интерфейс.",
        "done": False,
        "next": "Прави го след като основният поток вече работи.",
    },
    {
        "id": "7.5",
        "section": "7. Полезни функции",
        "task": "Добави време и радиационен фон.",
        "done": False,
        "next": "Това е втора фаза, не го започвай преди въздушните данни да са готови.",
    },
    {
        "id": "8.1",
        "section": "8. Тестване",
        "task": "Тествай четенето и почистването на данните.",
        "done": False,
        "next": "Провери нормален ред, празен ред, дубликат и невалидно число.",
    },
    {
        "id": "8.2",
        "section": "8. Тестване",
        "task": "Тествай SQL заявките отделно.",
        "done": False,
        "next": "Преди Flask провери резултатите в notebook или малък test файл.",
    },
    {
        "id": "8.3",
        "section": "8. Тестване",
        "task": "Тествай целия Flask поток.",
        "done": False,
        "next": "Начална страница → избор → заявка → резултат → диаграма.",
    },
    {
        "id": "8.4",
        "section": "8. Тестване",
        "task": "Добави обработка на грешки и логове.",
        "done": False,
        "next": "Показвай разбираемо съобщение, а подробността да остава в log.",
    },
    {
        "id": "9.1",
        "section": "9. Публикуване",
        "task": "Създай requirements.txt.",
        "done": False,
        "next": "Включи само библиотеките, които проектът реално използва.",
    },
    {
        "id": "9.2",
        "section": "9. Публикуване",
        "task": "Премахни пароли и API ключове от кода.",
        "done": False,
        "next": "Използвай environment variables или отделен непубличен config файл.",
    },
    {
        "id": "9.3",
        "section": "9. Публикуване",
        "task": "Качи проекта в PythonAnywhere или друга услуга.",
        "done": False,
        "next": "Използвай SQLite за първата безплатна версия.",
    },
    {
        "id": "9.4",
        "section": "9. Публикуване",
        "task": "Провери WSGI, Reload и error log.",
        "done": False,
        "next": "Това е задължителният облачен тест.",
    },
    {
        "id": "10.1",
        "section": "10. Портфолио",
        "task": "Създай README.md.",
        "done": False,
        "next": "Опиши проблема, данните, архитектурата, стартирането и резултата.",
    },
    {
        "id": "10.2",
        "section": "10. Портфолио",
        "task": "Добави screenshots на приложението.",
        "done": False,
        "next": "Покажи начална страница, филтър и диаграма.",
    },
    {
        "id": "10.3",
        "section": "10. Портфолио",
        "task": "Опиши какво си научил и какви проблеми си решил.",
        "done": False,
        "next": "Това е важно за кандидатстване за докторантура.",
    },
    {
        "id": "10.4",
        "section": "10. Портфолио",
        "task": "Качи проекта в GitHub, когато си готов.",
        "done": False,
        "next": "Не е нужно да активираш GitHub интеграцията във VS Code.",
    },
]


def ensure_utf8_output() -> None:
    """Настройва терминала да показва правилно български текст, когато е възможно."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def default_status() -> dict[str, bool]:
    """Връща началните отметки от DEFAULT_TASKS."""
    return {task["id"]: task["done"] for task in DEFAULT_TASKS}


def load_status() -> dict[str, bool]:
    """
    Зарежда състоянието от project_status.json.

    Ако файлът още не съществува, създава го автоматично.
    Ако по-късно добавим нова задача в кода, тя също ще се появи.
    """
    current = default_status()

    if STATUS_FILE.exists():
        try:
            saved = json.loads(STATUS_FILE.read_text(encoding="utf-8"))

            if isinstance(saved, dict):
                for task_id, done in saved.items():
                    if task_id in current and isinstance(done, bool):
                        current[task_id] = done
        except (json.JSONDecodeError, OSError):
            print("Предупреждение: project_status.json не можа да бъде прочетен.")
            print("Ще използваме началните отметки.\n")

    save_status(current)
    return current


def save_status(status: dict[str, bool]) -> None:
    """Записва отметките в project_status.json."""
    STATUS_FILE.write_text(
        json.dumps(status, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def print_header() -> None:
    """Показва заглавието и папката на проекта."""
    print("=" * 72)
    print(PROJECT_TITLE)
    print("=" * 72)
    print(f"Папка: {BASE_DIR}")
    print(f"Статус: {STATUS_FILE}")
    print()


def show_summary() -> None:
    """Показва целта, архитектурата и уроците от Head First Python."""
    print_header()

    print("ЦЕЛ НА ПРОЕКТА")
    print(dedent(PROJECT_GOAL).strip())
    print()

    print("АРХИТЕКТУРА")
    print(dedent(ARCHITECTURE).strip())
    print()

    print("КАКВО ПРЕНАСЯМЕ ОТ HEAD FIRST PYTHON")
    for number, lesson in enumerate(LESSONS_FROM_HEAD_FIRST, start=1):
        print(f"{number:>2}. {lesson}")
    print()


def show_checklist(status: dict[str, bool]) -> None:
    """Показва всички задачи, групирани по раздели."""
    current_section = None

    for task in DEFAULT_TASKS:
        if task["section"] != current_section:
            current_section = task["section"]
            print()
            print(current_section)
            print("-" * len(current_section))

        mark = "X" if status[task["id"]] else " "
        print(f"[{mark}] {task['id']}  {task['task']}")

    completed = sum(status.values())
    total = len(DEFAULT_TASKS)
    percent = round(completed / total * 100)

    print()
    print(f"Напредък: {completed}/{total} задачи ({percent}%)")
    print()


def find_task(task_id: str) -> dict | None:
    """Намира задача по нейния номер, например 3.2."""
    for task in DEFAULT_TASKS:
        if task["id"] == task_id:
            return task
    return None


def show_next_task(status: dict[str, bool]) -> None:
    """Показва първата незавършена задача и точната следваща стъпка."""
    for task in DEFAULT_TASKS:
        if not status[task["id"]]:
            print("СЛЕДВАЩА ЗАДАЧА")
            print(f"{task['id']} — {task['task']}")
            print(f"Как действаме: {task['next']}")
            print()
            return

    print("Всички задачи са отбелязани като завършени.")
    print()


def set_task_status(
    status: dict[str, bool],
    task_id: str,
    done: bool,
) -> None:
    """Маркира една задача като готова или незавършена."""
    task = find_task(task_id)

    if task is None:
        print(f"Няма задача с номер {task_id}.")
        print("Използвай: python project_roadmap.py list")
        return

    status[task_id] = done
    save_status(status)

    state = "ГОТОВА" if done else "НЕЗАВЪРШЕНА"
    print(f"{task_id} е маркирана като {state}.")
    print(task["task"])
    print()


def reset_status() -> None:
    """Връща всички отметки към началното състояние."""
    save_status(default_status())
    print("Чеклистът е върнат към началното състояние.")
    print()


def show_help() -> None:
    """Показва командите за използване на файла."""
    print_header()

    print("КОМАНДИ")
    print("python project_roadmap.py")
    print("    Показва обобщението, целия чеклист и следващата задача.")
    print()
    print("python project_roadmap.py list")
    print("    Показва само чеклиста.")
    print()
    print("python project_roadmap.py next")
    print("    Показва само следващата незавършена задача.")
    print()
    print("python project_roadmap.py done 3.2")
    print("    Маркира задача 3.2 като завършена.")
    print()
    print("python project_roadmap.py undo 3.2")
    print("    Връща задача 3.2 като незавършена.")
    print()
    print("python project_roadmap.py reset")
    print("    Връща целия чеклист към началното състояние.")
    print()


def main() -> None:
    """Главната функция обработва командите от PowerShell."""
    ensure_utf8_output()
    status = load_status()
    args = sys.argv[1:]

    if not args:
        show_summary()
        show_checklist(status)
        show_next_task(status)
        return

    command = args[0].lower()

    if command == "list":
        print_header()
        show_checklist(status)
        show_next_task(status)

    elif command == "next":
        print_header()
        show_next_task(status)

    elif command in {"done", "undo"}:
        if len(args) != 2:
            print(f"Правилен формат: python project_roadmap.py {command} 3.2")
            return

        set_task_status(
            status=status,
            task_id=args[1],
            done=command == "done",
        )
        show_next_task(status)

    elif command == "reset":
        reset_status()

    elif command in {"help", "-h", "--help"}:
        show_help()

    else:
        print(f"Непозната команда: {command}")
        print("Използвай: python project_roadmap.py help")


# Този блок се изпълнява само когато стартираме файла директно.
if __name__ == "__main__":
    main()
