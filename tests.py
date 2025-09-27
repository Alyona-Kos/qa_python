import pytest
from main import BooksCollector

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
        assert len(collector.get_books_genre()) == 2  # исправлено на get_books_genre

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()

    @pytest.mark.parametrize('book_name, expected', [
        ('Книга', True),
        ('A' * 40, True),
        ('A' * 1, True),
    ])
    def test_add_valid_book_name(self, book_name, expected):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        assert (book_name in collector.books_genre) == expected

    @pytest.mark.parametrize('invalid_name', [
        '',
        'О' * 41,
    ])
    def test_cannot_add_invalid_book_name(self, invalid_name):
        collector = BooksCollector()
        collector.add_new_book(invalid_name)
        assert invalid_name not in collector.books_genre

    def test_cannot_add_duplicate_book(self):
        collector = BooksCollector()
        collector.add_new_book('Зеленая миля')
        collector.add_new_book('Зеленая миля')
        assert len(collector.books_genre) == 1

    def test_added_book_has_no_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Новая книга')
        assert collector.get_book_genre('Новая книга') == ''

    # Тесты установки жанров
    def test_set_genre_when_book_exists_and_genre_valid(self):
        collector = BooksCollector()
        collector.add_new_book('1984')
        collector.set_book_genre('1984', 'Фантастика')
        assert collector.get_book_genre('1984') == 'Фантастика'

    def test_cannot_set_genre_when_book_not_exists(self):
        collector = BooksCollector()
        collector.set_book_genre('Несуществующая книга', 'Фантастика')
        assert 'Несуществующая книга' not in collector.books_genre

    def test_cannot_set_genre_when_genre_invalid(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.set_book_genre('Книга', 'Несуществующий жанр')
        assert collector.get_book_genre('Книга') == ''

    def test_can_change_existing_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.set_book_genre('Книга', 'Фантастика')
        collector.set_book_genre('Книга', 'Комедии')
        assert collector.get_book_genre('Книга') == 'Комедии'

    @pytest.mark.parametrize('valid_genre', [
        'Фантастика', 'Ужасы', 'Детективы', 'Мультфильмы', 'Комедии'
    ])
    def test_can_set_all_valid_genres(self, valid_genre):
        collector = BooksCollector()
        collector.add_new_book('Тестовая книга')
        collector.set_book_genre('Тестовая книга', valid_genre)
        assert collector.get_book_genre('Тестовая книга') == valid_genre

    # Тесты получения книг по жанрам
    def test_get_books_with_specific_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Фантастика 1')
        collector.add_new_book('Фантастика 2')
        collector.add_new_book('Комедия 1')

        collector.set_book_genre('Фантастика 1', 'Фантастика')
        collector.set_book_genre('Фантастика 2', 'Фантастика')
        collector.set_book_genre('Комедия 1', 'Комедии')

        fantasy_books = collector.get_books_with_specific_genre('Фантастика')
        assert len(fantasy_books) == 2
        assert 'Фантастика 1' in fantasy_books
        assert 'Фантастика 2' in fantasy_books
        assert 'Комедия 1' not in fantasy_books

    def test_get_books_for_children_excludes_age_rated_books(self):
        collector = BooksCollector()

        collector.add_new_book('Мультфильм')
        collector.add_new_book('Комедия')
        collector.set_book_genre('Мультфильм', 'Мультфильмы')
        collector.set_book_genre('Комедия', 'Комедии')

        collector.add_new_book('Ужасы')
        collector.add_new_book('Детектив')
        collector.set_book_genre('Ужасы', 'Ужасы')
        collector.set_book_genre('Детектив', 'Детективы')

        children_books = collector.get_books_for_children()

        assert 'Мультфильм' in children_books
        assert 'Комедия' in children_books
        assert 'Ужасы' not in children_books
        assert 'Детектив' not in children_books

    def test_get_books_genre_returns_all_books(self):
        collector = BooksCollector()
        collector.add_new_book('Книга 1')
        collector.add_new_book('Книга 2')
        collector.set_book_genre('Книга 1', 'Фантастика')

        all_books = collector.get_books_genre()
        assert len(all_books) == 2
        assert 'Книга 1' in all_books
        assert 'Книга 2' in all_books
        assert all_books['Книга 1'] == 'Фантастика'
        assert all_books['Книга 2'] == ''

    # Тесты работы с избранными
    def test_add_book_to_favorites(self):
        collector = BooksCollector()
        collector.add_new_book('Любимая книга')
        collector.add_book_in_favorites('Любимая книга')
        assert 'Любимая книга' in collector.get_list_of_favorites_books()

    def test_cannot_add_nonexistent_book_to_favorites(self):
        collector = BooksCollector()
        collector.add_book_in_favorites('Несуществующая книга')
        assert 'Несуществующая книга' not in collector.get_list_of_favorites_books()

    def test_cannot_add_duplicate_to_favorites(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.add_book_in_favorites('Книга')
        collector.add_book_in_favorites('Книга')
        assert len(collector.get_list_of_favorites_books()) == 1

    def test_remove_book_from_favorites(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.add_book_in_favorites('Книга')
        collector.delete_book_from_favorites('Книга')
        assert 'Книга' not in collector.get_list_of_favorites_books()

    def test_remove_nonexistent_book_from_favorites_no_error(self):
        collector = BooksCollector()
        # Должно выполниться без ошибок
        collector.delete_book_from_favorites('Несуществующая книга')

    def test_get_favorites_returns_correct_list(self):
        collector = BooksCollector()
        collector.add_new_book('Книга 1')
        collector.add_new_book('Книга 2')
        collector.add_book_in_favorites('Книга 1')

        favorites = collector.get_list_of_favorites_books()
        assert 'Книга 1' in favorites
        assert 'Книга 2' not in favorites
        assert len(favorites) == 1