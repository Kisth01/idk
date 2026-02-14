import requests
import time
import json
from datetime import datetime
import logging
import re
import random
from typing import Dict, List, Optional, Set

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('avito_parser.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AvitoParser:
    def __init__(self, telegram_bot_token: str, telegram_chat_id: str):
        self.telegram_bot_token = telegram_bot_token
        self.telegram_chat_id = telegram_chat_id
        self.seen_ads: Set[str] = set()
        
        # Параметры поиска
        self.search_params = {
            'query': 'iPhone 16 Pro Max 256',
            'min_price': 50000,
            'max_price': 60000,
            'location': 'Москва',
            'search_radius': 100,  # км
        }
        
        # Список User-Agent для ротации
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        ]

    def get_random_headers(self) -> Dict[str, str]:
        """Возвращает случайные заголовки для запроса"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        }

    def search_avito(self) -> List[Dict]:
        """Основной метод поиска через веб-интерфейс"""
        base_url = "https://www.avito.ru"
        
        # Формируем URL с параметрами
        params = {
            'q': self.search_params['query'],
            'pmin': self.search_params['min_price'],
            'pmax': self.search_params['max_price'],
            's': '104',  # Сортировка по дате (свежие)
            'f': 'ASgCAQECAkS4lgIUFJmWAgUYlZYCwAIBQOIC1gIA',  # Только с фото
            'user': '1',  # От частных лиц
            'radius': self.search_params['search_radius'],
        }
        
        try:
            # Получаем страницу с объявлениями
            response = requests.get(
                f"{base_url}/moskva/telefony",
                params=params,
                headers=self.get_random_headers(),
                timeout=30,
                allow_redirects=True
            )
            response.raise_for_status()
            
            # Извлекаем данные из страницы
            return self.parse_search_page(response.text)
            
        except Exception as e:
            logger.error(f"Ошибка при поиске: {e}")
            return []

    def parse_search_page(self, html_content: str) -> List[Dict]:
        """Парсинг HTML страницы с результатами поиска"""
        items = []
        
        # Ищем контейнеры с объявлениями
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Находим все карточки объявлений
        ad_cards = soup.find_all('div', {'data-marker': 'item'})
        
        for card in ad_cards:
            try:
                # Извлекаем данные из карточки
                title_elem = card.find('h3', {'itemprop': 'name'})
                title = title_elem.text.strip() if title_elem else ''
                
                # Проверяем, что это iPhone 16 Pro Max
                if not self.is_target_iphone(title):
                    continue
                
                # URL объявления
                link_elem = card.find('a', {'data-marker': 'item-title'})
                ad_url = f"https://www.avito.ru{link_elem['href']}" if link_elem else ''
                
                if not ad_url:
                    continue
                
                # Цена
                price_elem = card.find('meta', {'itemprop': 'price'})
                price = int(price_elem['content']) if price_elem else 0
                
                # Описание
                desc_elem = card.find('div', {'class': re.compile(r'description')})
                description = desc_elem.text.strip() if desc_elem else ''
                
                # Локация
                location_elem = card.find('div', {'data-marker': 'item-address'})
                location = location_elem.text.strip() if location_elem else ''
                
                # Дата
                date_elem = card.find('div', {'data-marker': 'item-date'})
                date_text = date_elem.text.strip() if date_elem else ''
                
                # ID объявления
                ad_id = card.get('data-item-id', '')
                
                item = {
                    'id': ad_id,
                    'title': title,
                    'description': description,
                    'price': price,
                    'url': ad_url,
                    'location': location,
                    'date': date_text
                }
                
                items.append(item)
                
            except Exception as e:
                logger.debug(f"Ошибка парсинга карточки: {e}")
                continue
        
        return items

    def is_target_iphone(self, title: str) -> bool:
        """Проверяет, что это нужный iPhone"""
        title_lower = title.lower()
        
        # Ключевые слова для iPhone 16 Pro Max
        keywords = ['iphone 16 pro max', 'айфон 16 про макс']
        
        # Проверяем модель
        if not any(keyword in title_lower for keyword in keywords):
            return False
        
        # Проверяем память (256 ГБ)
        memory_match = re.search(r'256\s*(гб|gb)', title_lower)
        if not memory_match:
            # Если память не указана в заголовке, проверяем позже
            pass
        
        return True

    def check_location(self, location: str) -> bool:
        """Проверка локации (Москва и область)"""
        location_lower = location.lower()
        
        # Москва
        moscow_patterns = ['москва', 'мск', 'г.москва', 'м. ', 'метро']
        
        # Московская область (ключевые города)
        region_cities = [
            'балашиха', 'химки', 'люберцы', 'королев', 'мытищи',
            'одинцово', 'красногорск', 'подольск', 'электросталь',
            'коломна', 'сергиев посад', 'щелково', 'волоколамск',
            'дмитров', 'наро-фоминск', 'подольск', 'раменское'
        ]
        
        # Проверяем Москву
        for pattern in moscow_patterns:
            if pattern in location_lower:
                return True
        
        # Проверяем города области
        for city in region_cities:
            if city in location_lower:
                return True
        
        # Проверяем общие указания на область
        if any(word in location_lower for word in ['московск', 'подмосков', 'м.о.', 'мо']):
            return True
        
        return False

    def check_item(self, item: Dict) -> bool:
        """Полная проверка объявления"""
        # Проверяем, что объявление еще не обрабатывалось
        if item['id'] in self.seen_ads:
            return False
        
        # Проверяем локацию
        if not self.check_location(item['location']):
            return False
        
        # Проверяем цену
        if not (self.search_params['min_price'] <= item['price'] <= self.search_params['max_price']):
            return False
        
        # Проверяем память в описании
        full_text = f"{item['title']} {item['description']}".lower()
        
        # Ищем указание на память
        memory_pattern = r'(\d+)\s*(гб|gb|гигабайт)'
        matches = re.findall(memory_pattern, full_text)
        
        if matches:
            for size, unit in matches:
                try:
                    size_int = int(size)
                    # Проверяем, что память не меньше 256 ГБ
                    if size_int < 256:
                        return False
                except:
                    continue
        
        # Проверяем состояние
        if self.check_condition(full_text) == 'bad':
            return False
        
        return True

    def check_condition(self, text: str) -> str:
        """Проверка состояния телефона"""
        text_lower = text.lower()
        
        # Плохое состояние
        bad_keywords = [
            'битый', 'разбит', 'треснул', 'сколы', 'сильно поцарапан',
            'поврежден', 'глубокие царапины', 'восстановлен',
            'реплика', 'копия', 'refurbished'
        ]
        
        for keyword in bad_keywords:
            if keyword in text_lower:
                return 'bad'
        
        # Хорошее состояние
        good_keywords = [
            'новый', 'не распакован', 'заводская упаковка',
            'полный комплект', 'не использовался'
        ]
        
        for keyword in good_keywords:
            if keyword in text_lower:
                return 'good'
        
        return 'acceptable'

    def send_telegram_notification(self, item: Dict) -> bool:
        """Отправка уведомления в Telegram"""
        try:
            message = (
                f"🎯 *Найдено новое объявление!*\n\n"
                f"📱 *{item['title']}*\n"
                f"💰 *Цена:* {item['price']:,} ₽\n"
                f"📍 *Место:* {item['location']}\n"
                f"📅 *Дата:* {item['date']}\n\n"
                f"📝 *Описание:*\n{item['description'][:150]}...\n\n"
                f"[👉 Смотреть объявление]({item['url']})"
            )
            
            telegram_url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
            
            payload = {
                'chat_id': self.telegram_chat_id,
                'text': message,
                'parse_mode': 'Markdown',
                'disable_web_page_preview': False,
                'reply_markup': json.dumps({
                    'inline_keyboard': [[
                        {'text': 'Открыть объявление', 'url': item['url']}
                    ]]
                })
            }
            
            response = requests.post(telegram_url, json=payload, timeout=10)
            response.raise_for_status()
            
            # Сохраняем ID объявления
            self.seen_ads.add(item['id'])
            
            logger.info(f"Уведомление отправлено: {item['title']}")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка отправки в Telegram: {e}")
            return False

    def run(self, interval_minutes: int = 10):
        """Запуск парсера"""
        logger.info("Запуск парсера Авито...")
        logger.info(f"Ищем: {self.search_params['query']}")
        logger.info(f"Цена: {self.search_params['min_price']} - {self.search_params['max_price']} ₽")
        logger.info(f"Локация: {self.search_params['location']}")
        
        while True:
            try:
                logger.info("=" * 50)
                logger.info("Начинаю поиск...")
                
                # Поиск объявлений
                items = self.search_avito()
                
                if items:
                    logger.info(f"Найдено {len(items)} объявлений")
                    
                    new_items = 0
                    for item in items:
                        if self.check_item(item):
                            self.send_telegram_notification(item)
                            new_items += 1
                            time.sleep(1)  # Пауза между отправками
                    
                    logger.info(f"Отправлено {new_items} новых уведомлений")
                else:
                    logger.info("Объявлений не найдено")
                
                logger.info(f"Ожидание {interval_minutes} минут...")
                time.sleep(interval_minutes * 60)
                
            except KeyboardInterrupt:
                logger.info("Парсер остановлен")
                break
            except Exception as e:
                logger.error(f"Ошибка: {e}")
                logger.info("Повтор через 5 минут...")
                time.sleep(300)

def main():
    """Основная функция"""
    # === НАСТРОЙКИ ===
    TELEGRAM_BOT_TOKEN = "8262427477:AAEMU1smBCp92FeanCl1HQKEdVzvLdgCLEA"
    TELEGRAM_CHAT_ID = "-1003665450639"
    
    if TELEGRAM_BOT_TOKEN == "ВАШ_ТОКЕН_БОТА" or TELEGRAM_CHAT_ID == "ВАШ_CHAT_ID":
        print("=" * 60)
        print("НАСТРОЙКА ПАРСЕРА")
        print("=" * 60)
        print("1. Создайте бота через @BotFather")
        print("2. Получите токен (пример: 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11)")
        print("3. Узнайте chat_id через @userinfobot")
        print("4. Вставьте значения в переменные выше")
        return
    
    # Установите нужные параметры поиска
    parser = AvitoParser(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
    
    # Настройки поиска
    parser.search_params = {
        'query': 'iPhone 16 Pro Max 256',  # Можно изменить
        'min_price': 50000,
        'max_price': 60000,
        'location': 'Москва',
        'search_radius': 100,
    }
    
    # Запуск
    parser.run(interval_minutes=15)  # Проверка каждые 15 минут

if __name__ == "__main__":
    # Установите библиотеки
    # pip install requests beautifulsoup4 lxml
    
    main()