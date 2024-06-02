import React, { useEffect} from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useCombinedContext } from './context';

export function TeamInfo() {
    const { id } = useParams();
    const { teamsList } = useCombinedContext();
    const idd = parseInt(id);
    const teamInfo = teamsList.find((team) => team.id === idd);
    // const value =  teamsList.find((team) => team.id === idd)?.name || 'Unknown';
    const navigate = useNavigate();

    if (!teamInfo) {
        return <div>Loading...</div>;
    }

    const navigateBack = () => {
        navigate('/team');
    };

    return (
        <div>
            <h2>Team Information</h2>
            <p>Id: {teamInfo.id}</p>
            <p>Name: {teamInfo.name}</p>
            <p>Country: {teamInfo.country}</p>
            <button onClick={navigateBack}>Back to the list</button>
        </div>
    );

} 
