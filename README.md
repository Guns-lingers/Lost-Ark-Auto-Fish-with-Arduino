# Lost-Ark-Auto-Fish-with-Arduino

**Automated Fishing Tool for Lost Ark (Автоматизированный инструмент для рыбалки в Lost Ark)**

## Overview (Обзор)

This tool is designed to streamline the fishing lifeskill in Lost Ark, providing automation without interfering with game code or network packets. It captures screenshots within specified regions and utilizes image recognition to identify and perform appropriate actions. (Этот инструмент разработан для оптимизации навыка рыболовства в Lost Ark, предоставляя автоматизацию без вмешательства в игровой код или сетевые пакеты. Он делает снимки экрана в указанных областях и использует распознавание изображений для определения и выполнения соответствующих действий.)

*Note: Results may vary based on individual circumstances. (Примечание: Результаты могут варьироваться в зависимости от индивидуальных обстоятельств.)*

## User Configuration (Конфигурация пользователя)

Before use, ensure your setup matches the tested configuration (Перед использованием убедитесь, что ваша настройка соответствует протестированной конфигурации):

- **Resolution (Разрешение):** 1080p
- **Display Mode (Режим отображения):** Fullscreen
- **HUD Size (Размер HUD):** 80%

## Development Environment Setup (Настройка среды разработки)

To set up the development environment, make sure you have Python 3.11.0 or a later version installed (Чтобы настроить среду разработки, убедитесь, что у вас установлена Python версии 3.11.0 или более поздней).

- [Python 3.11.0 or later](https://www.python.org/downloads/)
- [Arduino IDE](https://www.arduino.cc/en/software)

Once Python and Arduino IDE are installed, download the [Arduino sketch](https://github.com/Guns-lingers/Lost-Ark-Auto-Fish-with-Arduino/blob/main/auto_fish_sketch.ino) from the provided file.
После установки Python и Arduino IDE, загрузите [Arduino sketch](https://github.com/Guns-lingers/Lost-Ark-Auto-Fish-with-Arduino/blob/main/auto_fish_sketch.ino) из предоставленного файла.

Execute the following commands in the terminal (Выполните следующие команды в терминале):

```bash
pip3 install -r requirements.txt
python auto_fish.py
```

## WARNING (ПРЕДУПРЕЖДЕНИЕ)

⚠️ This tool is not endorsed by Smilegate or AGS. Its usage is not defined by Smilegate or AGS. No personal identifiable data is saved during the operation of this tool. Use it responsibly and at your own discretion. ⚠️

⚠️ Этот инструмент не поддерживается Smilegate или AGS. Его использование не определено Smilegate или AGS. Во время работы этого инструмента не сохраняются личные идентифицируемые данные. Используйте его ответственно и на свой страх и риск. ⚠️