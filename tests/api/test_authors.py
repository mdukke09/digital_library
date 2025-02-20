import pytest
from fastapi import HTTPException
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, PropertyMock
from app.api.v1.endpoints.authors import create_author, read_author, read_authors, update_author, delete_author
from app.schemas.author import AuthorCreate, AuthorUpdate
from app.crud.author import author

class MockAuthor:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

# Mock data
mock_author_data = {
    "id": 1,
    "name": "New Author",
    "birth_date": datetime(1990, 1, 1),
    "books": []
}

@pytest.fixture
def mock_db():
    return Mock()

@pytest.fixture
def mock_current_user():
    return {"user_id": 1, "email": "test@example.com"}

class TestAuthorEndpoints:
    
    def test_create_author_success(self, mock_db, mock_current_user):
        author_in = AuthorCreate(
            name="New Author",
            birth_date="01/01/1990"
        )
        
        mock_response = MockAuthor(**mock_author_data)
        
        with patch('app.crud.author.author.create') as mock_create:
            mock_create.return_value = mock_response
            
            response = create_author(
                db=mock_db,
                author_in=author_in,
                current_user=mock_current_user
            )
            
            assert response.name == "New Author"
            mock_create.assert_called_once()

    def test_create_author_future_birth_date(self, mock_db, mock_current_user):
        future_date = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
        author_in = AuthorCreate(
            name="New Author",
            birth_date=future_date
        )
        
        with pytest.raises(HTTPException) as exc_info:
            create_author(
                db=mock_db,
                author_in=author_in,
                current_user=mock_current_user
            )
        
        assert exc_info.value.status_code == 400
        assert "fecha de nacimiento no puede ser futura" in str(exc_info.value.detail)

    def test_read_authors(self, mock_db):
        mock_responses = [MockAuthor(**mock_author_data), MockAuthor(**mock_author_data)]
        
        with patch('app.crud.author.author.get_multi') as mock_get_multi:
            mock_get_multi.return_value = mock_responses
            
            response = read_authors(db=mock_db, skip=0, limit=10)
            
            assert len(response) == 2
            mock_get_multi.assert_called_once_with(mock_db, skip=0, limit=10)

    def test_read_author_success(self, mock_db):
        mock_response = MockAuthor(**mock_author_data)
        
        with patch('app.crud.author.author.get') as mock_get:
            mock_get.return_value = mock_response
            
            response = read_author(db=mock_db, author_id=1)
            
            assert response.id == 1
            assert response.name == "New Author"
            mock_get.assert_called_once_with(mock_db, id=1)

    def test_read_author_not_found(self, mock_db):
        with patch('app.crud.author.author.get') as mock_get:
            mock_get.return_value = None
            
            with pytest.raises(HTTPException) as exc_info:
                read_author(db=mock_db, author_id=999)
            
            assert exc_info.value.status_code == 404
            assert "Autor no encontrado" in str(exc_info.value.detail)

    def test_update_author_success(self, mock_db, mock_current_user):
        mock_original = MockAuthor(**mock_author_data)
        updated_data = {**mock_author_data, "name": "Updated Author"}
        mock_updated = MockAuthor(**updated_data)
        
        with patch('app.crud.author.author.get') as mock_get:
            mock_get.return_value = mock_original
            
            with patch('app.crud.author.author.update') as mock_update:
                mock_update.return_value = mock_updated
                
                author_update = AuthorUpdate(name="Updated Author")
                response = update_author(
                    db=mock_db,
                    author_id=1,
                    author_in=author_update,
                    current_user=mock_current_user
                )
                
                assert response.name == "Updated Author"
                mock_update.assert_called_once()

    def test_delete_author_success(self, mock_db, mock_current_user):
        mock_response = MockAuthor(**mock_author_data)
        
        with patch('app.crud.author.author.get') as mock_get:
            mock_get.return_value = mock_response
            
            with patch('app.crud.author.author.remove') as mock_remove:
                mock_remove.return_value = mock_response
                
                response = delete_author(
                    db=mock_db,
                    author_id=1,
                    current_user=mock_current_user
                )
                
                assert response.id == 1
                mock_remove.assert_called_once_with(mock_db, id=1)

    def test_delete_author_with_books(self, mock_db, mock_current_user):
        author_with_books = {**mock_author_data, "books": [{"id": 1, "title": "Test Book"}]}
        mock_response = MockAuthor(**author_with_books)
        
        with patch('app.crud.author.author.get') as mock_get:
            mock_get.return_value = mock_response
            
            with pytest.raises(HTTPException) as exc_info:
                delete_author(
                    db=mock_db,
                    author_id=1,
                    current_user=mock_current_user
                )
            
            assert exc_info.value.status_code == 400
            assert "tiene libros asociados" in str(exc_info.value.detail)