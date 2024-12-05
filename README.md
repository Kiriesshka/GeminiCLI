# GeminiCLI
Позволяет запустить gemini из терминала

## Установка(Python-версия)
  1. Скопировать репозиторий:
     ```
     git clone https://github.com/Kiriesshka/CommandLineGemini.git
     ```
  2. Перейти в папку:
     ```
     cd CommandLineGemini
     ```
  3. С помощью любого удобного редактора открыть файл:
     ```
     vim gemini.py
     ```
  4. Вставить api ключ в поле **`API_KEY`**.
  5. Если нужен запуск из любой места в терминале по шорткату, прочитайте файл `shortcut.txt` и выполните его требования.

## Использование(Python-версия)
  Запустите из директории с файлами с помощью:
  ```
  python3 gemini.py
  ```
  или сделайте на него alias в **`~/.bashrc`**, если хотите, чтобы было удобнее.
  После этого вы можете вводить запросы.

  Если получаете ошибку **`400`** или ей подобные, то либо ваш api ключ устарел/не существует, либо ваш ip адрес определяется в запрещенной для использования стране(что довольно просто избегается при желании)
  
  Предусмотрено несколько комманд, чтобы вывести их на экран нужно прописать команду:
  ```
  /help
  ```
  после запуска программы.
## Установка(Shell-версия)
 1. Установить jq:
    *Debian:*
    ```
    sudo apt-get install jq
    ```
    *Termux:*
    ```
    pkg install jq
    ```
  2. Скопировать репозиторий:
     ```
     git clone https://github.com/Kiriesshka/CommandLineGemini.git
     ```
  3. Перейти в папку:
     ```
     cd CommandLineGemini
     ```
  4. С помощью любого удобного редактора открыть файл:
     ```
     vim gemini.sh
     ```
  7. Вставить api ключ в поле **`API_KEY`**.
**Использование(Shell-версия)**
  Запустите из директории с файлами с помощью:
  ```
  bash gemini.sh
  ```
  или сделайте на него alias в **`~/.bashrc`**, если хотите, чтобы было удобнее.
  После этого вы можете вводить запросы.

  Если получаете **`null`** в качестве ответа или ошибку **`400`** или ей подобные, то либо ваш api ключ устарел/не существует(вероятнее всего при *`null`*), либо ваш ip адрес определяется в запрещенной для использования стране(что довольно просто избегается при желании)
  
  Предусмотрено несколько комманд, чтобы вывести их на экран нужно прописать команду:
  ```
  /help
  ```
  после запуска программы.
## Промпты
  В папке со скриптом есть папка **`PROMPTS`**, по умолчанию там лежат два файла **`Example.txt`** и **`Example.txt.settings`**,
  первый содержит промпт, второй имена модели и пользователя через `_/_`. Если вы хотите создать свой собственный промпт, то сделайте текстовый файл с любым расширением(хотя лучше использовать `.txt`), напрмер `Test.txt`, а также текстовый файл, название которого будет как название первого файла, но с расширением `.settings`, то есть **`Test.txt.settings`**, в нем через `_/_` перечислите имя модели и пользователя, например `SupeDuperSmartAI_/_Mark`, после создания вы сможете загружать его с помощью команды **`/load [p]`**, где `[p]` - полное название файла(в случае примера это будет `Test.txt`)
## Примечания
  1. Первый элемент памяти никогда не очищается при достижении лимита, можете использовать его для хранения основных инструкций, тогда нейросеть не забудет их, сюда же записывается промпт при загрузке. Все остальные элементы при достижении лимита сдвигаются влево, а второй удаляется. 
  2. Вставка через Ctrl+Shift+V работает некорректно, избегайте ее.
  3. Нельзя переносить на новую строку с помощью клавиши Enter(Это приведет к отправке сообщения).
  4. Проверяйте текст(если вы его вставляете) на отсутствие переносов строки(см. прим. 3).
