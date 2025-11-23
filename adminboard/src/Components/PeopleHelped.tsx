import React, { useEffect, useState } from 'react';

const PeopleHelped = () => {
    const [count, setCount] = useState(null);

    useEffect(() => {
        // Înlocuiește URL-ul cu endpoint-ul tău real
        fetch('https://exemplu.com/api/people-helped')
            .then((response) => response.json())
            .then((data) => {
                // presupunem că API-ul returnează { count: 123 }
                setCount(data.count);
            })
            .catch((error) => {
                console.error('Eroare la preluarea datelor:', error);
            });
    }, []);

    return (
        <div style={{
        border: '1px solid #333',
            padding: '10px 20px',
            borderRadius: '5px',
            display: 'inline-block',
            textAlign: 'center'
    }}>
    <p style={{ margin: 0, fontWeight: 'bold' }}>Oameni ajutati astazi</p>
    <p style={{ margin: 0, fontSize: '1.5rem' }}>{count !== null ? count : '...'}</p>
    </div>
);
};

export default PeopleHelped;
