import argparse
from collections import Counter

def load_logs(file_path: str) -> list:
    logs = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                logs.append(parse_log_line(line.strip()))   
    except FileNotFoundError:
        print(f"Файл за вказаним шляхом '{file_path}' не знайдено.")
    except (IOError, OSError) as e:
        print(f"Помилка читання файлу, ймовірно він пошкоджений: {e}")
    except ValueError as ve:
        print(f"Помилка при обробці даних: {ve}.")
    finally:
        return logs

def parse_log_line(line: str) -> dict:
    keys = ['date', 'time', 'level', 'mess']    
    list = line.split()    
    if list[2].upper() not in ['INFO', 'DEBUG', 'ERROR', 'WARNING']:
        list[2] = 'OTHER'
    return dict(zip(keys, [list[0], list[1], list[2], ' '.join(list[3:])]))

def filter_logs_by_level(logs: list, level: str) -> list:      
    return [f'{x['date']} {x['time']} - {x['mess']}' for x in logs if x['level'] == level]
     
def count_logs_by_level(logs: list) -> dict:  
    return dict(Counter(item['level'] for item in logs))

def display_log_counts(counts: dict):
    print('\n Рівень логування | Кількість')
    print('-----------------|----------')
    for level, count in counts.items():
        print(f'{level.ljust(17)}|{count}')
   
def main():
    parser = argparse.ArgumentParser(description="Аналіз лог-файлу за рівнями логування.")
    parser.add_argument("file_path", help="Шлях до файлу логів")
    parser.add_argument("log_level", nargs='?', help="Рівень логування (INFO, ERROR, DEBUG), щоб фільтрувати записи", choices=["INFO", "ERROR", "DEBUG", "WARNING"])

    # Отримання аргументів
    args = parser.parse_args()
        
    logs = load_logs(args.file_path)
    counts = count_logs_by_level(logs)
    display_log_counts(counts)
    if args.log_level != '':
        print(f"\n Деталі логів для рівня '{args.log_level}':")
        for x in filter_logs_by_level(logs, args.log_level):
            print(x)

if __name__ == "__main__":
    main()
