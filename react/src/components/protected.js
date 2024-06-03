import React, { useEffect, useState } from 'react';
import { createContext, useContext } from 'react';
import { useNavigate } from 'react-router-dom';

const withAuth = (WrappedComponent) => {
    const AuthenticatedComponent = (props) => {
        const navigate = useNavigate();
        const [loading, setLoading] = useState(true);
        useEffect(() => {
            const verifyToken = async () => {
                const token = localStorage.getItem('token');
                console.log(token);
                try {
                    const response = await fetch('http://localhost:8000/verify-token/' + token);

                    if (response.ok === false) {
                        throw new Error('Token verification failed');
                    }
                    setLoading(false);
                } catch (error) {
                    localStorage.removeItem('token');
                    navigate('/');
                    return null;
                }
            };

            verifyToken();
        }, [navigate]);
        const isAuthenticated = true;
        if (!isAuthenticated) {
            navigate('/');
            return null;
        }
        if (loading) {
            return <div>Loading...</div>;
        } else {
            return <WrappedComponent {...props} />
        }

            // <div>
            //     <h1>Protected Page</h1>
            //     <div> Only visible for authenticated users </div>
            // </div>
    };

    return AuthenticatedComponent;
};

// const AuthenticatedComponent = ({ component: Component, ...rest }) => {
//     return <Component {...rest} />;
// };
// export const withAuth = (WrappedComponent) => (props) =>{
//     return <AuthenticatedComponent component={WrappedComponent} {...props} />;
// };
export default withAuth;
// export default ProtectedPage;
// export { ProtectedPage };


const AuthenticatedContext = createContext();

export const AuthenticatedProvider = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState([]);
    return (
        <AuthenticatedContext.Provider value={{ isAuthenticated, setIsAuthenticated }}>
            {children}
        </AuthenticatedContext.Provider>
    );
};

export const useAuthenticatedContext = () => useContext(AuthenticatedContext);