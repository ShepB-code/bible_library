#Bible library
import requests 

class Bible:
    known_bibles = {"KJV": "de4e12af7f28f599-02", "DRA": "179568874c45066f-01"}

    def __init__(self, api_key="", bible_id=known_bibles["KJV"]):
        self.api = BibleAPI(api_key=api_key)
        self.bible_id = bible_id

    def get_verse(self, book_name="", chapter="", verse=""):
        reference = f"{book_name} {chapter}:{verse}"
        book_id = self.api.get_book_names(self.bible_id)[book_name]
        chapter_id = self.api.get_chapter_names(bible_id=self.bible_id, book_id=book_id)[chapter]
        verse_id = self.api.get_verse_names(bible_id=self.bible_id, chapter_id=chapter_id)[reference]
        verse = self.api.get_verse(bible_id=self.bible_id, verse_id=verse_id)["data"]
        return verse["content"]

    
class BibleAPI:

    def __init__(self, api_key=""):
        self.headers = {'api-key': api_key}


    def get_bibles(self):
        return requests.get(f'https://api.scripture.api.bible/v1/bibles/', headers=self.headers).json()
    def get_bible(self, bible_id=""):
        return requests.get(f'https://api.scripture.api.bible/v1/bibles/{bible_id}', headers=self.headers).json()

    
    def get_books(self, bible_id=""):
        return requests.get(f'https://api.scripture.api.bible/v1/bibles/{bible_id}/books', headers=self.headers).json()
    def get_book(self, bible_id=""):
        return requests.get(f'https://api.scripture.api.bible/v1/bibles/{bible_id}/books', headers=self.headers).json()
    def get_book_names(self, bible_id=""):
        books = dict() 
        for book in self.get_books(bible_id=bible_id)['data']:
            books[book.get("name")] = book.get("id")
        return books

    def get_chapters(self, bible_id="", book_id=""):
        return requests.get(f'https://api.scripture.api.bible/v1/bibles/{bible_id}/books/{book_id}/chapters', headers=self.headers).json()
    def get_chapter(self, bible_id="", chapter_id=""):
        return requests.get(f'https://api.scripture.api.bible/v1/bibles/{bible_id}/chapters/{chapter_id}', headers=self.headers).json()
    def get_chapter_names(self, bible_id="", book_id=""):
        chapters = dict()
        for chapter in self.get_chapters(bible_id=bible_id, book_id=book_id)['data']:
            chapters[chapter.get("number")] = chapter.get("id")
        return chapters
        
    def get_verses(self, bible_id="", chapter_id=""):
        return requests.get(f'https://api.scripture.api.bible/v1/bibles/{bible_id}/chapters/{chapter_id}/verses', headers=self.headers).json()
    def get_verse(self, bible_id="", verse_id="", params={"content-type": "text", "include-verse-numbers": False}):
        return requests.get(f'https://api.scripture.api.bible/v1/bibles/{bible_id}/verses/{verse_id}',headers=self.headers, params=params).json()
        
    def get_verse_names(self, bible_id="", chapter_id=""):
        verses = dict() 
        for verse in self.get_verses(bible_id=bible_id, chapter_id=chapter_id)['data']:
            verses[verse.get("reference")] = verse.get("id")
        return verses
main()   