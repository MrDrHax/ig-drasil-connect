import React, { createContext, useState, useContext, useEffect } from 'react';
import { Alert } from "@material-tailwind/react";


const AlertContext = createContext();

export function AlertProvider({ children }) {
    const [showAlert, setShowAlert] = useState(false);
    const [alert, setAlert] = useState({ color: 'gray', message: 'This is a test' });
    const [timeoutId, setTimeoutId] = useState(null);

    const showAlertWithMessage = (color, message, time = 5000) => {
        setAlert({ color, message });
        setShowAlert(true);

        if (timeoutId) {
            clearTimeout(timeoutId);
        }

        const id = setTimeout(() => {
            setShowAlert(false);
        }, time);
        
        setTimeoutId(id);
    };

    useEffect(() => {
        return () => {
            if (timeoutId) {
                clearTimeout(timeoutId);
            }
        };
    }, [timeoutId]);

    return (
        <AlertContext.Provider value={{ alert, showAlertWithMessage }}>
            {children}
            <div className="fixed bottom-0 p-4">
            {showAlert ? (
                <Alert
                    color={alert.color}
                    onClose={() => setShowAlert(false)}
                >
                    {alert.message}
                </Alert>
                ) : ""}
            </div>
        </AlertContext.Provider>
    );
}


export function useAlert() {
    return useContext(AlertContext);
}

export default useAlert;