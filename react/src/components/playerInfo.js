import React, { useEffect, useState } from 'react';
import { useLocation, useParams, useNavigate } from 'react-router-dom';

export function PlayerInfo() {
    const { id } = useParams();
    console.log(id);
    const location = useLocation();
    const [playerInfo, setPlayerInfo] = useState(null);
    const { name, age, team_id } = location.state.player;
    const navigate = useNavigate();

    useEffect(() => {
        if (location.state && location.state.player) {
            setPlayerInfo(location.state.player);
        }

    }, [location]);
    
    if (!playerInfo) {
        return <div>Loading...</div>;
    }

    const navigateBack = () => {
        navigate('/player');
    };

    return (
        <div>
            <h2>Player Information</h2>
            <p>Id: {id}</p>
            <p>Name: {playerInfo.name}</p>
            <p>Age: {playerInfo.age}</p>
            <p>Club: {playerInfo.team_id}</p>
            <button onClick = {navigateBack}>Back to the list</button>
        </div>
    );
}