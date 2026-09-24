# FunPay Cardinal Remake

Модифицированная сборка FunPay Cardinal Remake для автоматизации работы с биржей FunPay

В этой версии убраны рекламные интеграции, удаленные объявления, автозагрузка обновлений и автоматическое изменение профиля Telegram-бота. Интерфейс бота переведен на русский язык, а суммы для пользователя отображаются в рублях или UAH в зависимости от выбранного режима.

## Возможности

- Автовыдача товаров.
- Автоподнятие лотов.
- Автоответы на настроенные команды.
- Автовосстановление лотов после продажи.
- Автодеактивация лотов, если товары закончились.
- Уведомления о заказах, сообщениях и изменениях в Telegram.
- Управление настройками через Telegram-панель.
- Отдельные настройки уведомлений для каждого авторизованного Telegram-аккаунта.
- Поддержка шаблонов и переменных в текстах.
- Система плагинов для расширения функциональности.
- Ручной вывод средств через сохраненные кошельки FunPay.

## Что изменено

- Удалены авторские рекламные ссылки и упоминания.
- Удалены удаленные объявления и загрузка рекламных фото.
- Удалены скрытые preview-ссылки на сторонние изображения.
- Отключены автообновления из чужих источников.
- Отключено автоматическое изменение названия и описания Telegram-бота.
- Убрано требование, чтобы username Telegram-бота начинался с `funpay`.
- Удалены сторонние Telegram-каналы, донаты и чаты.
- Удалены команды и обработчики backup-архивов.
- Удалены водяной знак и автоматическое добавление подписи в сообщения.
- Удалены лишние команды Telegram-меню: `/about`, `/sys`, `/power_off`, `/upload_chat_img`, `/upload_offer_img`.
- Профиль, уведомления, покупки и ручной вывод отображаются в выбранной валюте.
- Неавторизованный пользователь получает короткий ответ `⛔ У тебя нет доступа`.
- Авторизованные пользователи получают критическое уведомление о попытке входа стороннего пользователя.
- Уведомление о новом заказе приходит независимо от того, привязана ли к лоту автовыдача.
- Очищены временные файлы, кеши, старые update-файлы и funding-настройки.

## Важно

После настройки не публикуйте и не передавайте другим людям:

- `golden_key`;
- токен Telegram-бота;
- файлы из `configs/`;
- файлы из `storage/`;
- логи из `logs/`;
- приватные архивы с данными бота.

Эти данные могут дать доступ к вашему аккаунту или панели управления.

## Установка на Windows

1. Установите Python 3.11 или новее.
2. Во время установки Python включите `Add python.exe to PATH`.
3. Скачайте архив проекта со страницы репозитория или из раздела Releases.
4. Распакуйте архив в удобную папку.
5. Запустите `Setup.bat` и дождитесь установки зависимостей.
6. Запустите `Start.bat`.
7. При первом запуске пройдите настройку в консоли.

Если окно сразу закрывается, откройте папку проекта в `cmd` или PowerShell и выполните:

```bat
python main.py
```

## Установка на Ubuntu/Debian

Автоматический установщик подходит для Ubuntu/Debian-серверов с `systemd`.

```bash
wget https://raw.githubusercontent.com/felusium/FunPayCardinalRemake/main/install-fpc.sh -O install-fpc.sh && bash install-fpc.sh
```

Установщик:

- загружает файлы только из этого репозитория;
- устанавливает системные зависимости;
- создает отдельного Linux-пользователя для запуска;
- создает виртуальное окружение Python;
- устанавливает Python-зависимости из `requirements.txt`;
- создает systemd-сервис `FunPayCardinalRemake`;
- предлагает добавить сервис в автозапуск;
- запускает первичную настройку.

При повторном запуске установщик обновляет файлы проекта, но не удаляет приватные папки:

- `configs/`;
- `storage/`;
- `plugins/`;
- `logs/`.

Полезные команды после установки:

```bash
sudo systemctl status FunPayCardinalRemake@fpc.service -n 100
sudo systemctl stop FunPayCardinalRemake@fpc.service
sudo systemctl start FunPayCardinalRemake@fpc.service
sudo systemctl restart FunPayCardinalRemake@fpc.service
sudo systemctl enable FunPayCardinalRemake@fpc.service
sudo journalctl -u FunPayCardinalRemake@fpc.service -n 100 --no-pager
```

Если при установке вы указали другого Linux-пользователя вместо `fpc`, замените `fpc` в командах на свое имя пользователя.

## Ручная установка на Linux

Этот вариант подходит для Linux без автоматического установщика или если нужно запускать бота вручную без `systemd`.

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
git clone https://github.com/felusium/FunPayCardinalRemake.git
cd FunPayCardinalRemake
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -r requirements.txt
python main.py
```

Для повторного запуска:

```bash
cd FunPayCardinalRemake
source .venv/bin/activate
python main.py
```

## Установка на Android через Termux

Termux не использует `systemd`, поэтому Ubuntu-установщик для него не подходит. Запускайте бота вручную или через `tmux`.

```bash
pkg update && pkg upgrade
pkg install python git clang rust make pkg-config libjpeg-turbo zlib libxml2 libxslt openssl libffi
git clone https://github.com/felusium/FunPayCardinalRemake.git
cd FunPayCardinalRemake
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip setuptools wheel
pip install --no-cache-dir -r requirements.txt
python main.py
```

Чтобы бот продолжал работать после закрытия сессии, используйте `tmux`:

```bash
pkg install tmux
termux-wake-lock
cd FunPayCardinalRemake
tmux new -s fpc
source .venv/bin/activate
python main.py
```

Выйти из `tmux`, не останавливая бота: нажмите `Ctrl+B`, затем `D`.

Вернуться к боту:

```bash
tmux attach -t fpc
```

На Android работа в фоне зависит от прошивки и энергосбережения. Для стабильности отключите оптимизацию батареи для Termux.

## Плагины

Не устанавливайте плагины из непроверенных источников. Плагин выполняется как обычный Python-код и может получить доступ к файлам, конфигам и аккаунту.

Установка плагина через Telegram-панель:

1. Напишите Telegram-боту команду `/menu`.
2. Откройте раздел `Плагины`.
3. Нажмите `Добавить плагин`.
4. Отправьте файл плагина.
5. Перезапустите бота.

## Курсы и валюта

Бот может отображать суммы в рублях или UAH. Для управления режимом UAH используется команда:

```text
/UAH auto
/UAH off
```

`/UAH auto` обновляет курс с FunPay

`/UAH off` возвращает отображение сумм в рублях.

Покупки, баланс в `/profile` и ручной вывод отображаются прямым пересчетом.

## Обновления

Автоматические обновления из чужих источников отключены.

Чтобы обновить проект вручную:

1. Остановите бота.
2. Сохраните приватные папки `configs/`, `storage/` и `plugins/`.
3. Скачайте новую версию вручную или запустите `/update`, если хотите обновиться из этого репозитория.
4. Проверьте работу бота перед запуском в постоянном режиме.

На Ubuntu/Debian можно повторно запустить `install-fpc.sh`: он обновит файлы проекта и сохранит `configs/`, `storage/`, `plugins/`, `logs/`.

## Ответственность

Используйте проект на свой риск. Соблюдайте правила FunPay, Telegram и GitHub. Не публикуйте приватные ключи, токены, cookie, конфиги, товары и логи.
