"""Build compositions for one Binance Heist part, English or Russian."""
import copy
import heist
import longnight
from hf import Project
from heist_eps import EPS
from longnight_ru import RuProject, walk
import longnight_ru

TR = {
"0 BTC": "0 BTC", "The Binance Heist": "Ограбление Binance", "$40 million": "$40 миллионов", "Bitcoin": "биткоинов",
"May 7, 2019": "7 мая 2019", "#1 crypto exchange": "Криптобиржа №1", "Millions of users": "Миллионы пользователей",
"Wallets": "Кошельки", "Cold wallet": "Холодный", "Hot wallet": "Горячий", "offline": "офлайн", "online": "онлайн", "withdrawal": "вывод",
"17:15 UTC": "17:15 UTC", "of all Binance bitcoin": "всех биткоинов Binance", "In one move": "Одним движением",
"Security system": "Система защиты", "Looks normal": "Выглядит нормально", "Binance · Lockdown": "Binance · Блокировка",
"Deposits: suspended": "Пополнения: стоп", "Withdrawals: suspended": "Выводы: стоп", "The statement": "Заявление",
"API keys": "API-ключи", "2FA codes": "Коды 2FA", "+ more?": "+ что-то ещё?", "Part 1": "Часть 1",
"How do you rob it<br><em>without breaking in?</em>": "Как ограбить<br><em>без взлома?</em>",
"Part 2 →": "Часть 2 →", "Part 3 →": "Часть 3 →", "Part 4 →": "Часть 4 →", "Part 5 →": "Часть 5 →", "Part 6 →": "Часть 6 →",
"The method": "Метод", "KEYS": "КЛЮЧИ", "Vault: untouched": "Сейф не тронут", "Step 1 · Phishing": "Шаг 1 · Фишинг", "FAKE": "ФЕЙК",
"Step 2 · Viruses": "Шаг 2 · Вирусы", "Virus": "Вирус", "Step 3 · Collect": "Шаг 3 · Сбор", "Step 4 · Wait": "Шаг 4 · Ждать",
"Nothing.": "Ничего.", "Wait.": "Ждать.", "Binance · May 7, 2019": "Binance · 7 мая 2019", "The most opportune time": "Самый удачный момент",
"Step 5 · Blend in": "Шаг 5 · Слиться", "Independent?": "Независимые?", "Step 6 · Strike": "Шаг 6 · Удар", "PASSED": "ПРОЙДЕНО", "Part 2": "Часть 2",
"Who pays?": "Кто платит?", "Not this time": "Не в этот раз", "Secure Asset Fund for Users": "Защитный фонд пользователей",
"of all trading fees": "всех торговых комиссий", "Emergency vault": "Аварийный сейф", "CEO · Changpeng Zhao": "Глава · Чанпэн Чжао",
"SAFU covers 100%": "SAFU покрывает 100%", "Users lose: 0": "Потери людей: 0", "Withdrawals": "Выводы", "~1 week": "~1 неделя",
"New rules": "Новые правила", "Trade only": "Только торговля", "No robot withdrawals": "Никаких выводов роботами", "Next": "Дальше",
"Crisis over?": "Кризис позади?", "Another idea…": "Ещё одна идея…", "Part 3": "Часть 3", "HACK": "КРАЖА",
"The rollback": "Откат", "Rollback": "Откат", "How bitcoin works": "Как устроен биткоин", "Each block locks the last": "Блок закрепляет прошлый",
"Miners": "Майнеры", "Rebuild without the theft": "Пересобрать без кражи", "Outrun the network": "Обогнать сеть",
"Live stream · May 2019": "Прямой эфир · май 2019", "Developers": "Разработчики", "Crypto Twitter": "Криптосообщество",
"NO!": "НЕТ!", "Never!": "Ни за что!", "Not our chain!": "Не трогай блокчейн!", "Bitcoin's promise": "Обещание биткоина",
"Once it's written,<br><em>nobody can change it</em>": "Что записано,<br><em>не изменить</em>", "Not banks": "Не банкам",
"Not governments": "Не правительствам", "Not Binance": "Не Binance", "May 8, 2019": "8 мая 2019", "No rollback": "Отката не будет",
"CZ · May 8, 2019": "CZ · 8 мая 2019", "Part 4": "Часть 4", "The biggest heist<br><em>was still coming</em>": "Главное ограбление<br><em>ещё впереди</em>",
"October 6, 2022": "6 октября 2022", "A new thief": "Новый вор", "He prints money": "Он печатает деньги", "Beacon": "Beacon", "Smart": "Smart", "chain": "chain",
"Cross-chain bridge": "Мост между цепочками", "How the bridge works": "Как работает мост", "coins were sent": "монеты отправлены",
"The flaw": "Дыра", "Flaw in the proof check": "Дыра в проверке", "Forgery": "Подделка", "forged": "подделка", "VALID": "ВЕРНО",
"Again": "Снова", "Out of nothing": "Из воздуха", "on paper": "на бумаге", "Part 5": "Часть 5", "Get it out. Fast.": "Вывести. Быстро.",
"The getaway": "Побег", "Getaway": "Уходим", "BNB Chain validators": "Валидаторы BNB Chain", "Validators": "Валидаторы", "STOP": "СТОП",
"BNB Chain · Halted": "BNB Chain · Остановлен", "HALTED": "СТОП", "No blocks": "Ни блоков", "No transactions": "Ни транзакций",
"Hacker's wallet": "Кошелёк хакера", "trapped": "в ловушке", "Escaped": "Ушло", "already gone": "уже ушли", "Hard fork": "Хардфорк",
"FIX": "ФИКС", "Patched": "Исправлено", "~1 week later": "~неделю спустя", "Critics": "Критики", "Decentralized?!": "Децентрализация?!",
"One company?": "Одна компания?", "Two heists": "Два ограбления", "7,074 BTC · rollback?": "7 074 BTC · откат?", "2M BNB · from nothing": "2М BNB · из воздуха",
"Your call": "Твой выбор", "Rewrite history<br>or <em>stop the chain?</em>": "Переписать историю<br>или <em>остановить блокчейн?</em>",
"Follow for the next heist": "Подпишись на следующее", "1M BNB": "1М BNB", "2M BNB": "2М BNB", "M BNB": "М BNB", "M+": "М+", "M": "М",
"BINANCE": "BINANCE", "ETHEREUM": "ETHEREUM", "POLYGON": "POLYGON", "AVALANCHE": "AVALANCHE",
}
LABELS = dict(STOLEN="УКРАДЕНО", MINTED="ВЫПУЩЕНО")
QUOTES = {"“The hackers had the patience to wait…”": "«У хакеров хватило терпения ждать…»", "“…the most immutable ledger on the planet.”": "«…самый неизменяемый реестр на планете»",
          "OFFICIAL STATEMENT": "ОФИЦИАЛЬНОЕ ЗАЯВЛЕНИЕ", "Hackers obtained:": "Хакеры получили:", "SECURITY CHECK": "ПРОВЕРКА БЕЗОПАСНОСТИ",
          "Withdrawal · 7,074 BTC": "Вывод · 7 074 BTC", "BINANCE STATEMENT": "ЗАЯВЛЕНИЕ BINANCE", "POST · MAY 8, 2019": "ПОСТ · 8 МАЯ 2019", "Log in": "Вход", "LOG IN": "ВОЙТИ", ">PASSED</div>": ">ПРОЙДЕНО</div>"}


