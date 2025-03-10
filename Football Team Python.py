class Team:
    def __init__(self, name):
        """Инициализация команды с названием и пустым списком игроков"""
        self.name = name
        self.players = set()  # Используем set, чтобы избежать дубликатов

    def add_player(self, player_name):
        """Добавляет игрока в команду, если он не в списке"""
        if player_name in self.players:
            print(f"⚠️ Игрок {player_name} уже в команде!")
        else:
            self.players.add(player_name)
            print(f"✅ Игрок {player_name} добавлен в команду {self.name}.")

    def remove_player(self, player_name):
        """Удаляет игрока из команды, если он в списке"""
        if player_name in self.players:
            self.players.remove(player_name)
            print(f"✅ Игрок {player_name} удалён из команды {self.name}.")
        else:
            print(f"⚠️ Игрок {player_name} не найден в команде {self.name}.")

    def show_team(self):
        """Выводит информацию о команде"""
        print(f"\n🏆 Команда: {self.name}")
        if self.players:
            print("👥 Игроки:", ", ".join(self.players))
        else:
            print("⚠️ В команде пока нет игроков.")

def get_valid_int(prompt):
    """Функция для безопасного ввода целого числа"""
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("❌ Число не может быть отрицательным! Попробуйте снова.")
            else:
                return value
        except ValueError:
            print("❌ Ошибка! Введите целое число.")

def get_valid_input(prompt):
    """Функция для обработки пустого ввода"""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("❌ Ошибка! Поле не может быть пустым.")

# Ввод данных от пользователя
team_name = get_valid_input("Введите название команды: ")
team = Team(team_name)

num_players = get_valid_int(f"Введите количество игроков для команды {team_name}: ")

for _ in range(num_players):
    player_name = get_valid_input("Введите имя игрока: ")
    team.add_player(player_name)

# Главное меню
while True:
    print("\n🔹 Выберите действие:")
    print("1️⃣ Показать команду")
    print("2️⃣ Добавить игрока в команду")
    print("3️⃣ Удалить игрока из команды")
    print("4️⃣ Выйти")

    choice = input("Введите номер действия: ").strip()

    if choice == "1":
        team.show_team()
    elif choice == "2":
        new_player = get_valid_input("Введите имя нового игрока: ")
        team.add_player(new_player)
    elif choice == "3":
        if not team.players:
            print("⚠️ В команде нет игроков для удаления!")
        else:
            player_to_remove = get_valid_input("Введите имя игрока для удаления: ")
            team.remove_player(player_to_remove)
    elif choice == "4":
        print("\n🚀 Программа завершена.")
        break
    else:
        print("❌ Ошибка! Введите число от 1 до 4.")
