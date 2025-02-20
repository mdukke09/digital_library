import pytest
from fastapi import HTTPException
from datetime import datetime
from unittest.mock import Mock, patch
from app.api.v1.endpoints.users import create_user, read_user, read_users, update_user, delete_user
from app.schemas.user import UserCreate, UserUpdate

class MockUser:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

# Mock data
mock_user_data = {
    "id": 1,
    "name": "Test User",
    "email": "test@example.com",
    "registration_date": datetime.now(),
    "borrowed_books": []
}

@pytest.fixture
def mock_db():
    return Mock()

@pytest.fixture
def mock_current_user():
    return {"user_id": 1, "email": "test@example.com"}

class TestUserEndpoints:
    
    def test_create_user_success(self, mock_db):
        user_in = UserCreate(
            name="Test User",
            email="test@example.com",
            password="Password123!"
        )
        
        with patch('app.crud.user.user.get_by_email') as mock_get_by_email:
            mock_get_by_email.return_value = None
            
            with patch('app.crud.user.user.create') as mock_create:
                mock_create.return_value = MockUser(**mock_user_data)
                
                # Quitamos el mock de send_welcome_email ya que no existe ese módulo
                response = create_user(db=mock_db, user_in=user_in)
                
                assert response.name == "Test User"
                assert response.email == "test@example.com"
                mock_create.assert_called_once()

    def test_create_user_email_exists(self, mock_db):
        user_in = UserCreate(
            name="Test User",
            email="existing@example.com",
            password="Password123!"
        )
        
        with patch('app.crud.user.user.get_by_email') as mock_get_by_email:
            mock_get_by_email.return_value = MockUser(**mock_user_data)
            
            with pytest.raises(HTTPException) as exc_info:
                create_user(db=mock_db, user_in=user_in)
            
            assert exc_info.value.status_code == 400
            assert "Ya existe un usuario con este email" in str(exc_info.value.detail)

    def test_read_users(self, mock_db, mock_current_user):
        mock_users = [MockUser(**mock_user_data), MockUser(**mock_user_data)]
        
        with patch('app.crud.user.user.get_multi') as mock_get_multi:
            mock_get_multi.return_value = mock_users
            
            response = read_users(
                db=mock_db,
                skip=0,
                limit=10,
                current_user=mock_current_user
            )
            
            assert len(response) == 2
            mock_get_multi.assert_called_once_with(mock_db, skip=0, limit=10)

    def test_read_user_success(self, mock_db, mock_current_user):
        with patch('app.crud.user.user.get') as mock_get:
            mock_get.return_value = MockUser(**mock_user_data)
            
            response = read_user(
                db=mock_db,
                user_id=1,
                current_user=mock_current_user
            )
            
            assert response.id == 1
            assert response.email == "test@example.com"
            mock_get.assert_called_once_with(mock_db, id=1)

    def test_update_user_success(self, mock_db, mock_current_user):
        updated_data = {**mock_user_data, "name": "Updated User"}
        
        with patch('app.crud.user.user.get') as mock_get:
            mock_get.return_value = MockUser(**mock_user_data)
            
            with patch('app.crud.user.user.get_by_email') as mock_get_by_email:
                mock_get_by_email.return_value = None
                
                with patch('app.crud.user.user.update') as mock_update:
                    mock_update.return_value = MockUser(**updated_data)
                    
                    user_update = UserUpdate(name="Updated User")
                    response = update_user(
                        db=mock_db,
                        user_id=1,
                        user_in=user_update,
                        current_user=mock_current_user
                    )
                    
                    assert response.name == "Updated User"
                    mock_update.assert_called_once()

    def test_delete_user_success(self, mock_db, mock_current_user):
        with patch('app.crud.user.user.get') as mock_get:
            mock_get.return_value = MockUser(**mock_user_data)
            
            with patch('app.crud.user.user.remove') as mock_remove:
                mock_remove.return_value = MockUser(**mock_user_data)
                
                response = delete_user(
                    db=mock_db,
                    user_id=1,
                    current_user=mock_current_user
                )
                
                assert response.id == 1
                mock_remove.assert_called_once_with(mock_db, id=1)

    def test_delete_user_with_borrowed_books(self, mock_db, mock_current_user):
        user_with_books = {
            **mock_user_data,
            "borrowed_books": [{"id": 1, "title": "Borrowed Book"}]
        }
        
        with patch('app.crud.user.user.get') as mock_get:
            mock_get.return_value = MockUser(**user_with_books)
            
            with pytest.raises(HTTPException) as exc_info:
                delete_user(
                    db=mock_db,
                    user_id=1,
                    current_user=mock_current_user
                )
            
            assert exc_info.value.status_code == 400
            assert "tiene libros prestados" in str(exc_info.value.detail)