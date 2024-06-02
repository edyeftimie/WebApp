import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

function ProtectedPage() {
    const navigate = useNavigate();

    useEffect(() => {
        const verifyToken = async () => {
            const token = localStorage.getItem('token');
            console.log(token);
            try {
                const response = await fetch('http://localhost:8000/verify-token/' + token);

                if (response.ok === false) {
                    throw new Error('Token verification failed');
                }
            } catch (error) {
                localStorage.removeItem('token');
                navigate('/');
            }
        };

        verifyToken();
    }, [navigate]);

    return (
        <div>
            <h1>Protected Page</h1>
            <div> Only visible for authenticated users </div>
        </div>
    );
}

export default ProtectedPage;
export { ProtectedPage };