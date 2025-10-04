
import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from bytebox.auth.helpers import get_session_user, parse_auth_header, generate_token
from bytebox.users.models import UserModel

class TestParseAuthHeader:
    def test_parse_auth_header_with_valid_token(self):
        """Test parsing a valid authorization header."""
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RAdGVzdC5jb20iLCJ1c2VybmFtZSI6InRlc3R1c2VyIn0.signature"
        authorization = f"Bearer {token}"
        
        with patch('bytebox.auth.helpers.jwt.decode') as mock_decode:
            mock_decode.return_value = {"email": "test@test.com", "username": "testuser"}
            claims, parsed_token = parse_auth_header(authorization)
            
            assert claims == {"email": "test@test.com", "username": "testuser"}
            assert parsed_token == token
            mock_decode.assert_called_once()
    
    def test_parse_auth_header_with_none(self):
        """Test parsing when authorization header is None."""
        with pytest.raises(HTTPException) as exc_info:
            parse_auth_header(None)
        
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Unauthorized"
    
    def test_parse_auth_header_with_invalid_format(self):
        """Test parsing with invalid authorization header format."""
        with pytest.raises(HTTPException) as exc_info:
            parse_auth_header("InvalidFormat")
        
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Invalid authorization header"
    
    def test_parse_auth_header_with_wrong_scheme(self):
        """Test parsing with wrong authentication scheme."""
        with pytest.raises(HTTPException) as exc_info:
            parse_auth_header("Basic token123")
        
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Invalid authorization header"
    
    def test_parse_auth_header_with_invalid_token(self):
        """Test parsing with invalid JWT token."""
        authorization = "Bearer invalid.token.here"
        
        with patch('bytebox.auth.helpers.jwt.decode') as mock_decode:
            mock_decode.side_effect = Exception("Invalid token")
            
            with pytest.raises(HTTPException) as exc_info:
                parse_auth_header(authorization)
            
            assert exc_info.value.status_code == 401
            assert exc_info.value.detail == "Invalid token"


class TestGenerateToken:
    def test_generate_token_with_valid_user(self):
        """Test generating a token for a valid user."""
        user = UserModel(
            id=1,
            email="test@test.com",
            username="testuser",
            password="hashed_password"
        )
        
        with patch('bytebox.auth.helpers.jwt.encode') as mock_encode:
            mock_encode.return_value = "generated.token.here"
            token = generate_token(user, "test-jwt-secret")
            
            assert token == "generated.token.here"
            mock_encode.assert_called_once_with(
                {"email": "test@test.com", "username": "testuser"},
                "test-jwt-secret",  # JWT_SECRET
                algorithm="HS256"
            )


class TestGetSessionUser:
    def test_get_session_user_with_valid_token(self):
        """Test getting session user with valid authorization."""
        mock_db = Mock()
        mock_user = UserModel(
            id=1,
            email="test@test.com",
            username="testuser",
            password="hashed_password"
        )
        authorization = "Bearer valid.token.here"
        
        with patch('bytebox.auth.helpers.UserRepository') as mock_repo_class:
            mock_repo = Mock()
            mock_repo.get_by_email_or_username.return_value = mock_user
            mock_repo_class.from_session.return_value = mock_repo
            
            with patch('bytebox.auth.helpers.parse_auth_header') as mock_parse:
                mock_parse.return_value = (
                    {"email": "test@test.com", "username": "testuser"},
                    "valid.token.here"
                )
                
                user = get_session_user(mock_db, authorization)
                
                assert user == mock_user
                mock_repo_class.from_session.assert_called_once_with(mock_db)
                mock_repo.get_by_email_or_username.assert_called_once_with(
                    "test@test.com",
                    "testuser"
                )
    
    def test_get_session_user_with_no_authorization(self):
        """Test getting session user without authorization header."""
        mock_db = Mock()
        
        with pytest.raises(HTTPException) as exc_info:
            get_session_user(mock_db, None)
        
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Unauthorized"
    
    def test_get_session_user_with_invalid_token(self):
        """Test getting session user with invalid token."""
        mock_db = Mock()
        authorization = "Bearer invalid.token"
        
        with patch('bytebox.auth.helpers.parse_auth_header') as mock_parse:
            mock_parse.side_effect = HTTPException(status_code=401, detail="Invalid token")
            
            with pytest.raises(HTTPException) as exc_info:
                get_session_user(mock_db, authorization)
            
            assert exc_info.value.status_code == 401
            assert exc_info.value.detail == "Invalid token"
