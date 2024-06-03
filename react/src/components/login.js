import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    const navigate = useNavigate();
    const location = useLocation();

    const isRegistered = location.pathname === '/register';

    const validateForm = () => {
        if (username === '' || password === '') {
            setError('Please fill in all fields');
            return false;
        }
        if (isRegistered) {
            if (password.length < 6) {
                setError('Password must be at least 6 characters');
                return false;
            }
            // check if the password is a combination of capital letters, small letters, numbers and special characters
            if (!password.match(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$/)) {
                setError('Password must contain at least one uppercase letter, one lowercase letter, one number and one special character');
                return false;
            }
        }
        setError('');
        return true;
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!validateForm()) {
            return;
        }
        setLoading(true);

        const formDetails = new URLSearchParams();
        formDetails.append('username', username);
        formDetails.append('password', password);
        const dataUser = {
            username: username,
            password: password
        }

        if (!isRegistered) {
            try {
                const response = await fetch('http://localhost:8000/token', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: formDetails,
                });
                setLoading(false);

                const data = await response.json();
                if (data.error) {
                    setError(data.error);
                } else {
                    localStorage.setItem('token', data.access_token);
                    navigate('/home');
                }
            } catch (error) {
                setLoading(false);
                setError('An error occurred. Please try again later.');
            }
        } else {
            try {
                const response = await fetch('http://localhost:8000/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(dataUser),
                });
                setLoading(false);

                const data = await response.json();
                if (data.error) {
                    setError(data.error);
                } else {
                    navigate('/');
                }
            } catch (error) {
                setLoading(false);
                setError('An error occurred. Please try again later.');
            }
        }

    };

    return (
        <div>
            <h1>{isRegistered ? 'Register' : 'Login'}</h1>
            <p>{isRegistered ? 'Create an account' : 'Login to your account'}</p>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Username</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                </div>
                <div>
                    <label>Password</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                {error && <div>{error}</div>}
                <button type="submit" disabled={loading}>
                    {loading ? 'Loading...' : 'Login'}
                </button>
            </form>
        </div>
    );
} 

export { Login };