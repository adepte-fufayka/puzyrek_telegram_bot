import re
from datetime import timedelta, timezone
FULL_PROFILE = re.compile(
    r"^📟Пип-бой\s3000\sv\d+\.\d+\n"
            r"(Игровое\sсобытие\n\".+?\")?\n(?P<nickname>.+),\s(?P<fraction_emoji>[🔪💣🔰⚛️⚙️👙🤕])(?P<fraction_name>.+)\n"
            r"🤟Банда:\s(?P<gang_name>.+)\n"
            r"❤️Здоровье:\s\d+/(?P<max_hp>\d+)\n"
            r"☠️Голод:\s\d+%\s/myfood\n"
            r"⚔️Урон:\s(?P<damage>\d+)\s🛡Броня:\s(?P<armor>\d+)(\s\(\+\d+\))?\n{2}"
            r"💪Сила:\s(?P<strength>\d+)\s🎯Меткость:\s(?P<accuracy>\d+)\n"
            r"🗣Харизма:\s(?P<charisma>\d+)\s🤸🏽‍♂️Ловкость:\s(?P<dexterity>\d+)\n"
            r"💡Умения\s/perks\n"
            r"⭐️Испытания\s/warpass\n{2}"
            r"🔋Выносливость:\s\d+/(?P<max_energy>\d+)\s/ref\n"
            r"📍.+?\s👣\d+км\. (👊)?\n{2}"
            r"Экипировка:.+?"
            r"Ресурсы:\n"
            r"🕳Крышки:\s(?P<lids>\d+)\s\n"
            r"📦Материалы:\s(?P<materials>\d+)\n"
            r"💈Пупсы:\s(?P<pups>\d+).+?"
            r"(🏵(?P<zen>\d+)\s[▓░]+\n)?"
            r"ID(?P<user_id>\d+)",
    re.DOTALL
)
SHORT_PROFILE = re.compile(
    r"^👤(?P<nickname>.+?)(🏵(?P<zen>\d+))?\n"
            r"├🤟\s(?P<gang_name>.+?)\n"
            r"├(?P<fraction_emoji>[🔪💣🔰⚛️⚙️👙🤕])(?P<fraction_name>.+?)\n"
            r"├❤️\d+/(?P<max_hp>\d+)\s\|\s🍗\d+%\s\|\s⚔️(?P<damage>\d+)\s\|\s🛡(?P<armor>\d+)\n"
            r"├💪(?P<strength>\d+)\s\|\s🎯(?P<accuracy>\d+)\n"
            r"├🗣(?P<charisma>\d+)\s\|\s🤸🏽‍♂️(?P<dexterity>\d+)\n"
            r"├🔋\d+/(?P<max_energy>\d+)\s\|\s👣\d+\n"
            r".+?"
            r"├🕳(?P<lids>\d+)\n"
            r"├📦(?P<materials>\d+)💈(?P<pups>\d+)",
            re.DOTALL
)
VIEW = re.compile(
    r"^(?P<zone>[🚷👣])(?P<kilometr>\d+)\sкм\.\n"
           r"Ты\sогляделся\sвокруг\sсебя\.\s"
           r"\nРядом\sкто-то\sесть\.\n"
           r"\n(.+\n)*",
    re.DOTALL)
BAND_PANEL=re.compile(r"^🤘 (?P<nickname>.+) 🏅(?P<raiting>\d+)\n"
                      r"Панель банды.\n"
                      r"\n"
                      r"Главарь\n"
                      r"⚜️ (?P<band_leader_name>.+)\n"
                      r"\n"
                      r"Козёл\n"
                      r"🐐 (?P<goat_name>.+) /goat\n"
                      r"\n")
BOT_WW_ID = 430930191
BOT_WW_USERNAME="@WastelandWarsBot"
PROFILE_BUTTONS = ['📟Пип-бой']
PROFILE_DELTA = 30
FRAC_CHAT_IDS = [-1002506127430]
RUKOVODSTVO_CHAT_ID=-1002347000814
GOAT_NAME="⚙️Острые Пузырьки🫧"
GOAT_BAND_NAMES = ['Фисташки', 'Жидобои', 'Потом Придумаем', 'Телепузики']
GOAT_BAND_NAMES_LATIN=['Fistashki', 'Zhidoboi','Potomki','Telepuziki']
GOAT_BAND_NAMES_SHORT=['🥜','🆓','🔜','😎']
GOAT_BAND_CHAT_IDS=[-1002163822478, -1002170342191, -1002654379245, -1002873689795]
LINE_SPLITTER = ';^;'
ROLES=['User','Mover','Officer','Admin']
OWNER_ID=[850966027]
RAID_KMS=['🔆9','🔆12','🚷24','🚷32', '🔆46']
LONG_RAID_KMS=['9 км СЗ🔆','12 км СЗ🔆','24 км ТЗ🚷','32 км ТЗ🚷', '46 км СЗ🔆']
SAFE_ZONES=[[8], [11], [22,23], [22,27], [45]]
SHAG_MESSAGE=['пинг',"проверка связи","кусь","смотри закреп"]
MOSCOW = timezone(timedelta(hours=3), "Moscow")
CREATE_PIN="Пины козла"
NOT_IN_USER_DATABASE="Уж не засланный ли ты казачок? Скинь свой пип-бой и попробуй еще раз"