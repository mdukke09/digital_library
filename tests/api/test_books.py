import pytest
from fastapi import HTTPException
from datetime import datetime
from unittest.mock import Mock, patch
from app.api.v1.endpoints.books import (
    create_book, read_book, read_books, update_book, delete_book,
    search_books, borrow_book, return_book
)
from app.schemas.book import BookCreate, BookUpdate

class MockBook:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class MockAuthor:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

# Mock data
mock_author_data = {
    "id": 1,
    "name": "Test Author",
    "birth_date": datetime(1990, 1, 1)
}

mock_book_data = {
    "id": 1,
    "title": "Test Book",
    "author_id": 1,
    "publication_year": 2023,
    "borrowed_by_id": None,
    "author": MockAuthor(**mock_author_data),
    "borrowed_by": None
}

@pytest.fixture
def mock_db():
    return Mock()

@pytest.fixture
def mock_current_user():
    return {"user_id": 1, "email": "test@example.com"}

class TestBookEndpoints:
    
    def test_create_book_success(self, mock_db, mock_current_user):
        book_in = BookCreate(
            title="Test Book",
            author_id=1,
            publication_year=2023
        )
        
        with patch('app.crud.author.author.get') as mock_get_author:
            mock_get_author.return_value = MockAuthor(**mock_author_data)
            
            with patch('app.crud.book.book.create') as mock_create:
                mock_create.return_value = MockBook(**mock_book_data)
                
                response = create_book(
                    db=mock_db,
                    book_in=book_in,
                    current_user=mock_current_user
                )
                
                assert response.title == "Test Book"
                assert response.author_id == 1
                mock_create.assert_called_once()

    def test_create_book_author_not_found(self, mock_db, mock_current_user):
        book_in = BookCreate(
            title="Test Book",
            author_id=999,
            publication_year=2023
        )
        
        with patch('app.crud.author.author.get') as mock_get_author:
            mock_get_author.return_value = None
            
            with pytest.raises(HTTPException) as exc_info:
                create_book(
                    db=mock_db,
                    book_in=book_in,
                    current_user=mock_current_user
                )
            
            assert exc_info.value.status_code == 404
            assert "autor con ID 999 no existe" in str(exc_info.value.detail)

    def test_read_books(self, mock_db):
        mock_books = [MockBook(**mock_book_data), MockBook(**mock_book_data)]
        
        with patch('app.crud.book.book.get_multi') as mock_get_multi:
            mock_get_multi.return_value = mock_books
            
            response = read_books(db=mock_db, skip=0, limit=10)
            
            assert len(response) == 2
            mock_get_multi.assert_called_once_with(mock_db, skip=0, limit=10)

    def test_read_book_success(self, mock_db):
        with patch('app.crud.book.book.get') as mock_get:
            mock_get.return_value = MockBook(**mock_book_data)
            
            response = read_book(db=mock_db, book_id=1)
            
            assert response.id == 1
            assert response.title == "Test Book"
            mock_get.assert_called_once_with(mock_db, id=1)

    def test_read_book_not_found(self, mock_db):
        with patch('app.crud.book.book.get') as mock_get:
            mock_get.return_value = None
            
            with pytest.raises(HTTPException) as exc_info:
                read_book(db=mock_db, book_id=999)
            
            assert exc_info.value.status_code == 404
            assert "Libro no encontrado" in str(exc_info.value.detail)

    def test_update_book_success(self, mock_db, mock_current_user):
        updated_data = {**mock_book_data, "title": "Updated Book"}
        
        with patch('app.crud.book.book.get') as mock_get:
            mock_get.return_value = MockBook(**mock_book_data)
            
            with patch('app.crud.book.book.update') as mock_update:
                mock_update.return_value = MockBook(**updated_data)
                
                book_update = BookUpdate(title="Updated Book")
                response = update_book(
                    db=mock_db,
                    book_id=1,
                    book_in=book_update,
                    current_user=mock_current_user
                )
                
                assert response.title == "Updated Book"
                mock_update.assert_called_once()

    def test_delete_book_success(self, mock_db, mock_current_user):
        with patch('app.crud.book.book.get') as mock_get:
            mock_get.return_value = MockBook(**mock_book_data)
            
            with patch('app.crud.book.book.remove') as mock_remove:
                mock_remove.return_value = MockBook(**mock_book_data)
                
                response = delete_book(
                    db=mock_db,
                    book_id=1,
                    current_user=mock_current_user
                )
                
                assert response.id == 1
                mock_remove.assert_called_once_with(mock_db, id=1)

    def test_search_books(self, mock_db):
        with patch('app.crud.book.book.search_books') as mock_search:
            mock_search.return_value = [MockBook(**mock_book_data)]
            
            response = search_books(
                db=mock_db,
                title="Test",
                author_id=1,
                publication_year=2023
            )
            
            assert len(response) == 1
            assert response[0].title == "Test Book"
            mock_search.assert_called_once_with(
                mock_db,
                title="Test",
                author_id=1,
                publication_year=2023
            )

    def test_borrow_book_success(self, mock_db, mock_current_user):
        available_book = MockBook(**mock_book_data)
        borrowed_book = MockBook(**{**mock_book_data, "borrowed_by_id": 1})
        
        with patch('app.crud.book.book.get') as mock_get:
            mock_get.return_value = available_book
            
            with patch('app.crud.user.user.get') as mock_get_user:
                mock_get_user.return_value = Mock(id=1)
                
                with patch('app.crud.book.book.borrow_book') as mock_borrow:
                    mock_borrow.return_value = borrowed_book
                    
                    response = borrow_book(
                        db=mock_db,
                        book_id=1,
                        current_user=mock_current_user
                    )
                    
                    assert response.borrowed_by_id == 1
                    mock_borrow.assert_called_once_with(mock_db, book_id=1, user_id=1)

    def test_borrow_book_already_borrowed(self, mock_db, mock_current_user):
        borrowed_book = MockBook(**{**mock_book_data, "borrowed_by_id": 2})
        
        with patch('app.crud.book.book.get') as mock_get:
            mock_get.return_value = borrowed_book
            
            with pytest.raises(HTTPException) as exc_info:
                borrow_book(
                    db=mock_db,
                    book_id=1,
                    current_user=mock_current_user
                )
            
            assert exc_info.value.status_code == 400
            assert "libro ya está prestado" in str(exc_info.value.detail)

    def test_return_book_success(self, mock_db, mock_current_user):
        borrowed_book = MockBook(**{**mock_book_data, "borrowed_by_id": 1})
        returned_book = MockBook(**{**mock_book_data, "borrowed_by_id": None})
        
        with patch('app.crud.book.book.get') as mock_get:
            mock_get.return_value = borrowed_book
            
            with patch('app.crud.book.book.return_book') as mock_return:
                mock_return.return_value = returned_book
                
                response = return_book(
                    db=mock_db,
                    book_id=1,
                    current_user=mock_current_user
                )
                
                assert response.borrowed_by_id is None
                mock_return.assert_called_once_with(mock_db, book_id=1)

    def test_return_book_not_borrowed(self, mock_db, mock_current_user):
        not_borrowed_book = MockBook(**{**mock_book_data, "borrowed_by_id": None})
        
        with patch('app.crud.book.book.get') as mock_get:
            mock_get.return_value = not_borrowed_book
            
            with pytest.raises(HTTPException) as exc_info:
                return_book(
                    db=mock_db,
                    book_id=1,
                    current_user=mock_current_user
                )
            
            assert exc_info.value.status_code == 400
            assert "El libro no está prestado" in str(exc_info.value.detail)

    def test_return_book_wrong_user(self, mock_db, mock_current_user):
        borrowed_by_other = MockBook(**{**mock_book_data, "borrowed_by_id": 2})
        
        with patch('app.crud.book.book.get') as mock_get:
            mock_get.return_value = borrowed_by_other
            
            with pytest.raises(HTTPException) as exc_info:
                return_book(
                    db=mock_db,
                    book_id=1,
                    current_user=mock_current_user
                )
            
            assert exc_info.value.status_code == 403
            assert "No puedes devolver un libro que no te prestaron" in str(exc_info.value.detail)