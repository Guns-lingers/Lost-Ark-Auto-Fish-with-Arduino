# Lost-Ark-Auto-Fish-with-Arduino

**Автоматизированный инструмент для рыбалки в Lost Ark**

## Обзор

Этот инструмент разработан для оптимизации навыка рыболовства в Lost Ark, предоставляя автоматизацию без вмешательства в игровой код или сетевые пакеты. Он делает снимки экрана в указанных областях и использует распознавание изображений для определения и выполнения соответствующих действий с помощью сервомотора и платы Arduino.

*Примечание: Результаты могут варьироваться в зависимости от индивидуальных обстоятельств.*

## Конфигурация пользователя

Перед использованием убедитесь, что ваша настройка соответствует протестированной конфигурации:

- **Разрешение:** 1080p
- **Режим отображения:** Fullscreen
- **Размер HUD:** 80%

## Настройка среды разработки

Чтобы настроить среду разработки, убедитесь, что у вас установлена Python версии 3.11.0 или более поздней, а так же Arduino IDE.

- [Python 3.11.0 or later](https://www.python.org/downloads/)
- [Arduino IDE](https://www.arduino.cc/en/software)

Схема подключания сервомотора к Arduino
![servo scheme](https://github.com/Guns-lingers/Lost-Ark-Auto-Fish-with-Arduino/blob/main/ex23_servo_scheme.png)

После установки Python и Arduino IDE, загрузите [Arduino sketch](https://github.com/Guns-lingers/Lost-Ark-Auto-Fish-with-Arduino/blob/main/auto_fish_sketch/auto_fish_sketch.ino) из предоставленного файла, откройте его в Arduino IDE, подключите Arduino и загрузите.

![Upload sketch](https://github.com/Guns-lingers/Lost-Ark-Auto-Fish-with-Arduino/blob/main/Upload_sketch.jpg)

Выполните следующие команды в терминале не отключая Arduino:

```bash
pip3 install -r requirements.txt
python auto_fish.py
```

Если вы все сделали правильно, у вас должно открыться окно, и в поле выбора COM-порта будет отображен используемый в текущий момент Arduino порт.

![Auto fish UI](https://github.com/Guns-lingers/Lost-Ark-Auto-Fish-with-Arduino/blob/main/Auto_fish_UI.jpg)

После этого воодите текущее количество энергии, прочность инструмента, а так же не забудьте прикрепить сервомотор к той клавише, которая у вас отвечает за рыбалку. И после этого можете запускать, не забыв потом переключиться на окно игры.

## ПРЕДУПРЕЖДЕНИЕ

⚠️ Этот инструмент не поддерживается Smilegate или AGS. Его использование не определено Smilegate или AGS. Во время работы этого инструмента не сохраняются личные идентифицируемые данные. Используйте его ответственно и на свой страх и риск. ⚠️