def ru_walk(x):
    if isinstance(x, str):
        s = TR.get(x, x)
        for a, b in QUOTES.items():
            s = s.replace(a, b)
        return s
    if isinstance(x, list):
        return [ru_walk(v) for v in x]
    if isinstance(x, tuple):
        return tuple(ru_walk(v) for v in x)
    if isinstance(x, dict):
        return {k: (v if k in ("id", "k", "col", "bc", "bgc") else ru_walk(v)) for k, v in x.items()}
    return x


def ru_frame(f):
    f = dict(f)
    for k in ("loc", "counters", "props", "over"):
        if k in f:
            f[k] = ru_walk(f[k])
    if "tags" in f:
        f["tags"] = [(ru_walk(t), w, c) for t, w, c in f["tags"]]
    if "bubbles" in f:
        f["bubbles"] = [(ru_walk(t), x, y, w) for t, x, y, w in f["bubbles"]]
    if "card" in f:
        f["card"] = (ru_walk(f["card"][0]),) + tuple(f["card"][1:])
    if "ev" in f:
        f["ev"] = [e if e[1] != "counter" else (e[0], e[1], (e[2][0], ru_walk(e[2][1]))) for e in f["ev"]]
    return f


def build(root, n, lang="en"):
    c, fr = copy.deepcopy(EPS[n])
    if lang == "ru":
        longnight.LABELS.update(LABELS)
        P = RuProject(root, n, f"/home/user/-/channels/crypto-heists/ep{n}.md")
        c = ru_walk(c)
        fr = [ru_frame(f) for f in fr]
    else:
        P = Project(root)
    ep = heist.HEp(P, c)
    for i, f in enumerate(fr, 1):
        ep.build(i, f)
    return len(fr)
