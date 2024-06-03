import React, { useState, useEffect } from 'react';
import axios from 'axios';


export function Network() {
    const [ifNetwork, setIfNetwork] = useState(null);
    const [ifConnection, setIfConnection] = useState(null);
    function checkNetwork() {
        if (navigator.onLine) {
            setIfNetwork('online');
        } else {
            setIfNetwork('offline');
            alert('Network is offline');
        }
    }

    function checkConnection() {
        try {
            axios.get('http://127.0.0.1:8000/') 
                .then((response) => {
                    if (response.status === 200) {
                        setIfConnection('online');
                        // console.log('online');
                    } else {
                        throw new Error('Server response was not ok');
                    }
                })
                .catch((error) => {
                    setIfConnection('offline');
                    alert('Server is offline');
                    // console.log('offline');
                });
        } catch (error) {
            setIfConnection('offline');
            // console.log('error err');
            // console.log(error);
        }
    }

    function checkConnections() {
        checkNetwork();
        checkConnection();
    }

    useEffect (() => {
        const interval = setInterval (checkConnections, 1000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div>
            <p>Network: {ifNetwork === 'online' ? "Network is on" : "Network is off"} </p>
            <p>Connection: {ifConnection === 'online' ? "Connection is on" : "Connection is off"}</p>
        </div>
    );
}