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

import pytest
from main import BooksCollector

class TestBooksCollector:

    @pytest.fixture
    def collector(self):
        return BooksCollector()

    def test_add_new_book_add_two_books(self, collector):
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2

    @pytest.mark.parametrize('book_name', ['Книга', 'A' * 40, 'A' * 1])
    def test_add_valid_book_name(self, collector, book_name):
        collector.add_new_book(book_name)
        assert book_name in collector.get_books_genre()

    @pytest.mark.parametrize('invalid_name', ['', 'О' * 41])
    def test_cannot_add_invalid_book_name(self, collector, invalid_name):
        collector.add_new_book(invalid_name)
        assert invalid_name not in collector.get_books_genre()

    def test_cannot_add_duplicate_book(self, collector):
        collector.add_new_book('Зеленая миля')
        collector.add_new_book('Зеленая миля')
        assert len(collector.get_books_genre()) == 1

    def test_added_book_has_no_genre(self, collector):
        collector.add_new_book('Новая книга')
        assert collector.get_book_genre('Новая книга') == ''

    def test_set_genre_for_existing_book(self, collector):
        collector.add_new_book('1984')
        collector.set_book_genre('1984', 'Фантастика')
        assert collector.books_genre['1984'] == 'Фантастика'

    @pytest.mark.parametrize('valid_genre', [
        'Фантастика', 'Ужасы', 'Детективы', 'Мультфильмы', 'Комедии'
    ])
    def test_set_all_valid_genres(self, collector, valid_genre):
        collector.add_new_book('Тестовая книга')
        collector.set_book_genre('Тестовая книга', valid_genre)
        assert collector.books_genre['Тестовая книга'] == valid_genre

    def test_cannot_set_genre_when_book_not_exists(self, collector):
        collector.set_book_genre('Несуществующая книга', 'Фантастика')
        assert 'Несуществующая книга' not in collector.books_genre

    def test_cannot_set_genre_when_genre_invalid(self, collector):
        collector.add_new_book('Книга')
        collector.set_book_genre('Книга', 'Несуществующий жанр')
        assert collector.books_genre['Книга'] == ''

    def test_can_change_existing_genre(self, collector):
        collector.add_new_book('Книга')
        collector.set_book_genre('Книга', 'Фантастика')
        collector.set_book_genre('Книга', 'Комедии')
        assert collector.books_genre['Книга'] == 'Комедии'

    def test_get_book_genre_returns_correct_genre(self, collector):
        collector.books_genre = {'Книга с жанром': 'Детективы'}
        assert collector.get_book_genre('Книга с жанром') == 'Детективы'

    def test_get_book_genre_returns_empty_for_book_without_genre(self, collector):
        collector.books_genre = {'Книга без жанра': ''}
        assert collector.get_book_genre('Книга без жанра') == ''

    def test_get_book_genre_returns_none_for_nonexistent_book(self, collector):
        assert collector.get_book_genre('Несуществующая книга') is None

    def test_get_books_with_specific_genre(self, collector):
        collector.books_genre = {
            'Фантастика 1': 'Фантастика',
            'Фантастика 2': 'Фантастика',
            'Комедия 1': 'Комедии'
        }
        fantasy_books = collector.get_books_with_specific_genre('Фантастика')
        assert fantasy_books == ['Фантастика 1', 'Фантастика 2']

    def test_get_books_for_children_excludes_age_rated_books(self, collector):
        collector.books_genre = {
            'Мультфильм': 'Мультфильмы',
            'Комедия': 'Комедии',
            'Ужасы': 'Ужасы',
            'Детектив': 'Детективы'
        }
        children_books = collector.get_books_for_children()
        assert children_books == ['Мультфильм', 'Комедия']

    def test_get_books_genre_returns_all_books(self, collector):
        collector.books_genre = {'Книга 1': 'Фантастика', 'Книга 2': ''}
        all_books = collector.get_books_genre()
        assert all_books == {'Книга 1': 'Фантастика', 'Книга 2': ''}

    def test_add_book_to_favorites(self, collector):
        collector.books_genre = {'Любимая книга': 'Фантастика'}
        collector.add_book_in_favorites('Любимая книга')
        assert 'Любимая книга' in collector.favorites

    def test_cannot_add_nonexistent_book_to_favorites(self, collector):
        collector.add_book_in_favorites('Несуществующая книга')
        assert 'Несуществующая книга' not in collector.favorites

    def test_cannot_add_duplicate_to_favorites(self, collector):
        collector.books_genre = {'Книга': 'Фантастика'}
        collector.add_book_in_favorites('Книга')
        collector.add_book_in_favorites('Книга')
        assert collector.favorites == ['Книга']

    def test_remove_book_from_favorites(self, collector):
        collector.favorites = ['Книга']
        collector.delete_book_from_favorites('Книга')
        assert 'Книга' not in collector.favorites

    def test_remove_nonexistent_book_from_favorites_no_error(self, collector):
        # Этот тест проверяет, что метод не вызывает исключение
        collector.delete_book_from_favorites('Несуществующая книга')
        assert True  # Если дошли сюда - исключения не было

    def test_get_list_of_favorites_books_returns_correct_list(self, collector):
        collector.favorites = ['Книга 1', 'Книга 2']
        assert collector.get_list_of_favorites_books() == ['Книга 1', 'Книга 2']