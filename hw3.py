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
    user_input = input("Enter a command: ")    
    parts = user_input.split()
    # перевіряємо передан тільки шлях до файлу чи і рівень логів також
    if len(parts) < 2:
        file_path = parts[0]
        log_level = ''
    else:
        file_path, log_level = parts        
        
    logs = load_logs(file_path)
    counts = count_logs_by_level(logs)
    display_log_counts(counts)
    if log_level != '':
        print(f"\n Деталі логів для рівня '{log_level.upper()}':")
        for x in filter_logs_by_level(logs, log_level.upper()):
            print(x)

if __name__ == "__main__":
    main()
