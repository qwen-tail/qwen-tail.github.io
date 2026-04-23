# qwen-tail.github.io

Site qwen-tail.github.io

## Usefull scripts

### Универсальное копирование в буфер обмена на линукс



```sh
#!/usr/bin/env bash

clip2() {
    # 1. Надёжная проверка наличия xclip
    if ! command -v xclip &>/dev/null; then
        echo "Ошибка: xclip не установлен." >&2
        exit 1
    fi

    # 2. Обработка ввода
    if (( $# == 0 )); then
        # Чтение из stdin (пайп)
        xclip -selection clipboard -i
    else
        # Чтение из аргументов (сохраняет пробелы и спецсимволы)
        printf "%s" "$*" | xclip -selection clipboard -i
    fi

    echo "✅ Текст скопирован в буфер обмена."
}

# 3. Вызов функции со всеми переданными аргументами
clip2 "$@"

```

### midnight style

мой скрипт изначально называется mc1

запуск midnight commander
каждый раз со случаной доступной темой
(темы сканируются из папки /usr/share)
для пользователя
или для root (red cursor)

пример скрипта:
```sh
#!/usr/bin/env bash

run_mc1() {

    local who_am=$(whoami)
    # echo $who_am

    # !is_root
    if [ $who_am == "user" ]; then
        # echo "not root"

        # https://www.ing.iac.es/~docs/external/bash/abs-guide/randomvar.html
        local number=$(expr 0 + $RANDOM % 20)
        # https://opensource.com/article/18/5/you-dont-know-bash-intro-bash-arrays
        local allThreads=(darkfar
            dark
            featured-plus
            gotar
            gray-green-purple256
            gray-orange-blue256
            julia256
            modarcon16-defbg-thin
            modarcon16
            modarcon16-thin
            modarin256-defbg-thin
            modarin256
            modarin256-thin
            nicedark
            sand256
            seasons-autumn16M
            seasons-spring16M
            seasons-summer16M
            seasons-winter16M
            xoria256
            yadt256-defbg)
        # mc -S ${allThreads[number]}
        echo "${allThreads[number]}"
        mc -S ${allThreads[number]}

    else

        # https://www.ing.iac.es/~docs/external/bash/abs-guide/randomvar.html
        local number=$(expr 0 + $RANDOM % 7)
        # https://opensource.com/article/18/5/you-dont-know-bash-intro-bash-arrays
        local allThreads=(modarcon16root-defbg modarcon16root-defbg-thin modarcon16root modarcon16root-thin modarin256root-defbg modarin256root-defbg-thin modarin256root modarin256root-thin)

        # echo "mc -S ${allThreads[number]}"
        echo "${allThreads[number]}"
        sudo mc -S ${allThreads[number]}

    fi
}

run_mc1

```

нужно чтобы команды mcedit
также реагировал на разные темы
или по умолчания mcedit -S gotar $1

### timg

просмотр картинок в консоле

```sh
/usr/local/bin/timg -g100x50 "$1"
```

### 

### midnight style
### midnight style
### midnight style