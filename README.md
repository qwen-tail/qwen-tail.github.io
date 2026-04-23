# qwen-tail.github.io

Site qwen-tail.github.io

## Usefull scripts

### Git init or add and commit

```sh
#!/usr/bin/env bash

# 1. Проверяем, находимся ли мы уже внутри git-репозитория
if ! git rev-parse --is-inside-work-tree &>/dev/null; then
    echo "Git-репозиторий не найден. Выполняется инициализация..."
    git init
fi

# 2. Добавляем все изменения в индекс
git add .

# 3. Определяем сообщение коммита:
#    Если передан $1 → используем его
#    Если $1 пустой или не передан → берём значение по умолчанию
COMMIT_MSG="${1:-Auto commit}"

# 4. Проверяем, есть ли что коммитить (чтобы избежать ошибки "nothing to commit")
if [[ -z $(git status --porcelain) ]]; then
    echo "Нет изменений для коммита. Пропускаем."
    exit 0
fi

# 5. Создаём коммит
git commit -m "$COMMIT_MSG"

echo "✅ Успешно. Коммит создан с сообщением: '$COMMIT_MSG'"

```

### Универсальное копирование в буфер обмена на линукс


### midnight random skins

### timg

просмотр картинок в консоле

```sh
/usr/local/bin/timg -g100x50 "$1"
```

### Markdown viewr mdm

### grc highlight
### color man pages
### 

